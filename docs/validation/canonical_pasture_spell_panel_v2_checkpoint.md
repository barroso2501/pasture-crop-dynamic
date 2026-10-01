# Checkpoint de validação dos painéis corrigidos de episódios de pastagem v2

**Estado:** PASS para o critério 9 da Decisão 024; remediação completa ainda pendente.  
**Escopo:** painel de estoque e fluxos, métricas derivadas e painel integrado, 1985–2025.  
**Execução:** `analysis/17p_build_corrected_pasture_spell_panels_v2.py` no Colab, 1º de outubro de 2026.

## Resultado aceito neste checkpoint

O processamento autenticou os painéis v1 e a verificação 17o, incorporou os oito arquivos de origem e destino validados e escreveu três Parquets v2. Cada painel contém 199.112 linhas, correspondentes a 24.889 células em oito intervalos. O intervalo 2020–2025 permanece incluído e sinalizado como diagnóstico.

Os nove campos legados de partição PAS→TMP baseada no asset de idade foram removidos dos painéis v2. A partição de origem reconstruída, os destinos observados, as perdas de observação e as participações PAS→TMP foram inseridos como novos campos. O JSON de validação registra `nonorigin_fields_preserved_exactly = true`, resíduo máximo da identidade de origem de `1.4552e-11` ha por célula e diferença máxima dos totais PAS frente à fonte v1 de `3.2547e-6` ha por célula. A verificação 17o havia confirmado a cadeia de campos não dependentes de origem entre painel, métricas derivadas, integração e entrada espacial; o 17p comparou explicitamente os campos preservados nas versões v1 e v2.

| Produto | Local no Drive | SHA-256 registrado na validação |
| --- | --- | --- |
| Painel v2 | `Trabalho/Contabilidade/panel/canonical_stock_flow_panel_1985_2025_v2.parquet` | `ef3589be99e3a2cdc1c2245a15cedd090c8255775b34f14d4f2f27d3f9f8faa7` |
| Métricas derivadas v2 | `Trabalho/Contabilidade/analysis/canonical_stock_flow_derived_metrics_1985_2025_v2.parquet` | `e4a17ba21640704e2f7db7a9885417a403b842910624f36f7f9da34bfd67a9c2` |
| Painel integrado v2 | `Trabalho/Contabilidade/analysis/canonical_integrated_stock_flow_trajectory_1985_2025_v2.parquet` | `06127aac2f67a34ed79118f666a9c00063e28f32f16a046901370c0336b98499` |

Os Parquets não acompanharam o pacote compacto de revisão. Seus hashes acima são declarações verificadas pelo script após a gravação, mas não foram recalculados nesta revisão independente. Os hashes dos dois CSVs anexos conferem exatamente com o JSON; o hash da validação 17o referenciada pelo 17p também confere com o arquivo anteriormente recebido.

## Reconciliação independente dos resumos

As somas dos oito registros do resumo por intervalo reproduzem exatamente, na precisão serializada, as duas janelas do resumo agregado. As áreas de origem inicial, nova e não resolvida fecham o fluxo PAS→TMP em cada intervalo, com maior resíduo absoluto de `2.9672e-6` ha no total de um intervalo. As participações foram recalculadas a partir das áreas agregadas e coincidem com os CSVs.

| Janela | PAS→TMP (ha) | Origem inicial | Origem nova | Origem não resolvida |
| --- | ---: | ---: | ---: | ---: |
| Primária, 1985–2020 | 20.119.468,098572 | 46,909899% | 53,089790% | 0,000311% |
| Observada, 1985–2025 | 22.205.794,848602 | 44,392464% | 55,607213% | 0,000323% |

As diferenças de milionésimos de hectare frente ao resumo RQ2 anterior refletem a precisão de agregação e ficam dentro do resíduo registrado; não mudam as participações apresentadas. A leitura 2020–2025 é diagnóstica, embora participe integralmente do resumo da série observada.

## Alcance da conclusão

Este checkpoint satisfaz o **critério 9 da Decisão 024**, que exige o teste de invariância dos campos não dependentes de origem e a comparação explícita de um painel corrigido versionado. Não houve reexportação independente de todos os demais fluxos raster; esses campos foram preservados dos produtos v1 autenticados e sua dependência foi auditada. Os produtos aceitos v1 permanecem imutáveis e os achados P9A035–P9A037 continuam suspensos.

A Decisão 024 permanece como especificação vigente **ainda não integralmente implementada**. Permanecem:

1. critério 10: propagar tipo e ano dos eventos de fronteira 2024–2025 para a produção do domínio inteiro;
2. critério 11: concluir a auditoria dos códigos anômalos `1` e `100` e de sua sobreposição;
3. critério 12: completar validações, manifesto e produtos de evidência corrigidos, com novo evento versionado para qualquer eventual retirada da suspensão;
4. revalidar população, definição e hashes da coorte fixa de PAS em 1985 usada em RQ1, conforme etapa 8 do Plano 008 v3.

Até essas verificações, não declarar a remediação completa nem promover os achados suspensos como evidência aceita. Os oito CSVs corrigidos para associação espacial por `cell_id` constituem produto posterior, a ser derivado e validado a partir dos painéis v2 quando essa exportação for implementada.

## Evidências compactas para este registro

- `outputs/validation/pasture_spell_panel_v2/canonical_pasture_spell_panel_v2_validation.json`
- `outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_interval_summary_v2.csv`
- `outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_pooled_summary_v2.csv`
- Validação prévia: `canonical_pasture_spell_nonorigin_invariance_validation_v1.json` (SHA-256 `fdeb8d99f6bbfeb65e855975b88dcb1cc8fa98f692ca9e35eb0b81357b8bf3e3`).
