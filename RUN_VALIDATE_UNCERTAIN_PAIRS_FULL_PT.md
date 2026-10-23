# Reproduzir a validação completa aceita

Resultado de 21/10/2026: **PASS**, 24.889 células, 49.778 linhas. A execução usa Python 3.10 ou mais recente e somente a biblioteca padrão.

A partir da raiz extraída do pacote:

```bash
python3 analysis/19b_validate_uncertain_pair_crosstab_v1.py \
  --scope full \
  --export-dir outputs/native/uncertain_pair_crosstab_v1/full \
  --pilot-validation outputs/validation/uncertain_pair_crosstab_v1/pilot/canonical_uncertain_pairs_pilot_v1_validation.json \
  --output-dir outputs/validation/uncertain_pair_crosstab_v1/full
```

A pasta de entrada contém os nove CSVs recebidos e a cópia exata do CSV sintético aceito no piloto. O piloto não precisa ser repetido. O validador foi preservado sem edições. Os produtos existentes são imutáveis: uma reexecução idêntica é aceita; produtos diferentes não são sobrescritos.

A saída esperada é `status: PASS`, `scope: full`, `cells: 24889`, `rows: 49778`, `native_fixtures_passed: 34` e `scientific_full_domain_complete: true`. Os logs da execução constam na pasta de validação completa. Essa reexecução é local e não inicia tarefas no GEE.
