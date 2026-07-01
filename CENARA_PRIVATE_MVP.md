# Cenara Private MVP

Cenara is a private GXEON-operated MVP for assisted short-video generation. The user-facing product name is **Cenara** and the owner signature is **Powered by GXEON**.

## Upstream attribution

Cenara is based on the upstream **MoneyPrinterTurbo** project and preserves the original MIT license and attribution in `LICENSE` and the upstream documentation. Do not represent Cenara as built from zero.

## Railway readiness

The Docker/Railway runtime serves the Streamlit WebUI on port `8501` (or Railway's injected `PORT`). Railway should use `/_stcore/health` for the service health check because the active Railway process is Streamlit. The FastAPI app still exposes `/healthz` publicly when that runtime is served directly.

Required Railway variables before exposing a public domain:

- `GX1_ACCESS_TOKEN`: required strong private operator token. Do not commit this value.
- `ENVIRONMENT`: set to `production`.
- `CORS_ALLOWED_ORIGINS`: set to the Railway public domain after the domain exists, or keep empty during private review.

Keep the Railway service private until `GX1_ACCESS_TOKEN` is configured.
