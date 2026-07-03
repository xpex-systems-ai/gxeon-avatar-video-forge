import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int, minimum: int = 0) -> int:
    try:
        return max(minimum, int(float(os.getenv(name, str(default)))))
    except (TypeError, ValueError):
        return default


def _env_float(name: str, default: float, minimum: float = 0.0) -> float:
    try:
        return max(minimum, float(os.getenv(name, str(default))))
    except (TypeError, ValueError):
        return default


def is_railway_runtime() -> bool:
    return bool(os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_SERVICE_NAME"))


@dataclass(frozen=True)
class CenaraRuntimeLimits:
    low_memory_mode: bool
    max_remote_video_mb: int
    max_output_mp4_mb: int
    preview_inline_max_mb: int
    download_prep_max_mb: int
    library_limit: int
    max_downloads_per_task: int
    render_threads: int
    railway_max_width: int
    railway_max_height: int
    prune_cache_max_mb: int
    prune_tasks_keep: int
    generation_lock_ttl_seconds: int
    render_fps: int
    audio_bitrate: str
    video_bitrate: str
    render_engine: str
    disable_local_whisper: bool
    subtitles_optional: bool
    skip_subtitle_on_failure: bool
    subtitle_engine: str

    @property
    def max_remote_video_bytes(self) -> int:
        return self.max_remote_video_mb * 1024 * 1024

    @property
    def max_output_mp4_bytes(self) -> int:
        return self.max_output_mp4_mb * 1024 * 1024

    @property
    def preview_inline_max_bytes(self) -> int:
        return self.preview_inline_max_mb * 1024 * 1024

    @property
    def download_prep_max_bytes(self) -> int:
        return self.download_prep_max_mb * 1024 * 1024


def get_runtime_limits() -> CenaraRuntimeLimits:
    railway = is_railway_runtime()
    low_default = railway
    low_memory = _env_bool("CENARA_LOW_MEMORY_MODE", low_default)
    return CenaraRuntimeLimits(
        low_memory_mode=low_memory,
        max_remote_video_mb=_env_int("CENARA_MAX_REMOTE_VIDEO_MB", 24 if low_memory else 96, 1),
        max_output_mp4_mb=_env_int("CENARA_MAX_OUTPUT_MP4_MB", 45 if low_memory else 300, 1),
        preview_inline_max_mb=_env_int("CENARA_PREVIEW_INLINE_MAX_MB", 12 if low_memory else 150, 1),
        download_prep_max_mb=_env_int("CENARA_DOWNLOAD_PREP_MAX_MB", 45 if low_memory else 300, 1),
        library_limit=_env_int("CENARA_LIBRARY_LIMIT", 5 if low_memory else 12, 1),
        max_downloads_per_task=_env_int("CENARA_MAX_DOWNLOADS_PER_TASK", 1 if low_memory else 8, 1),
        render_threads=_env_int("CENARA_RENDER_THREADS", 1 if low_memory else 2, 1),
        railway_max_width=_env_int("CENARA_RAILWAY_MAX_WIDTH", 540 if low_memory else 720, 240),
        railway_max_height=_env_int("CENARA_RAILWAY_MAX_HEIGHT", 960 if low_memory else 1280, 240),
        prune_cache_max_mb=_env_int("CENARA_PRUNE_CACHE_MAX_MB", 300, 1),
        prune_tasks_keep=_env_int("CENARA_PRUNE_TASKS_KEEP", 8, 1),
        generation_lock_ttl_seconds=_env_int("CENARA_GENERATION_LOCK_TTL_SECONDS", 300 if low_memory else 1800, 60),
        render_fps=_env_int("CENARA_RENDER_FPS", 12 if low_memory else 30, 1),
        audio_bitrate=os.getenv("CENARA_AUDIO_BITRATE", "64k" if low_memory else "192k").strip() or ("64k" if low_memory else "192k"),
        video_bitrate=os.getenv("CENARA_VIDEO_BITRATE", "900k" if low_memory else "2500k").strip() or ("900k" if low_memory else "2500k"),
        render_engine=os.getenv("CENARA_RENDER_ENGINE", "ffmpeg_survival" if low_memory else "moviepy").strip() or ("ffmpeg_survival" if low_memory else "moviepy"),
        disable_local_whisper=_env_bool("CENARA_DISABLE_LOCAL_WHISPER", railway or low_memory),
        subtitles_optional=_env_bool("CENARA_SUBTITLES_OPTIONAL", railway or low_memory),
        skip_subtitle_on_failure=_env_bool("CENARA_SKIP_SUBTITLE_ON_FAILURE", railway or low_memory),
        subtitle_engine=os.getenv("CENARA_SUBTITLE_ENGINE", "script_estimate" if (railway or low_memory) else "provider").strip().lower() or ("script_estimate" if (railway or low_memory) else "provider"),
    )
