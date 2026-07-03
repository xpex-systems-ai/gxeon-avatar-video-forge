# Cenara Railway render survival mode

Railway containers can terminate a process during MoviePy composition when memory spikes. In Railway low-memory mode Cenara selects `ffmpeg_survival`, a direct FFmpeg CLI renderer that uses one downloaded provider video, trims it to the requested duration, scales it to a small vertical frame, and publishes only an atomically validated final MP4.

## Recommended Railway variables

```text
CENARA_LOW_MEMORY_MODE=true
CENARA_RENDER_ENGINE=ffmpeg_survival
CENARA_MAX_DOWNLOADS_PER_TASK=1
CENARA_RAILWAY_MAX_WIDTH=540
CENARA_RAILWAY_MAX_HEIGHT=960
CENARA_RENDER_FPS=12
CENARA_VIDEO_BITRATE=900k
CENARA_AUDIO_BITRATE=64k
CENARA_MAX_OUTPUT_MP4_MB=45
CENARA_PREVIEW_INLINE_MAX_MB=12
CENARA_DOWNLOAD_PREP_MAX_MB=45
CENARA_LIBRARY_LIMIT=5
CENARA_GENERATION_LOCK_TTL_SECONDS=600
```

## Validation rules

Survival mode writes `cenara-final-{task_id}.mp4.part` first. The file is atomically renamed to `cenara-final-{task_id}.mp4` only after validation confirms it is inside safe storage, is larger than 100 KB, has an `.mp4` extension, and passes `ffprobe` when available. Zero-byte files, `.part` files, browser previews, `temp-clip*`, and `combined-*` files are invalid deliverables.

## Test protocol

1. Redeploy Railway.
2. Generate one 3-second real video from Pexels or Pixabay.
3. Confirm Biblioteca shows one non-zero `MP4 final verificado` item.
4. Click `Abrir preview seguro`.
5. Click `Preparar download seguro` and download the MP4.
6. Repeat with 7 seconds only after the 3-second test succeeds.
