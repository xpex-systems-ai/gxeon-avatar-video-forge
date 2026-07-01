# Cenara Private MVP Railway Release

This release prepares a private, manual-first Railway deployment for Cenara review.

## Required Railway variables before exposing a public domain

- `GX1_ACCESS_TOKEN`: required strong random operator token. Do not commit it.
- `ENVIRONMENT=production`: enables production safety checks.
- `CORS_ALLOWED_ORIGINS`: optional for private UI review; when set in production, use exact origins only and never `*`.

## Safety posture

- API routes for video and LLM generation require the private token.
- The Streamlit interface stops at the private operator gate before rendering generation controls.
- `/tasks` media is protected by the same token middleware.
- Provider keys are not prefilled into sensitive WebUI password inputs.
- Hotmart, billing, SaaS login, Product Hunt material, and autopost flows are intentionally out of scope.
