# Piloto entrada/reentrada — correção r2 do travamento

Esta revisão substitui o primeiro `20a`, que travou depois de Run. Ela remove as 42 consultas síncronas de metadados e faz a recorrência anual real e sintética com `ee.List.iterate` no servidor. A correção passou em testes locais; a execução no GEE e a aceitação nativa continuam pendentes.

1. Recarregue a aba do Earth Engine que ficou travada, ou abra uma nova aba.
2. Crie um script vazio e copie **todo** o conteúdo de `gee/20a_export_entry_reentry_pilot_v1.js` **deste novo ZIP**.
3. Clique **Run**, sem editar parâmetros. A primeira mensagem será `r2: consultando metadados de cobertura de forma assincrona`.
4. Aguarde a mensagem de metadados aprovados e depois `r2: QUATRO tarefas CSV criadas`.
5. Na aba **Tasks**, inicie as quatro tarefas. Os arquivos irão para **`entry_reentry_pilot_v1_r2`**, no Drive.
6. Aguarde os quatro arquivos serem efetivamente gravados e envie-os juntos em um ZIP.

| Arquivo | Linhas de dados esperadas |
|---|---:|
| `canonical_entry_reentry_pilot_v1.csv` | 4 |
| `canonical_entry_reentry_history_audit_pilot_v1.csv` | 2 |
| `canonical_entry_reentry_native_synthetic_v1.csv` | 31 |
| `canonical_entry_reentry_manifest_pilot_v1.csv` | 1 |

A pasta `gee/` contém **somente o arquivo que deve ser executado**. Os scripts históricos foram movidos para `docs/history/entry_reentry_browser_freeze_r1/gee/`.

As células, os dois intervalos, os 31 casos e todas as regras científicas são os mesmos. O identificador da execução recebeu o sufixo `_r2`; use os quatro CSVs da nova pasta, sem misturá-los com arquivos de tentativas anteriores. Use também o validador e as configurações deste ZIP.

Se aparecer erro em vermelho, envie a mensagem completa. Se a página voltar a travar, informe a última mensagem `r2:` que apareceu na Console. Ela permite distinguir a etapa de metadados, os dados reais e os testes sintéticos.
