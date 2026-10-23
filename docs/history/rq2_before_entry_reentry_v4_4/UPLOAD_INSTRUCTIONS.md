# Subir o registro completo pelo navegador do GitHub

**23/10/2026. Os resultados continuam aceitos (PASS). Esta edição muda apenas o empacotamento.**

## Instalação

1. Baixe `entry_reentry_github_parte1_v1.zip` e `entry_reentry_github_parte2_v1.zip`.
2. Extraia os dois ZIPs na mesma pasta local, mesclando as pastas com o mesmo nome. São ZIPs independentes; não precisam ser concatenados.
3. Envie ao repositório o conteúdo extraído, preservando as pastas. O GitHub não extrai ZIPs automaticamente. Cada arquivo para envio tem menos de 25 MB; cada ZIP de entrega também tem menos de 25 MB.
4. Faça os envios em grupos de até 100 arquivos. Por exemplo: arquivos da raiz; depois `analysis`, `config`, `gee`, `docs`, `tests`, `provenance`; por fim `outputs/native` e `outputs/validation` separadamente e `data`. Subdivida qualquer pasta caso a seleção ultrapasse 100 arquivos.

O arquivo `canonical_entry_reentry_full_v1_cells.csv` foi substituído, para transporte e versionamento, por `data/entry_reentry_full_v1/canonical_entry_reentry_full_v1_cells.csv.gz`. O CSV completo é restaurado byte por byte pelo comando abaixo. Os CSVs nativos, os relatórios de aceitação, os demais produtos e os arquivos críticos do código/piloto mantêm seus bytes originais. Uma cópia temporária incompleta que havia entrado no ZIP anterior foi retirada; ela não é produto de validação.

## Reproduzir a validação

Faça esta etapa em uma cópia local ou no Colab, depois de extrair ambas as partes. Use Python 3.10 ou superior, na raiz do pacote:

```bash
python analysis/restore_entry_reentry_large_csv_v1.py
python analysis/20d_validate_entry_reentry_full_v1.py --scope full --export-dir outputs/native/entry_reentry_v1/full --output-dir outputs/validation/entry_reentry_v1/full
```

No Colab/Linux também pode usar `python3`. A restauração confere tamanho e SHA256, aceita arquivo já idêntico e recusa sobrescrever um arquivo diferente. Depois de restaurar, mantenha o CSV grande apenas no ambiente de análise; no GitHub permanece a cópia `.csv.gz`. As regras em `.gitignore` tratam apenas desse painel restaurado ao usar Git local; pelo navegador selecione a cópia comprimida para envio.

Não precisa restaurar ou executar nada para consultar os resumos e relatórios. Não é necessário repetir o GEE. O JSON PASS original permanece inalterado; ele registra o hash do CSV descomprimido, que o restaurador reproduz exatamente.

O inventário `PACKAGE_SHA256.csv` descreve os arquivos de distribuição, incluindo a cópia gzip. O manifesto `config/entry_reentry_github_packaging_v1.json` relaciona os hashes comprimido e descomprimido. O inventário e as instruções da edição anterior estão preservados em `docs/history/entry_reentry_github_packaging_v1/`.

Resultados e limites científicos: `docs/results/entry_reentry_full_findings_v1.md`. Aceitação: `docs/validation/entry_reentry_full_acceptance_v1.md`. Matriz v4.3/events-v5 permanecem inalteradas.

Limites do GitHub pelo navegador: https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
