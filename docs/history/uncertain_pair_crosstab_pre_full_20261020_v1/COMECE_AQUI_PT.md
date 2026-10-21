# Próximo passo: pares incertos em domínio completo

A auditoria direcionada da idade v2 está encerrada. Agora vamos produzir a tabela que explica os pares incertos da cobertura, incluindo os casos que envolvem PAS. Esta análise usa apenas a cobertura e não exige migrar o asset de idade da contabilidade.

## Executar no GEE

1. Abra `gee/19a_export_uncertain_pair_crosstab_full_v1.js` deste pacote.
2. Copie todo o conteúdo para o Code Editor e clique **Run**, sem editar parâmetros.
3. Inicie as **nove tarefas**: oito lotes e um manifesto.
4. Aguarde os nove CSVs aparecerem efetivamente no Drive, pasta `uncertain_pair_crosstab_v1`.
5. Envie os nove CSVs juntos em um ZIP, preservando os nomes.

Arquivos esperados:

- `canonical_uncertain_pairs_b00_v1.csv` até `canonical_uncertain_pairs_b07_v1.csv`;
- `canonical_uncertain_pairs_manifest_full_v1.csv`.

Não repita o piloto: seus três arquivos e sua validação estão preservados neste pacote. Não repita os lotes da auditoria da idade. Se a execução completa já tiver sido feita, envie os arquivos existentes em vez de executar novamente. Se alguma tarefa falhar, envie nome e mensagem completa do erro.

## O que vamos verificar

São os pares anuais 2023→2024 e 2024→2025 em 24.889 células da grade canônica: **49.778 linhas**. É um domínio diferente das 21.869 células usadas na auditoria direcionada da idade. Cada endpoint é classificado como PAS, não PAS observado, NODATA, mascarado ou inesperado. A tabela cruza os 25 pares possíveis e distingue pares incertos com PAS no início, com PAS no fim e sem PAS observado.

A validação exigirá inventário completo, suporte e projeção nativos, partições consistentes, contadores de erro zero, reprodução dos totais históricos e consistência com o piloto aceito. Só depois interpretaremos a composição dos aproximadamente 4,69 Mha de área incerta. Nenhuma proporção de PAS nessa área foi estimada pelo piloto.

O script, o validador e as configurações são os mesmos já distribuídos e validados no piloto. Este pacote atualiza a organização das instruções e usa o README completo após o encerramento da auditoria da idade v2. A execução completa ainda está pendente de resultados; não há alteração da matriz v4.3/events-v5.

O detalhe de validação local está em `RUN_UNCERTAIN_PAIRS_FULL_PT.md`. Pode apenas enviar os nove CSVs e fazemos a validação aqui.
