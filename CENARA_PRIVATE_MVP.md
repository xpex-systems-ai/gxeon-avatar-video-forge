# Cenara private MVP deployment guide

Cenara is GXEON's private operator UI for this MVP. This repository remains based on the upstream MoneyPrinterTurbo project and preserves the upstream MIT license and attribution.

## Railway runtime

Railway deploys the private MVP as a Streamlit process, not as the FastAPI API process:

```bash
streamlit run ./webui/Main.py --server.address=0.0.0.0 --server.port=${PORT:-8501}
```

The Railway healthcheck must use Streamlit's health endpoint:

```text
/_stcore/health
```

Do not rely on a FastAPI `/healthz` endpoint for the Railway service while the deployed process is Streamlit.

## Required Railway variables before public link generation

Set these before generating or sharing a Railway public domain:

- `ENVIRONMENT=production` — enables production-like safety behavior.
- `GX1_ACCESS_TOKEN=<strong-private-operator-token>` — required private operator token for the Streamlit gate and protected API/media access.

Optional variables:

- `CORS_ALLOWED_ORIGINS=https://your-approved-origin.example` — comma-separated browser origins for public API usage.
- `RAILWAY_ENVIRONMENT`, `RAILWAY_PROJECT_ID`, and `RAILWAY_SERVICE_ID` are provided by Railway and are treated as production-like runtime signals.

## CORS guidance

CORS must not default to wildcard (`*`) in Railway or production-like runtime. Empty `CORS_ALLOWED_ORIGINS` is acceptable for private Streamlit UI review because the browser is not meant to call the FastAPI API publicly. Before public API usage, set `CORS_ALLOWED_ORIGINS` to explicit trusted origins.

Only explicit local development may fall back to wildcard CORS.

## Security checklist

- `GX1_ACCESS_TOKEN` is preferred over `config.app["api_key"]` as the expected operator token.
- API requests may authenticate with either `Authorization: Bearer <token>` or `x-api-key: <token>`.
- Video and LLM API routers require token verification.
- Generated task media under `/tasks` requires the same token verification.
- Provider keys must never be committed in `config.toml`, `.env`, screenshots, logs, or docs.

## Product scope

This PR is private MVP only. It does not add public SaaS customer login, billing, Hotmart integration, payment flows, Product Hunt launch material, or autoposting.

## Attribution

Cenara is a GXEON-branded private MVP built from MoneyPrinterTurbo. The original MoneyPrinterTurbo MIT license is preserved in `LICENSE`, and attribution is recorded in `NOTICE`.
