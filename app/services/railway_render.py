"""Railway-safe low-memory MP4 renderer.

This module intentionally uses subprocess ffmpeg/ffprobe only. Do not import
MoviePy here; survival mode exists to avoid MoviePy memory pressure on Railway.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from loguru import logger

from app.services.runtime_limits import get_runtime_limits
from app.utils import utils

MIN_FINAL_MP4_BYTES = 100 * 1024


def _is_inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def safe_output_roots() -> list[Path]:
    storage = Path(utils.storage_dir(create=True)).resolve()
    return [storage / "tasks", storage]


def is_safe_final_mp4_path(path: str | os.PathLike[str], min_bytes: int = MIN_FINAL_MP4_BYTES, allow_part: bool = False) -> tuple[bool, str]:
    try:
        candidate = Path(path).expanduser().resolve()
        if candidate.suffix.lower() != ".mp4" and not (allow_part and candidate.name.endswith(".mp4.part")):
            return False, "NOT_MP4"
        if not candidate.is_file():
            return False, "MISSING_FILE"
        if candidate.name.startswith(("temp-clip", "combined-")) or candidate.name.endswith(".browser.mp4"):
            return False, "INTERMEDIATE_MP4"
        if candidate.stat().st_size < min_bytes:
            return False, "MP4_TOO_SMALL"
        if not any(_is_inside(candidate, root) for root in safe_output_roots()):
            return False, "UNSAFE_OUTPUT_PATH"
        return True, "ok"
    except OSError:
        return False, "PATH_ERROR"


def ffprobe_validate_mp4(path: str | os.PathLike[str], min_bytes: int = MIN_FINAL_MP4_BYTES, allow_part: bool = False) -> dict[str, Any]:
    safe, reason = is_safe_final_mp4_path(path, min_bytes=min_bytes, allow_part=allow_part)
    result: dict[str, Any] = {"valid": False, "reason": reason, "ffprobe_available": False, "duration": 0.0, "size_bytes": 0}
    candidate = Path(path)
    if candidate.exists():
        result["size_bytes"] = candidate.stat().st_size
    if not safe:
        return result
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        result.update(valid=True, reason="ffprobe_unavailable_size_checked")
        return result
    result["ffprobe_available"] = True
    try:
        probe = subprocess.run(
            [ffprobe, "-v", "error", "-show_entries", "format=duration", "-show_streams", "-of", "json", str(candidate)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            timeout=20,
        )
        data = json.loads(probe.stdout or "{}")
        streams = data.get("streams") or []
        has_video = any(stream.get("codec_type") == "video" for stream in streams)
        duration = float((data.get("format") or {}).get("duration") or 0.0)
        result.update(valid=has_video and duration > 0, reason="ok" if has_video and duration > 0 else "NO_VIDEO_STREAM", duration=duration)
        return result
    except Exception as exc:
        logger.warning(f"survival ffprobe validation failed: {type(exc).__name__}")
        result["reason"] = "FFPROBE_FAILED"
        return result


def _scale_filter(aspect: str, width: int, height: int) -> str:
    if aspect == "9:16":
        return f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1"
    return f"scale='min({width},iw)':-2,setsar=1"


def render_survival_mp4(task_id, source_video_path, audio_path, subtitle_path, output_path, duration_seconds, aspect="9:16"):
    limits = get_runtime_limits()
    stages: list[dict[str, Any]] = []
    output = Path(output_path).expanduser().resolve()
    part = output.with_name(f"{output.name}.part")
    result: dict[str, Any] = {"success": False, "output_path": str(output), "size_bytes": 0, "duration": 0.0, "safe_message": "", "stages": stages}
    ffmpeg = shutil.which("ffmpeg") or utils.get_ffmpeg_binary()
    if not ffmpeg:
        result.update(safe_error_code="FFMPEG_UNAVAILABLE", safe_message="FFmpeg não encontrado para render survival.")
        return result
    source = Path(source_video_path).expanduser().resolve()
    if not source.is_file() or source.stat().st_size <= 0:
        result.update(safe_error_code="NO_PROVIDER_VIDEO", safe_message="Nenhum vídeo de provedor válido foi encontrado.")
        return result
    output.parent.mkdir(parents=True, exist_ok=True)
    for cleanup in (part, output if output.exists() and output.stat().st_size == 0 else None):
        if cleanup:
            cleanup.unlink(missing_ok=True)
    duration = max(1.0, float(duration_seconds or 1.0))
    stages.append({"stage": "subtitle", "subtitle_skipped_survival_mode": bool(subtitle_path and Path(subtitle_path).exists())})
    command = [ffmpeg, "-y", "-hide_banner", "-loglevel", "warning", "-i", str(source)]
    audio = Path(audio_path).expanduser().resolve() if audio_path else None
    has_audio = bool(audio and audio.is_file() and audio.stat().st_size > 0)
    if has_audio:
        command += ["-i", str(audio)]
    command += ["-t", f"{duration:.3f}", "-vf", _scale_filter(aspect, limits.railway_max_width, limits.railway_max_height), "-r", str(limits.render_fps), "-c:v", "libx264", "-preset", "ultrafast", "-crf", "30", "-b:v", limits.video_bitrate, "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    if has_audio:
        command += ["-map", "0:v:0", "-map", "1:a:0", "-c:a", "aac", "-b:a", limits.audio_bitrate, "-shortest"]
    else:
        command += ["-an"]
    command += ["-f", "mp4", str(part)]
    stages.append({"stage": "ffmpeg_start", "engine": "ffmpeg_survival"})
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, timeout=max(120, int(duration * 30)))
        validation = ffprobe_validate_mp4(part, allow_part=True)
        stages.append({"stage": "ffprobe", **validation})
        if not validation["valid"]:
            part.unlink(missing_ok=True)
            result.update(safe_error_code=validation.get("reason", "INVALID_MP4"), safe_message="Render survival gerou MP4 inválido; arquivo final não foi publicado.")
            return result
        os.replace(part, output)
        final_validation = ffprobe_validate_mp4(output)
        if not final_validation["valid"]:
            output.unlink(missing_ok=True)
            result.update(safe_error_code=final_validation.get("reason", "INVALID_FINAL_MP4"), safe_message="MP4 final falhou na validação após publicação atômica.")
            return result
        result.update(success=True, size_bytes=output.stat().st_size, duration=final_validation.get("duration", 0.0), safe_message="MP4 final verificado", validation=final_validation)
        stages.append({"stage": "published", "output_file": output.name})
        return result
    except subprocess.CalledProcessError as exc:
        logger.warning(f"survival ffmpeg failed: {exc.stderr[-800:] if exc.stderr else type(exc).__name__}")
        result.update(safe_error_code="FFMPEG_RENDER_FAILED", safe_message="FFmpeg survival falhou sem publicar MP4 final.")
    except Exception as exc:
        logger.warning(f"survival render failed: {type(exc).__name__}")
        result.update(safe_error_code="SURVIVAL_RENDER_FAILED", safe_message="Render survival falhou sem publicar MP4 final.")
    finally:
        part.unlink(missing_ok=True)
        if output.exists() and output.stat().st_size == 0:
            output.unlink(missing_ok=True)
    return result
