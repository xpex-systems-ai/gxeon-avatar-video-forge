# Cenara Private MVP — Railway Release Notes

Cenara is a private operator MVP built on the upstream MoneyPrinterTurbo project under the MIT License. Keep the upstream MIT license, attribution, and NOTICE requirements intact for every private Railway deployment.

## Private scope

This release remains a private MVP only:

- No Hotmart integration.
- No billing or public subscription flow.
- No public SaaS login.
- No autoposting automation.

## Railway deployment gate order

Do not generate or expose the Railway public domain until `GX1_ACCESS_TOKEN` is configured for the service. The private deployment must fail closed before the service receives public traffic.

Required Railway variables:

- `ENVIRONMENT=production`
- `GX1_ACCESS_TOKEN=<private operator token>`
- `CORS_ALLOWED_ORIGINS=<explicit Cenara WebUI/API origins>` when browser access needs cross-origin API calls

Railway runtime variables such as `RAILWAY_ENVIRONMENT`, `RAILWAY_PROJECT_ID`, or `RAILWAY_SERVICE_ID` are treated as production-like signals even if `ENVIRONMENT` is missing.

## API CORS behavior

CORS no longer falls back to a wildcard in Railway or production-like runtimes. If `CORS_ALLOWED_ORIGINS` is empty while `ENVIRONMENT=production`, `ENVIRONMENT=railway`, `ENVIRONMENT=prod`, or Railway runtime variables are present, the API uses an empty CORS origin list instead of `*`.

Wildcard CORS is only for explicit local development outside Railway/production-like runtime detection.

## Streamlit WebUI private gate

The Cenara Streamlit WebUI has a private operator gate that appears immediately after the Cenara title/language header and before Basic Settings or any sensitive controls.

The gate activates when `ENVIRONMENT` is `production`, `railway`, or `prod`, or when Railway runtime variables are present. The expected token prefers `GX1_ACCESS_TOKEN` and falls back to `config.app["api_key"]`. If no expected token exists in production-like runtime, the WebUI stops closed and instructs the operator to configure `GX1_ACCESS_TOKEN` before exposing Railway.

## Saved provider key safety

Saved ElevenLabs and Chatterbox keys are not displayed or prefilled in the WebUI. Their inputs render as password fields with an empty value; when a saved key exists, the placeholder says `Saved key configured`.

Submitting a blank ElevenLabs or Chatterbox key preserves the saved key. ElevenLabs voice-cache entries are cleared only when a non-empty newly submitted key differs from the saved key.

## Attribution

Cenara preserves MoneyPrinterTurbo upstream attribution and MIT License obligations. Do not remove the MoneyPrinterTurbo license, attribution, or NOTICE materials while preparing this private MVP.
