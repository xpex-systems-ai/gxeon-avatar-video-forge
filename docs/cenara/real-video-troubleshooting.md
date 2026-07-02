# Cenara real video troubleshooting

Cenara only treats a generation as successful when the current task creates a new, non-empty `.mp4` inside that task directory. Older files in storage may appear in the library, but they are never used as success for the active render.

## OpenAI 429 `insufficient_quota`

OpenAI 429 `insufficient_quota` means the LLM key is present but the provider cannot serve the request because of quota, billing, rate-limit, or account availability. This is not a Railway deploy failure, not an FFmpeg failure, and not proof that the provider key is missing.

After this failure Cenara reports the LLM as configured but blocked by quota. The safe next actions are:

1. Add billing or quota to the OpenAI project/account.
2. Replace the LLM key in Railway with a usable key.
3. Use manual script mode to bypass LLM script generation.

## Manual script mode bypasses the LLM

If **Roteiro manual opcional** contains text, Cenara uses that text as the canonical script and does not call the LLM to create the main script. If **Palavras-chave opcionais** is filled, Cenara uses those keywords directly. If keywords are empty, Cenara derives simple safe search terms from Tema, Nicho, Público, Promessa, and CTA without calling the LLM.

This mode still requires the downstream real providers needed for the selected route, such as a video source, a TTS/voice option or custom audio, and FFmpeg for rendering.

## Provider keys for full automatic mode

Full automatic mode needs a usable LLM key because the backend must generate the script and/or search terms. Provider presence and provider usability are separate states:

- **Configurado**: a key or local provider configuration exists.
- **Ausente**: Cenara cannot find the required key.
- **Bloqueado por cota**: a key exists but the provider rejected generation due to quota, billing, or rate limit.
- **Falha de autenticação**: a key exists but the provider rejected authentication.
- **Opcional**: the provider is not required for the selected path.
- **Teste pendente**: a key exists but has not been exercised in the current run.

Cenara never displays raw API keys or detailed provider response bodies in the browser.

## Quick 3-second real video test

1. Redeploy Railway after merging the patch.
2. Open Cenara in a private browser and authenticate with `GX1_ACCESS_TOKEN`.
3. Keep the OpenAI key configured, even if it is quota-blocked.
4. Fill **Roteiro manual opcional** with a short complete script.
5. Fill **Palavras-chave opcionais** with terms such as `fitness, treino em casa, saúde`.
6. Select Pexels, Pixabay, Coverr, or local media with the matching provider key/material available.
7. Select a voice or upload custom audio.
8. Choose duration **3** and aspect **9:16**.
9. Generate and confirm status moves through script, media, voice/subtitles, render, and completed.
10. Confirm preview/download appears only when the current task produced a real non-empty MP4.

If no MP4 appears, inspect the **Prévia Real** status JSON for `failed_stage`, `safe_error_code`, `safe_message`, `next_action`, `script_ready`, `media_ready`, `audio_ready`, and `ffmpeg_available`.
