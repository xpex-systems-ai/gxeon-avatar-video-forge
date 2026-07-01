# Cenara — status de auditoria do MVP privado

Cenara é uma revisão privada de MVP sobre o upstream MoneyPrinterTurbo, com apoio discreto Powered by GXEON e mantendo a atribuição e a licença MIT originais do projeto. Esta versão não é um produto público, não adiciona cobrança SaaS, login de clientes, autoposting ou integrações comerciais novas.

## Polimento de segurança de chaves

- As chaves de provedores de vídeo (Pexels, Pixabay e Coverr) aparecem mascaradas no WebUI, inclusive em campos de configuração e gerenciamento; a seleção para exclusão usa o rótulo mascarado, mas preserva internamente a chave original correta para remover.
- As chaves salvas de voz (ElevenLabs e Chatterbox) não são exibidas em texto claro: os campos permanecem visualmente em branco com placeholder mascarado.
- Ao deixar o campo de ElevenLabs ou Chatterbox em branco, a chave salva é preservada e não é sobrescrita por string vazia. O cache de vozes do ElevenLabs só é limpo quando uma nova chave não vazia diferente da salva é enviada.
- Para autenticação operacional da API, `GX1_ACCESS_TOKEN` tem preferência quando definido no ambiente; `config.app['api_key']` permanece apenas como fallback local compatível com o upstream.
