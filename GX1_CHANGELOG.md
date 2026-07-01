# GX1 Changelog

## Private MVP hardening

- Rebranded the Streamlit WebUI title and About content to GX1 Video Forge while preserving MoneyPrinterTurbo attribution.
- Added `GX1_ACCESS_TOKEN` support for private operator mode on protected generation, upload, listing, detail, and delete APIs.
- Restricted default CORS behavior so production/Railway deployments do not fall back to wildcard origins.
- Added Railway deployment metadata and a `/healthz` endpoint.
- Set safer MVP queue defaults in `config.example.toml` (`max_concurrent_tasks = 1`, `max_queued_tasks = 5`).
- Added GXEON compliance, asset-safety, product-readiness, and audit documentation.
