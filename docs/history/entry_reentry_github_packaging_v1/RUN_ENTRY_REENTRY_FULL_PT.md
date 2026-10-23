# Reproduzir a validação completa aceita

**23/10/2026 — PASS.** Os 73 CSVs nativos já estão incluídos. Não é necessário repetir o GEE. A partir da raiz deste pacote, com Python 3.10 ou superior:

```bash
python3 analysis/20d_validate_entry_reentry_full_v1.py --scope full --export-dir outputs/native/entry_reentry_v1/full --output-dir outputs/validation/entry_reentry_v1/full
```

O validador autentica os arquivos críticos, revalida o piloto preservado e compara todos os registros completos. Não exige pacotes Python adicionais. Reexecução idêntica é aceita; saída diferente é recusada. Preserve a estrutura de diretórios. O relatório de aceitação permanece com os bytes originais gerados pelo validador.

As instruções originais de exportação estão preservadas abaixo para reprodução histórica.

---

# Execução completa de entrada/reentrada v1

## O que executar

Copie somente `gee/20c_export_entry_reentry_full_v1.js` para um novo script do GEE e clique Run uma vez, sem editar parâmetros. Use o mesmo acesso à cobertura, grade canônica e módulo de constantes do piloto r2 aceito. Não execute os scripts do piloto arquivado.

O script faz uma única consulta assíncrona aos metadados da cobertura, verifica as 41 bandas e as 41 projeções e então cria gradualmente 73 tarefas, cedendo o controle à interface entre tarefas. Aguarde a mensagem de criação completa antes de clicar Run novamente. Não há prévia de raster nem redução do domínio avaliada na Console.

## Tarefas e nomes

- `canonical_entry_reentry_1985_1990_b00_v1.csv` até `..._b07_v1.csv`, repetidos para cada intervalo 1985–1990, 1990–1995, 1995–2000, 2000–2005, 2005–2010, 2010–2015, 2015–2020 e 2020–2025: **64 tabelas**.
- `canonical_entry_reentry_history_audit_b00_v1.csv` até `..._b07_v1.csv`: **8 auditorias**.
- `canonical_entry_reentry_manifest_full_v1.csv`: **1 manifesto**.

Todos irão para a pasta Drive `entry_reentry_full_v1`. O identificador é `er1_full_20261021_full`, com versão de saída `entry-reentry-full-v1`. Preserve os nomes. O inventário exato, com quantidade de linhas por arquivo, está em `config/entry_reentry_full_expected_exports_v1.csv`.

| Lote | Células / linhas em cada intervalo | Linhas da auditoria do lote |
|---|---:|---:|
| b00 | 3.168 | 3.168 |
| b01 | 3.128 | 3.128 |
| b02 | 3.061 | 3.061 |
| b03 | 3.118 | 3.118 |
| b04 | 3.104 | 3.104 |
| b05 | 3.105 | 3.105 |
| b06 | 3.088 | 3.088 |
| b07 | 3.117 | 3.117 |
| Total | 24.889 por intervalo | 24.889 |

São 199.112 linhas de célula/intervalo e 24.889 linhas de auditoria, além da linha do manifesto. Inicie as tarefas por grupos e acompanhe as falhas. Não é necessário repetir o piloto ou seus testes sintéticos: o validador completo revalida os arquivos nativos aceitos que acompanham este pacote.

A exportação mantém cobertura `coverage_v3`, grade canônica, CRS e transformação, `tileScale: 16` e `maxPixelsPerRegion: 100000000`. Cada tarefa de dados reduz apenas um intervalo e um lote, com 22 bandas; o histórico completo tem tarefas próprias. Não há leitura do produto de idade de pastagem ou mudança da contabilidade.

## Devolver resultados

Aguarde os 73 arquivos estarem efetivamente no Drive. Exporte-os juntos em ZIP, com seus nomes originais, e envie o ZIP. A pasta de entrada da validação deve conter somente esses 73 CSVs. Arquivos do piloto, resultados de tentativas duplicadas e nomes com sufixos de cópia serão rejeitados pelo inventário.

## Validação local opcional

Pode apenas enviar os arquivos para validação aqui. Para validar por conta própria, extraia o pacote de implementação e coloque os 73 CSVs em `dados/entry_reentry_full_v1`. Execute a partir da raiz:

```bash
python3 analysis/20d_validate_entry_reentry_full_v1.py   --scope full   --export-dir dados/entry_reentry_full_v1   --output-dir outputs/validation/entry_reentry_v1/full
```

Requer Python 3.10 ou superior, sem dependências adicionais. As referências completas e o piloto aceito já acompanham o ZIP. Não mova arquivos isolados do pacote ao usar o validador, pois seus caminhos relativos e hashes são verificados.

A aceitação exige inventário completo, 24.889 células únicas em cada intervalo, atribuição exata aos lotes, 199.112 linhas de dados, 24.889 auditorias de 41 anos, parâmetros e projeções nativos, partições de origem e de entrada/reentrada, contadores de erro zero, preservação dos controles históricos e concordância com as quatro linhas e duas auditorias do piloto. As tolerâncias são 0,01 ha por célula e 0,001 ha nos agregados.

Os produtos incluem painel normalizado, oito resumos por intervalo, auditoria completa, controles históricos, comparação com o piloto, inventário e JSON de validação. O validador recusa sobrescrever resultados diferentes; reexecuções idênticas são aceitas.

## Referências e interpretação

A referência contém as 199.112 linhas da base 1985 do painel de sensibilidade previamente aceito. Preserva 49.778 linhas rotuladas como referências reaproveitadas e 149.334 de exportações nativas; seus controles de área são usados, sem criar contadores nativos fictícios para os registros históricos reaproveitados.

Se precisar reconstruir essas referências a partir do pacote de dados original já distribuído:

```bash
python3 analysis/20e_rebuild_entry_reentry_reference_v1.py   --source-data-zip /caminho/window_origin_sensitivity_full_data_v1.zip
```

O extrator verifica o hash exato do ZIP e do painel antes de reproduzir os dois CSVs de controle. As cópias prontas já incluídas são suficientes para a validação normal.

No primeiro intervalo, origem inicial é 100% do fluxo por construção e o componente pós-1985 em t0 é zero: proporções condicionais a esse componente ficam vazias, não zero ou 100%. Em todos os demais intervalos, primeira observada/reentrada/histórico anterior incerto subdividem somente o componente de entrada pós-1985. Primeira observada não significa primeira implantação histórica. O intervalo 2020–2025 permanece diagnóstico e somas entre intervalos não são áreas espaciais deduplicadas.

A implementação foi verificada localmente. A execução nativa completa e seus resultados científicos continuam pendentes; o pacote não apresenta resultados sintéticos como evidência do domínio.
