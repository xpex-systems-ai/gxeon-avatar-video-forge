# GX1 Video Forge — MVP privado GXEON

GX1 Video Forge é uma versão privada e auditável do MoneyPrinterTurbo adaptada para o fluxo interno da GXEON/GX1. O objetivo do MVP é transformar ideias, textos e diagramas em vídeos curtos com roteiro, voz, legendas e montagem final.

> Status: MVP privado. Não é um estúdio completo de avatar e não deve ser vendido como SaaS público antes da revisão de segurança, direitos de uso e qualidade.

## Para quem

- Gestores de tráfego
- Agências
- Afiliados
- Donos de loja
- Infoprodutores
- Equipes internas da GXEON que precisam explicar diagramas, processos e ofertas

## Fluxo principal

1. Ideia, texto ou diagrama: o operador define o conceito e os pontos que precisam aparecer.
2. Roteiro: o sistema ajuda a transformar o briefing em script curto.
3. Voz: o operador escolhe o provedor/voz configurado e gera narração.
4. Legendas: o vídeo recebe legendas para consumo em redes sociais e anúncios.
5. Vídeo: os materiais visuais são combinados com áudio, legenda e música segura.
6. Revisão manual: o operador valida fatos, direitos de uso, qualidade, claims e adequação ao público.

## Workflow manual-first para diagramas GXEON

1. Exportar o diagrama em imagem ou descrever os blocos em texto.
2. Escrever o objetivo do vídeo: explicar, vender, treinar ou resumir.
3. Criar um roteiro em linguagem simples com abertura, problema, mecanismo, exemplo e CTA.
4. Selecionar materiais próprios ou comercialmente liberados.
5. Gerar áudio e legendas.
6. Montar o vídeo e revisar manualmente antes de publicar.

## Segurança operacional

Antes de expor qualquer domínio público, configure `GX1_ACCESS_TOKEN`. Chamadas protegidas aceitam o header `x-gx1-access-token` ou `Authorization: Bearer <token>`.

Não gere domínio público nem compartilhe endpoints de upload, deleção, listagem ou geração sem token configurado.

## Deploy Railway

- Porta alvo: `8501`
- Healthcheck: `/healthz`
- Variáveis obrigatórias antes de exposição pública: `GX1_ACCESS_TOKEN`, `CORS_ALLOWED_ORIGINS`
- Defaults recomendados de MVP: `max_concurrent_tasks = 1`, `max_queued_tasks = 5`

## Atribuição

GX1 Video Forge é baseado no MoneyPrinterTurbo por Harry, sob licença MIT. Veja `LICENSE`, `NOTICE.md` e `THIRD_PARTY_LICENSES.md`.
