# Cenara Product Blueprint

A Cenara é uma distribuição privada, manual-first, baseada no MoneyPrinterTurbo MIT para apoiar operadores na criação de vídeos curtos com IA.

## Escopo do MVP privado

- Geração assistida de roteiro, palavras-chave, seleção de fonte visual, voz IA, legendas e renderização de vídeo.
- Operação protegida por token privado antes de qualquer controle operacional da WebUI.
- Uso de provedores configurados pelo operador, como Pexels, Pixabay e Coverr para imagens/vídeos quando houver chaves disponíveis.
- Configuração de LLM e TTS pelo painel privado ou por variáveis do Railway.

## Fora do escopo nesta fase

- Billing, Hotmart, Stripe, Mercado Pago ou qualquer cobrança.
- Login SaaS público, multi-tenant ou banco de dados de usuários.
- Autopost público em redes sociais.
- Promessas de conversão garantida.

## Segurança e operação

As chaves devem ser mantidas em Railway Variables ou digitadas no painel privado quando necessário. Campos de chave não são pré-preenchidos com valores salvos; entradas vazias preservam a configuração existente.

## Railway

O deploy saudável no Railway deve continuar usando a configuração existente de porta, healthcheck e runtime. Esta documentação não altera `railway.json`, `Dockerfile` nem comandos de inicialização.

## Atribuição

Powered by GXEON · Based on MoneyPrinterTurbo MIT. A licença MIT original e o NOTICE devem ser preservados.

## Roadmap sugerido

1. Refinar presets por nicho e formato.
2. Criar biblioteca interna de templates de roteiro.
3. Adicionar checklist de qualidade antes da exportação.
4. Evoluir observabilidade operacional sem expor segredos.
