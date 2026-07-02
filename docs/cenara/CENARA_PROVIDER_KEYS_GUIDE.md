# Cenara Provider Keys Guide

Este guia orienta o operador a configurar provedores sem expor chaves reais no repositório.

## Onde configurar

- Preferencial: Railway Variables para produção.
- Alternativo: painel privado Cenara, após desbloquear com `GX1_ACCESS_TOKEN`.

## Fontes visuais

- Pexels: https://www.pexels.com/api/
- Pixabay: https://pixabay.com/api/docs/
- Coverr: https://coverr.co/api

A Cenara mostra apenas o status `Configurado` ou `Não configurado`. O valor salvo nunca deve ser revelado no campo de texto.

## LLM e TTS

Configure o provedor de LLM e TTS conforme a necessidade do operador. Para ElevenLabs e Chatterbox, os campos de API key permanecem vazios por padrão; digite uma nova chave somente para atualizar a sessão/configuração.

## Regras de segurança

- Nunca commitar chaves reais.
- Não compartilhar prints contendo secrets.
- Não validar chaves chamando APIs externas durante testes de UI.
- Se um campo de chave estiver vazio, a configuração existente deve ser preservada.
