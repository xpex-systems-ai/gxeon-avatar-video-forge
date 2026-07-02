# Cenara real video troubleshooting

Cenara real generation no longer depends on an LLM quota to start the render pipeline.

## Local script and keyword fallback

When the lower real-generation form has no manual script, Cenara reuses the existing MoneyPrinterTurbo `video_script` field when it is safe. If that is blank or looks like a provider failure, Cenara builds a deterministic PT-BR ad script from tema, público, promessa, nicho and CTA. Keywords are taken from manual terms first, then existing `video_terms`, then deterministic safe terms derived locally from the brief and script.

## Provider failover

For external stock media, Cenara attempts the selected provider first, then configured Pexels, Pixabay and Coverr. The status file records only safe provider names and statuses, never raw provider responses or secrets.

## Local visual fallback MP4

If no external provider returns a usable current-task MP4, Cenara uses FFmpeg to create a truthful local visual fallback MP4 in the current task directory. The fallback is labeled as `fallback_video_used=true` and should not be described as stock footage.

## Strict MP4 gate

A generation is successful only after Cenara verifies a `.mp4` exists inside the current task directory, has non-zero size, and was created during the current task. Old MP4 files are not reused as success.

## MP4 gerou mas não abre

A geração, o preview e o download são camadas diferentes. A geração cria um arquivo `.mp4` em `storage`; a UI só entrega o vídeo depois de validar que o arquivo existe, não está vazio e está dentro da área segura de storage do projeto.

A Biblioteca agora renderiza controles de preview e download para cada MP4 verificado. Arquivos antigos continuam sendo tratados como Biblioteca e não como sucesso da geração atual.

Para evitar problemas de entrega de caminho local no Railway/Streamlit, o preview lê o MP4 em bytes e envia esses bytes para `st.video(..., format="video/mp4")`. O botão de download usa os mesmos bytes com MIME `video/mp4` e filename seguro.

Se um MP4 precisar de compatibilidade extra para navegadores, Cenara pode criar uma cópia irmã `.browser.mp4` com FFmpeg sem sobrescrever o original. Essa normalização usa H.264, `yuv420p`, `+faststart` e áudio AAC quando possível; se o áudio falhar, a cópia é recriada sem áudio.
