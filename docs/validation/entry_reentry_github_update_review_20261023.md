# Revisão da atualização do GitHub — 23/10/2026

Repositório: https://github.com/barroso2501/pasture-crop-dynamic

Branch `main`; commit examinado: `64c4618c56619fb30e12657e6810c371bb3a6fd7`, registrado em 23/10/2026 às 15:34:56 (-03:00).

## Conclusão

A atualização publicada está **parcialmente completa** em relação aos dois pacotes `entry_reentry_github_parte1_v1.zip` e `entry_reentry_github_parte2_v1.zip`. Dos 241 arquivos esperados, 225 têm os bytes exatos, 15 estão ausentes e o README corresponde à edição anterior de aceitação, anterior às instruções de compactação. A ciência e a validação publicada estão preservadas.

| Conferência | Resultado |
|---|---|
| Arquivos esperados idênticos | 225 / 241 |
| Arquivos críticos autenticados pelo snapshot completo | 91 / 91, sem diferenças |
| CSVs nativos da execução completa | 73 / 73, bytes idênticos |
| Relatório PASS publicado | Idêntico ao aceito |
| Cinco CSVs derivados presentes | Idênticos ao aceito |
| Painel consolidado grande | Ausente, inclusive a cópia `.csv.gz` esperada |
| Reprodução local a partir do clone | PASS, 24.889 células e 199.112 registros |
| Comparação após reprodução | Todos os seis CSVs e JSON reproduzem os hashes/bytes aceitos |

A reprodução usou o `20d` publicado e os dados publicados, com saídas locais separadas. O painel grande foi regenerado com seu hash aceito, sem adicionar dados externos à execução. Isso confirma que a ausência da cópia comprimida não impede recalcular o produto a partir dos inputs presentes; ela impede obter pelo caminho de restauração previsto no pacote.

## Arquivos ausentes

- `.gitignore`
- `COMECE_AQUI_PT.md`
- `PACKAGE_SHA256.csv`
- `RESULTADO_E_PROXIMO_PASSO_PT.md`
- `RUN_ENTRY_REENTRY_FULL_PT.md`
- `SUBIR_NO_GITHUB_PT.md`
- `UPLOAD_INSTRUCTIONS.md`
- `analysis/restore_entry_reentry_large_csv_v1.py`
- `config/entry_reentry_github_packaging_v1.json`
- `docs/history/entry_reentry_github_packaging_v1/COMECE_AQUI_PT.md`
- `docs/history/entry_reentry_github_packaging_v1/PACKAGE_SHA256.csv`
- `docs/history/entry_reentry_github_packaging_v1/README.md`
- `docs/history/entry_reentry_github_packaging_v1/RUN_ENTRY_REENTRY_FULL_PT.md`
- `docs/history/entry_reentry_github_packaging_v1/UPLOAD_INSTRUCTIONS.md`
- `data/entry_reentry_full_v1/canonical_entry_reentry_full_v1_cells.csv.gz`

Também precisa ser substituído `README.md` pela edição fornecida no pacote para GitHub. O README publicado já informa a aceitação científica completa, mas ainda não contém o aviso do empacotamento comprimido.

## Links e complemento

Foram encontrados cinco destinos locais ausentes no README. Três pertencem aos 15 arquivos acima: `RESULTADO_E_PROXIMO_PASSO_PT.md`, `RUN_ENTRY_REENTRY_FULL_PT.md` e `UPLOAD_INSTRUCTIONS.md`. Dois são instruções de etapas anteriores: `RUN_REPRODUCE_PT.md` e `RUN_VALIDATE_UNCERTAIN_PAIRS_FULL_PT.md`. Este complemento recupera essas duas instruções a partir dos registros aceitos locais; o primeiro recebe um aviso datado para qualificar o estado histórico de 12/10/2026.

`entry_reentry_github_complemento_v1.zip` inclui somente os 16 arquivos da correção esperada, as duas instruções recuperadas, este registro e um inventário do complemento. A aplicação local simulada fornece correspondência exata a todos os 241 arquivos esperados e resolve os cinco links locais ausentes do README. Os demais arquivos do repositório não são candidatos a exclusão por estarem fora do inventário desta atualização incremental.

Extraia o ZIP e envie seu conteúdo para a raiz do repositório, preservando os caminhos. Substitua o README. O ZIP e cada arquivo interno estão abaixo de 25 MB. O painel permanece em `.csv.gz`; o restaurador confere seu hash descomprimido. Não é necessário repetir o GEE.

## Escopo

A revisão cobre a atualização de entrada/reentrada, a sua reprodução e os links locais do README. Não é uma revisão integral das 661 outras entradas do repositório, nem uma validação nova das análises de fases anteriores. Nenhuma alteração foi enviada automaticamente ao GitHub. A matriz v4.3/events-v5 e as qualificações de autoria da execução remota permanecem inalteradas. A observação refere-se ao commit identificado; uploads posteriores precisam de nova conferência.
