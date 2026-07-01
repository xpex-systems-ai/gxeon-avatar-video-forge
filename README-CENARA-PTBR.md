# Cenara MVP privado

Cenara é uma adaptação privada operacional do MoneyPrinterTurbo para geração assistida de vídeos curtos. A marca pública do produto é **Cenara**; a interface exibe discretamente **Powered by GXEON**.

## Segurança do MVP

- Este PR consolida um **MVP privado apenas para operadores**. Não é um SaaS público pronto.
- Configure `GX1_ACCESS_TOKEN` para proteger API e WebUI em produção/Railway. O nome da variável é mantido por compatibilidade; ela não define a marca pública do produto.
- Envie o token por `x-api-key` ou `Authorization: Bearer <token>`.
- Configure `CORS_ALLOWED_ORIGINS` em produção/Railway. Sem essa configuração, nenhuma origem de browser é liberada por padrão.
- O mount estático `/tasks` é protegido por token, mas **não é seguro para exposição pública a clientes**. Use apenas para revisão privada de operadores.

## Endpoints protegidos

`/videos`, `/subtitle`, `/audio`, `/scripts`, `/terms`, `/social-metadata`, `/tasks`, `/tasks/{task_id}`, `DELETE /tasks/{task_id}`, `/musics`, `/video_materials`, `/stream`, `/download` e arquivos estáticos em `/tasks` exigem o token de operador.

## Atribuição

Cenara preserva a atribuição MIT do projeto upstream MoneyPrinterTurbo. Consulte `LICENSE`, `NOTICE`, `README.md` e `README-en.md`.
