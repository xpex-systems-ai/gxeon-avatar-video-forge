# Cenara Railway memory stability

This guardrail keeps real MP4 generation available on low-memory Railway deployments without treating provider credentials or OpenAI quota as the bottleneck.

## What changed

- Railway low-memory mode is enabled automatically when `RAILWAY_ENVIRONMENT` or `RAILWAY_SERVICE_NAME` is present.
- Remote provider MP4s are streamed to `.part` files and rejected before or during download when they exceed the configured cap.
- Rendering uses a lower-memory profile: capped dimensions, one render thread, lower FPS, and lower audio bitrate.
- Preview and download are explicit operator actions. Biblioteca cards are metadata-first and do not eagerly load MP4 bytes.
- A single-flight generation lock prevents concurrent MoviePy/FFmpeg jobs inside the Streamlit process.
- Storage pruning removes stale `.part`, zero-byte, temp, combined, old task, and oversized cached provider artifacts.

## Recommended Railway variables

These defaults are already applied in Railway low-memory mode, but can be set explicitly:

| Variable | Recommended value |
| --- | --- |
| `CENARA_LOW_MEMORY_MODE` | `true` |
| `CENARA_MAX_REMOTE_VIDEO_MB` | `24` |
| `CENARA_MAX_OUTPUT_MP4_MB` | `90` |
| `CENARA_PREVIEW_INLINE_MAX_MB` | `24` |
| `CENARA_DOWNLOAD_PREP_MAX_MB` | `90` |
| `CENARA_LIBRARY_LIMIT` | `5` |
| `CENARA_MAX_DOWNLOADS_PER_TASK` | `3` |
| `CENARA_RENDER_THREADS` | `1` |
| `CENARA_RAILWAY_MAX_WIDTH` | `720` |
| `CENARA_RAILWAY_MAX_HEIGHT` | `1280` |
| `CENARA_PRUNE_CACHE_MAX_MB` | `300` |
| `CENARA_PRUNE_TASKS_KEEP` | `8` |
| `CENARA_GENERATION_LOCK_TTL_SECONDS` | `1800` |

## Safe validation flow

1. Redeploy Railway and confirm boot logs do not show memory crashes.
2. Open Cenara with `GX1_ACCESS_TOKEN`.
3. Generate one 3-second video with `video_count=1` using Pexels or Pixabay.
4. Wait for `mp4_created` or `render_completed_low_memory`.
5. Click preview once. If the MP4 exceeds the inline cap, use download instead.
6. Click download once.
7. Refresh the page and confirm Biblioteca loads as metadata-only cards.
8. Generate a second 3-second video and confirm no Railway memory crash.

## OpenAI quota is separate

OpenAI quota or 429 errors are separate from Railway memory pressure. Cenara's zero-LLM/manual fallback should continue to generate a real local visual MP4 when provider media or LLM calls are unavailable.
