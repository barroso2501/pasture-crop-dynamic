# Reproduzir a incorporação científica de RQ2 v4.4

Use este pacote incremental sobre o repositório que já contém os dados e o código completos da etapa de entrada/reentrada. Python 3.10 ou mais recente; Matplotlib apenas para os gráficos. Não é necessário repetir o GEE. Na raiz do repositório:

```bash
python analysis/20g_integrate_rq2_entry_reentry_v4_4.py
python analysis/test_rq2_entry_reentry_v4_4.py
python analysis/20h_plot_entry_reentry_v4_4.py
python analysis/20i_validate_rq2_entry_reentry_v4_4.py
```

Os novos dados e a matriz têm escrita imutável: saídas existentes só são aceitas se os bytes forem idênticos. O script de figura recria PNG/SVG/PDF com metadados de data removidos. O validador autentica as versões anteriores, os 73 CSVs nativos, os arquivos críticos originais, os seis produtos derivados originais (lendo o painel grande diretamente do gzip), os documentos e a nova implementação. Reagrega de forma independente os 199.112 registros nativos e reconfere os contadores das 24.889 auditorias, sem nova computação remota.

O resultado esperado é `status: PASS`, 35 achados, apenas P9A035/P9A036 com adições substantivas, 33 preservados, 12 eventos anteriores preservados byte por byte e dois acrescentados. As frações usam denominadores explícitos. O primeiro intervalo tem frações condicionais em branco, e 2020–2025 permanece diagnóstico. Não são estimadas área única entre intervalos, taxa de exposição, hazard ou causalidade.

Saídas: `outputs/summary/rq2_entry_reentry_v4_4/`, `outputs/validation/rq2_entry_reentry_v4_4/`, `figures/rq2_entry_reentry_v4_4/`. O relatório nativo original e seus hashes permanecem inalterados. A nova validação é de incorporação descritiva e preservação; não renomeia uma execução de software como nova execução GEE.

A garantia da idade 201 é da idade auxiliar reconstruída da cobertura. A auditoria completa da idade numérica do asset público e o desenho amostral de pixels proposto no protocolo histórico não são declarados executados. O status atual está em `config/plan009_followup_status_20261023_v1.json`.
