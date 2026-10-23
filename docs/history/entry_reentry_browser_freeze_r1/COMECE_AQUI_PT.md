# Próximo passo: piloto de primeira entrada observada e reentrada

O software foi verificado localmente. A execução e a aceitação nativas deste piloto ainda estão **pendentes**.

1. Abra `gee/20a_export_entry_reentry_pilot_v1.js` deste ZIP.
2. Copie o arquivo inteiro para o Code Editor do Google Earth Engine, no mesmo acesso aos assets e ao módulo `users/barroso2501/pasture-crop:lib/constants` usado anteriormente.
3. Clique **Run**, sem editar parâmetros. O script confere metadados das 41 bandas anuais antes de criar as tarefas; essa etapa inicial pode levar algum tempo.
4. Na aba **Tasks**, inicie as **quatro tarefas CSV**.
5. Aguarde as quatro terminarem e os quatro arquivos aparecerem efetivamente no Drive, pasta `entry_reentry_pilot_v1`.
6. Envie os quatro CSVs juntos, preferencialmente em um ZIP, preservando os nomes.

| Arquivo esperado | Linhas de dados |
|---|---:|
| `canonical_entry_reentry_pilot_v1.csv` | 4 |
| `canonical_entry_reentry_history_audit_pilot_v1.csv` | 2 |
| `canonical_entry_reentry_native_synthetic_v1.csv` | 31 |
| `canonical_entry_reentry_manifest_pilot_v1.csv` | 1 |

São as células GH-123 / 18081 / lote 1 e IK-77 / 32173 / lote 5, nos intervalos 2015–2020 e 2020–2025. O segundo permanece diagnóstico. A auditoria real acumula verificações de 1985 a 2025 e retém as áreas de entrada e término em 2024/2025 em campos próprios.

O script não altera assets, o piloto anterior, os pares incertos aceitos ou a contabilidade. Este é um novo namespace de exportação. As referências históricas necessárias para validar os resultados já estão no pacote; não precisa reenviá-las. Os arquivos `17g` e `18c` deste ZIP são referências históricas, não tarefas deste piloto.

Se houver falha, envie o nome da tarefa e a mensagem completa. Aguarde a validação deste piloto antes de ampliar o domínio. As instruções locais e os critérios estão em `RUN_ENTRY_REENTRY_PILOT_PT.md`.
