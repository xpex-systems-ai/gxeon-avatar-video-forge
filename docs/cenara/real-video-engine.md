# Cenara real video engine E2E validation

Cenara uses the existing MoneyPrinterTurbo task engine from the premium Streamlit workspace. The workspace must never report success unless a non-empty `.mp4` exists on disk.

## Provider readiness

The provider center validates the following before generation:

- LLM provider: configured through the existing provider settings, or avoid LLM calls by providing both manual script and keywords.
- Pexels and Pixabay: required only when selected as the video source.
- Coverr: displayed as optional until selected; when selected, its key is required.
- TTS: a voice must be configured unless a custom audio file is used by the runtime payload.
- FFmpeg: required for MP4 rendering; readiness honors the runtime-compatible resolver, including configured `ffmpeg_path`, `IMAGEIO_FFMPEG_EXE`, `utils.get_ffmpeg_binary()`, PATH, and bundled imageio-ffmpeg when available.
- ImageMagick: shown for subtitle/runtime diagnostics and treated as optional because FFmpeg can still render when subtitle styling does not require it.

Raw API keys are never rendered in the status center, project history, or generation messages. Blank secret fields in the existing provider configuration continue to preserve saved values.

## Generation status contract

The Streamlit cockpit exposes these operator-facing stages in Portuguese:

1. `validando provedores`
2. `preparando roteiro`
3. `buscando mídia`
4. `gerando voz`
5. `montando cenas`
6. `aplicando legendas`
7. `renderizando MP4`
8. `finalizado` or `falhou`

Each run receives a UUID `task_id`. The task is recorded in `storage/cenara_projects.json` with status, source, aspect, output path on success, and a friendly failure reason on failure.

## Railway/runtime diagnostics

The provider center includes a runtime diagnostics card for:

- `ffmpeg` availability.
- `magick` or `convert` ImageMagick availability.
- `storage/` output folder writability.
- `storage/tasks/` task folder readiness.

Do not change `Dockerfile` or `railway.json` for this validation unless a runtime diagnostic proves those files are the blocker.

## Preview and download behavior

After the engine returns, Cenara requires a real, non-empty `.mp4` tied to the current `task_id`: either under `storage/tasks/<task_id>` or returned by the engine from that same task folder. The broader storage scan is only for the recent-library display and is never used to mark the current run successful. Only after strict current-task validation does Cenara show the Streamlit video preview, output path, and MP4 download button. If no current-task MP4 exists, the attempt is saved as failed and the UI shows the diagnostic error instead of a fake success.
