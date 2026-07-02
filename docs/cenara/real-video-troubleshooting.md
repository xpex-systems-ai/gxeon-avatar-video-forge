# Cenara real video troubleshooting

Cenara real generation no longer depends on an LLM quota to start the render pipeline.

## Local script and keyword fallback

When the lower real-generation form has no manual script, Cenara reuses the existing MoneyPrinterTurbo `video_script` field when it is safe. If that is blank or looks like a provider failure, Cenara builds a deterministic PT-BR ad script from tema, público, promessa, nicho and CTA. Keywords are taken from manual terms first, then existing `video_terms`, then deterministic safe terms derived locally from the brief and script.

## Provider failover

For external stock media, Cenara attempts the selected provider first, then configured Pexels, Pixabay and Coverr. The status file records only safe provider names and statuses, never raw provider responses or secrets.

## Local visual fallback MP4

If no external provider returns a usable current-task MP4, Cenara uses FFmpeg to create a truthful local visual fallback MP4 in the current task directory. The fallback is labeled as `fallback_video_used=true` and should not be described as stock footage.

## Strict MP4 gate

A generation is successful only after Cenara verifies a `.mp4` exists inside the current task directory, has non-zero size, and was created during the current task. Old MP4 files are not reused as success.
