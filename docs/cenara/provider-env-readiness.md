# Cenara provider env readiness on Railway

Cenara reads provider credentials from Railway environment variables first, then from the current Streamlit session, then from the existing app configuration. The UI only reports provider status (`Configurado`, `Ausente`, `Opcional` or `Bloqueado`) and must never render raw secret values.

## Required Railway variables

| Provider | Accepted Railway variable names | Required when |
| --- | --- | --- |
| OpenAI / LLM | `OPENAI_API_KEY` or `OPENAI_KEY` | Always required for real AI-assisted generation. |
| Pexels | `PEXELS_API_KEY` | Required when the video source is Pexels. |
| Pixabay | `PIXABAY_API_KEY` | Required when the video source is Pixabay. |
| Cover / Coverr | `COVER_API_KEY` or `COVERR_API_KEY` | Optional unless the video source is Coverr. Both aliases are accepted. |
| ElevenLabs | `ELEVENLABS_API_KEY` or `ELEVEN_API_KEY` | Required when ElevenLabs TTS is selected and no custom audio is uploaded. |

## Readiness behavior

- Empty strings, whitespace-only values, masked placeholders and placeholder text such as `Cole sua nova chave...` are treated as missing.
- Password inputs are intentionally blank on page load; Railway variables are still detected without pasting them again.
- Generation fails closed when a required provider for the selected source or voice path is missing.
- Preview and download controls are shown only for a new non-empty MP4 created by the current generation run.

## Troubleshooting Railway

After adding or changing Railway variables, redeploy the Railway service so the running container receives the updated environment. Then open the Provider Center and verify statuses only; do not paste or expose secret values in logs, screenshots or support messages.
