# Cenara Private MVP Railway Release Guard

Cenara is a GXEON-branded private MVP distribution based on MoneyPrinterTurbo for protected internal/operator use only.

## Railway deployment requirements

Before generating or assigning a Railway public domain, configure all of the following Railway variables:

- `ENVIRONMENT=production` — required for the Railway deployment profile.
- `GX1_ACCESS_TOKEN=<strong private operator token>` — required before public exposure.

If `GX1_ACCESS_TOKEN` is missing and `config.app["api_key"]` is also empty, the app/API must fail closed. API requests and `/tasks` media access must return `401` until an expected operator token is configured.

## Private MVP boundaries

This release is private MVP only:

- No Hotmart integration.
- No billing flow.
- No SaaS public login.
- No autoposting workflow.

## Attribution

Cenara preserves upstream MoneyPrinterTurbo attribution and the MIT License. It is a branded private distribution, not a from-zero rewrite.
