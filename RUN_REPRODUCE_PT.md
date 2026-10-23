> **Atualização de contexto em 23/10/2026:** este documento preserva as instruções da sensibilidade aceitas em 12/10/2026. Desde então, o cruzamento de pares incertos, a decomposição entrada/reentrada e a idade auxiliar 201 também foram aceitos em suas etapas completas. O depósito público/DOI continua separado. Para a etapa atual, veja `RUN_ENTRY_REENTRY_FULL_PT.md`.

# Sensibilidade da janela — entrega e reprodução

**Status em 2026-10-12:** piloto nativo e validação completa PASS. A análise descritiva da sensibilidade está concluída; não é necessário rodar novas tarefas no GEE para esta etapa.

## Pacote compacto do GitHub

Extraia `window_origin_sensitivity_full_record_v1.zip` na raiz do repositório, preservando as pastas. Ele contém o README completo atualizado, método v2, registro de validação, achados, adendo de execução ao plano 009, gráficos PNG/SVG/PDF, código, configurações, o JSON de validação completa, os cinco CSVs de resumo originais e tabelas adicionais de revisão. Copie os arquivos para o GitHub como nas atualizações anteriores. Documentos históricos e matriz v4.1 permanecem preservados.

O inventário `GITHUB_PACKAGE_MANIFEST.csv` identifica o conteúdo do pacote compacto. `config/window_origin_sensitivity_full_input_inventory_v1.csv` identifica os inputs por hash. O inventário de dados externos e o JSON do pacote de dados registram o painel grande e os CSVs nativos.

## Pacote externo de dados

Extraia `window_origin_sensitivity_full_data_v1.zip` na pasta `Trabalho/Contabilidade` do projeto, preservando a árvore `spatial/`. Confira arquivos já existentes antes de substituir versões diferentes. Os resultados originais da validação completa ficam em:

```text
spatial/phase9/window_origin_sensitivity_v1/full/
```

O painel grande tem 472.891 linhas. A pasta `full/raw/` contém os 49 CSVs completos enviados e os três CSVs originais do piloto. O JSON PASS e o painel normalizado do piloto estão em `pilot/`. O pacote de dados deve ficar fora da atualização compacta do GitHub e pode integrar o futuro depósito público. Não foi criado DOI.

Os oito CSVs de referência aceitos continuam na pasta existente:

```text
spatial/phase9/pasture_spell_closure_full_v1/
```

## Reproduzir a validação

Na raiz do código extraído, usando o caminho local da pasta de dados:

```bash
python analysis/18d_validate_window_origin_sensitivity_v1.py \
  --scope full \
  --export-dir /CAMINHO/Contabilidade/spatial/phase9/window_origin_sensitivity_v1/full/raw \
  --reference-dir /CAMINHO/Contabilidade/spatial/phase9/pasture_spell_closure_full_v1 \
  --pilot-validation /CAMINHO/Contabilidade/spatial/phase9/window_origin_sensitivity_v1/pilot/pilot_window_origin_sensitivity_validation_v1.json \
  --output-dir /CAMINHO/Contabilidade/spatial/phase9/window_origin_sensitivity_v1/full
```

O resultado esperado é **FULL VALIDATION PASS**, com 423.113 linhas novas, 49.778 reutilizadas e 472.891 normalizadas. O validador exige os mesmos hashes de configuração, testes nativos, referências e snapshot fornecido. Saídas existentes só são reutilizadas se os bytes forem iguais. A chamada não acrescenta uma declaração de hash do texto executado pelo operador; o registro desta entrega mantém esse campo null.

## Reproduzir os gráficos

Instale as dependências listadas em `analysis/requirements_window_sensitivity_review_v1.txt` e execute:

```bash
python analysis/18f_plot_window_origin_sensitivity_v1.py
```

O gráfico usa exclusivamente o resumo intervalar validado já incluído no pacote compacto. Não exige rasters nem o painel grande.

## Escopo encerrado e itens independentes

A sensibilidade compara as três janelas por calendário comum e por 20 anos de acompanhamento, com 2020–2025 separado como diagnóstico. Ela reforça a interpretação condicionada pela janela e não estima uma fração de artefato, estacionariedade ou limiar do processo. Primeira entrada versus reentrada, idade auxiliar 201, cruzamento dos pixels incertos e depósito público com DOI são itens independentes ainda não executados. Sua necessidade depende das afirmações pretendidas no manuscrito ou do release.
