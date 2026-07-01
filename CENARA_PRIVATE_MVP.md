# Cenara Private MVP

## Private MVP status

Cenara is maintained as a private MVP branch on top of MoneyPrinterTurbo. This branch is intended for final human audit before merge and does not add public SaaS billing, Hotmart flows, Product Hunt material, or social autopost automation.

## Railway deployment variables

Railway deployments should provide secrets through Railway environment variables or mounted private configuration, not through committed files. Do not commit `config.toml`, `.env`, provider API keys, access tokens, or generated credentials.

Expected private MVP voice-provider configuration includes:

- ElevenLabs: saved API keys may be configured privately for the deployment.
- Chatterbox: self-hosted OpenAI-compatible base URL/model/voices may be configured privately, with an optional saved API key for protected deployments.

## Saved provider key handling

Saved ElevenLabs and Chatterbox API keys are never displayed or prefilled in the WebUI. When a saved key exists, the WebUI shows an empty password field with the placeholder `Saved key configured`; submitting the field blank preserves the saved private key, and entering a non-empty replacement updates the runtime configuration.

## Upstream attribution and license

Cenara preserves the upstream MoneyPrinterTurbo attribution and MIT License. The original MoneyPrinterTurbo project remains credited in the existing README files and application metadata, and this private MVP patch does not remove or replace that attribution.
