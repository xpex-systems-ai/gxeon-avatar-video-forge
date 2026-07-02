# Cenara Ultimate Generation Workspace

Cenara now presents the Streamlit app as a premium dark AI video workspace instead of a single technical form. The authenticated operator enters a cohesive shell with topbar, hero, provider control center, an eight-step generation stepper, and a three-panel creation flow.

## Runtime preservation

- The private operator token gate still runs before the authenticated workspace renders.
- The real `VideoParams` payload and `tm.start(...)` generation path are preserved.
- Provider secrets remain write-only in the UI: blank inputs do not overwrite saved keys.
- Generated MP4 files are surfaced in the preview/download area and recent library.

## Workspace panels

1. **AI Briefing** captures topic, niche, audience, promise, CTA, script, keywords, duration, format, media source, and voice.
2. **Build Engine** summarizes media, voice, subtitles, and advanced runtime controls while keeping MoneyPrinterTurbo controls available.
3. **Preview & Output** shows render status, the latest real video preview, MP4 download, and recent project history.

## Persistence

Successful and failed Cenara generation attempts are stored in `storage/cenara_projects.json` with task id, title, provider source, aspect, status, MP4 path, and timestamp. This lightweight history powers the recent projects area without changing Docker, Railway, or backend API behavior.
