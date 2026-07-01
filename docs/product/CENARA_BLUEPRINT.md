# Cenara product blueprint

## Status

Cenara is a **private MVP only** for internal/operator use. It is **not public SaaS yet** and should not be exposed to untrusted customers without additional authentication, tenant isolation, billing, abuse controls, storage hardening, and legal review.

## Identity

- User-facing product name: **Cenara**.
- UI attribution: **Powered by GXEON**.
- Compatibility env var: `GX1_ACCESS_TOKEN`.
- Upstream attribution: MoneyPrinterTurbo MIT notices remain in `LICENSE`, `NOTICE`, and docs.

## Security baseline

- Operator token required for generation, media, task, music, video-material, script, term, social-metadata, stream, download, and static task access.
- `/healthz` remains unauthenticated for deployment health checks.
- Production/Railway CORS must be configured explicitly via `CORS_ALLOWED_ORIGINS`; it does not default to `*`.
- WebUI production/Railway mode requires the private token before sensitive controls render.
- API keys shown in WebUI are masked placeholders and are never prefilled in full.

## Static media warning

The static `/tasks` mount exists for private operator review only. Even with token protection, it is not designed as a public customer delivery surface.
