# Execução completa: primeira entrada observada e reentrada

O piloto r2 foi aceito e está preservado. Agora execute **apenas**:

**`gee/20c_export_entry_reentry_full_v1.js`**

1. Abra um script vazio no Code Editor do GEE e copie o arquivo inteiro, sem editar parâmetros.
2. Clique **Run uma vez**. Aguarde a consulta assíncrona e a criação gradual até a mensagem **`COMPLETO: 73 tarefas criadas`**. As tarefas surgem aos poucos para manter o editor responsivo.
3. Na aba **Tasks**, inicie as tarefas por grupos. Pode começar pelos oito lotes de 1985–1990 e seguir os intervalos em ordem; depois conclua as oito auditorias e o manifesto.
4. Aguarde todas terminarem e os **73 CSVs** serem efetivamente gravados no Drive, pasta **`entry_reentry_full_v1`**.
5. Envie os **73 CSVs novos juntos em um ZIP**, preservando os nomes. A lista completa está em `config/entry_reentry_full_expected_exports_v1.csv`.

| Tipo de arquivo | Quantidade | Linhas de dados no conjunto |
|---|---:|---:|
| Tabelas de células: oito intervalos × oito lotes | 64 | 199.112 |
| Auditorias do histórico de 1985–2025: uma por lote | 8 | 24.889 |
| Manifesto completo | 1 | 1 |
| Total de CSVs novos | **73** | **224.002** |

O domínio contém **24.889 células**. O intervalo 2020–2025 continua diagnóstico. Os quatro CSVs e os 31 testes sintéticos nativos do piloto já estão preservados neste pacote: **não repita o piloto nem inclua seus arquivos na pasta dos 73 CSVs novos**.

A pasta `gee/` deste ZIP contém somente o `20c` que deve ser executado. O piloto e seu código estão arquivados em `provenance/entry_reentry_pilot_r2/`; não são tarefas desta etapa.

Se uma tarefa falhar, envie seu nome e a mensagem completa. Se a criação das tarefas for interrompida, envie a última mensagem da Console. Não altere escala, projeção ou classes para contornar falhas. As instruções completas e a validação opcional estão em `RUN_ENTRY_REENTRY_FULL_PT.md`.
