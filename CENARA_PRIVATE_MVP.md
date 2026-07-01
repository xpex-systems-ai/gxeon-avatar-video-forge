# Cenara Private MVP — Railway Deployment Notes

Cenara is the private MVP deployment profile for this MIT-licensed fork of
MoneyPrinterTurbo. Preserve the upstream MoneyPrinterTurbo attribution and MIT
license while presenting the operator-facing product as Cenara.

## Required Railway variables

- `GX1_ACCESS_TOKEN` is required before exposing any public Railway link. Do not
  generate or share the public link until this private operator gate is set.
- `ENVIRONMENT=production` is recommended for Railway private MVP deployments.
  `ENVIRONMENT=railway` is also treated as production-like by the runtime.
- `CORS_ALLOWED_ORIGINS` is optional. For public API use, configure explicit
  trusted origins such as `https://example.com`; do not use wildcard (`*`) CORS
  for Railway or production deployments.

## Runtime and health check

Railway runs the Streamlit web UI for Cenara. Configure Railway health checks to
use Streamlit's health endpoint:

```text
/_stcore/health
```

## Security checklist before public link generation

1. Configure `GX1_ACCESS_TOKEN` in Railway.
2. Set `ENVIRONMENT=production` for the Railway service.
3. If enabling browser access to the FastAPI surface, set
   `CORS_ALLOWED_ORIGINS` to explicit trusted origins only.
4. Confirm provider API keys are entered only through password fields and saved
   key lists remain masked in the UI.
5. Confirm the app still displays Cenara as the user-facing name and keeps the
   Powered by GXEON branding.

## Attribution

Cenara is based on MoneyPrinterTurbo and keeps the upstream MIT license and
attribution intact. Do not remove upstream copyright, license, or repository
references when preparing the private MVP deployment.
