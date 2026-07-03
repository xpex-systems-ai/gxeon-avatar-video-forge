# Cenara: solução de problemas de vídeo real

## MP4 gerou mas não abre

A geração do MP4, o preview no navegador e o download pelo Streamlit são camadas diferentes:

1. **Geração** cria um arquivo `.mp4` real em `storage/` ou `storage/tasks/`.
2. **Validação de entrega** confirma que o arquivo existe, não está vazio, tem extensão `.mp4` e está dentro do armazenamento permitido do projeto.
3. **Preview e download** carregam os bytes do MP4 validado e entregam esses bytes ao navegador via Streamlit.

Isso evita depender de caminhos locais do servidor, que podem falhar em ambientes como Railway depois de reruns, refreshes ou perda de `session_state`.

## Biblioteca com preview e download

A Biblioteca lista MP4s verificados encontrados em `storage/tasks` e `storage`. Por padrão, cada item mostra apenas metadados seguros para o operador: nome do arquivo, tamanho em MB, data de geração e status de verificação.

O preview e o botão **Baixar MP4** só são carregados depois que o operador clica em **Carregar preview e download** no item desejado. Isso evita leitura/transcodificação ansiosa de todos os MP4s da biblioteca a cada rerun do Streamlit.

Arquivos antigos continuam sendo biblioteca; eles não são tratados como sucesso da geração atual. Para validar uma tarefa atual, gere novamente e use o preview exibido para o task em execução. Os widgets de download usam chaves únicas por contexto de renderização, evitando colisões de IDs do Streamlit quando o mesmo MP4 aparece no Preview Real e na Biblioteca.

## Recuperação do Preview Real

Quando o estado de sessão perde o caminho do último MP4, o Preview Real procura automaticamente o MP4 seguro mais recente no armazenamento. Se encontrar, mostra a mensagem de recuperação e permite abrir/baixar o arquivo sem afirmar que ele pertence à geração atual.

## Normalização para compatibilidade com navegador

Se um MP4 não parecer compatível com browser, a Cenara pode criar uma cópia ao lado do arquivo original com o sufixo `.browser.mp4`. Essa cópia usa H.264, pixel format `yuv420p`, áudio AAC quando possível e `-movflags +faststart`. O original não é sobrescrito. Se a conversão com áudio falhar, a rotina tenta uma cópia sem áudio para preservar a entrega visual.

Para arquivos maiores que 150MB, o preview inline é evitado para reduzir risco de travamento no browser, mas o download continua disponível.

## Fallback local de roteiro e palavras-chave

A geração real da Cenara não depende de cota de LLM para iniciar o pipeline. Quando o formulário não recebe roteiro manual, a Cenara reaproveita o campo `video_script` existente se ele for seguro. Se estiver vazio ou parecer uma falha de provedor, ela cria um roteiro publicitário PT-BR determinístico a partir de tema, público, promessa, nicho e CTA. As palavras-chave vêm primeiro dos termos manuais, depois de `video_terms`, e por fim de termos seguros derivados localmente do briefing e roteiro.

## Failover de provedores

Para mídia externa, a Cenara tenta o provedor selecionado primeiro e depois os provedores configurados entre Pexels, Pixabay e Coverr. O arquivo de status registra apenas nomes e estados seguros dos provedores, nunca respostas brutas nem segredos.

## Fallback visual local em MP4

Se nenhum provedor externo retornar um MP4 utilizável para a tarefa atual, a Cenara usa FFmpeg para criar um MP4 visual local verdadeiro dentro do diretório da tarefa atual. Esse fallback é marcado como `fallback_video_used=true` e não deve ser descrito como stock footage.

## Gate estrito de MP4

Uma geração só é sucesso depois que a Cenara verifica que existe um `.mp4` dentro do diretório da tarefa atual, com tamanho maior que zero, e criado durante a tarefa atual. MP4s antigos não são reutilizados como sucesso da tarefa atual.

## MP4 existe mas não abre no navegador

Quando um MP4 verificado aparece na Cenara, isso significa apenas que a camada de **geração** criou um arquivo real e não vazio dentro do armazenamento seguro. A entrega ao usuário continua separada em duas etapas independentes:

- **Sucesso de geração (`mp4_created`)**: existe um `.mp4` novo, não vazio e aprovado pelo gate seguro da tarefa atual.
- **Falha de preview (`mp4_created_preview_failed`)**: o MP4 continua válido, mas o navegador/Streamlit não conseguiu renderizar o player inline naquele rerun. Use **Baixar MP4**; isso não apaga nem invalida o arquivo gerado.
- **Download pronto (`download_ready`)**: o botão recebeu bytes do MP4 validado e pode entregar o arquivo ao operador. Se o preparo do download falhar, a UI mostra um aviso sem transformar a geração em falha.

Para reduzir erros de frontend como `removeChild`/`NotFoundError`, a Cenara renderiza apenas **um player ativo** por padrão na área **Preview Real**. A **Biblioteca** é lazy: ela lista cards leves com data, tamanho, task de origem e status, mas não cria players de vídeo dentro dos cards. O botão **Abrir na prévia** grava a seleção segura no `session_state` e recarrega a área única de preview; o botão **Baixar MP4** usa chaves estáveis por contexto e fingerprint seguro, sem expor caminhos absolutos do servidor.

### Seleção explícita da Biblioteca e status de entrega

A partir da correção da PR #26, **Abrir na prévia** respeita o item escolhido na Biblioteca quando o arquivo selecionado ainda passa pelo gate seguro de MP4. A área **Preview Real** usa a seleção explícita antes de considerar o MP4 da geração atual e só usa o MP4 mais recente como fallback visual quando não há seleção segura.

Os status também representam camadas diferentes:

- `mp4_created=true` confirma geração: um MP4 real, não vazio e seguro existe para a tarefa.
- `preview_ready=true` só deve aparecer depois que a camada Streamlit conseguir montar o player `st.video` sem erro.
- `download_ready=true` só deve aparecer depois que os bytes do MP4 forem lidos e o botão de download for preparado.
- `mp4_created_preview_failed=true` indica que o MP4 continua válido, mas o navegador não recebeu o preview inline naquele rerun. Se o download estiver pronto, a geração permanece válida e o operador deve baixar o arquivo.
