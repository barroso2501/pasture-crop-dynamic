# Primeira entrada e reentrada observadas: domínio completo

**23/10/2026 — exportações nativas aceitas; 24.889 células e oito intervalos.** Valores calculados pelo validador distribuído sem alterações. Separação auxiliar aplicada somente ao componente de entrada pós-1985 já aceito na contabilidade de origem.

## Fluxos PAS→TMP

| Intervalo | PAS→TMP total (ha) | Episódio inicial (ha) | Entrada pós-1985 (ha) | Primeira entrada observada (ha) | Reentrada observada (ha) | Histórico anterior incerto (ha) | Origem não resolvida (ha) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1985–1990 | 1450003.979397 | 1450003.979397 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 1990–1995 | 1638736.605527 | 1153518.271081 | 485217.116757 | 473790.071670 | 11424.001292 | 3.043794 | 1.217689 |
| 1995–2000 | 1809550.134841 | 1035145.531797 | 774399.382462 | 689150.341594 | 85242.248379 | 6.792490 | 5.220582 |
| 2000–2005 | 3504280.627226 | 1708658.594866 | 1795610.451551 | 1552768.424440 | 242815.652738 | 26.374374 | 11.580808 |
| 2005–2010 | 2825891.973992 | 1164341.131387 | 1661537.728348 | 1378961.468576 | 282555.261584 | 20.998188 | 13.114257 |
| 2010–2015 | 4974529.591197 | 1708989.757515 | 3265518.008070 | 2756900.593017 | 508596.955885 | 20.459167 | 21.825613 |
| 2015–2020 | 3916475.186386 | 1217364.836966 | 2699100.739562 | 2183070.727765 | 516010.727646 | 19.284151 | 9.609858 |
| 2020–2025 (diagnóstico) | 2086326.750031 | 419677.457137 | 1666640.246879 | 1125167.057738 | 541458.935683 | 14.253459 | 9.046015 |

Em cada linha, episódio inicial + entrada pós-1985 + origem não resolvida = fluxo total. Primeira entrada observada + reentrada observada + histórico anterior incerto = componente de entrada pós-1985. Histórico anterior incerto é uma subdivisão de episódio com entrada confirmada; difere de origem atual não resolvida.

## Composições condicionais

| Intervalo | Primeira entrada / fluxo de entrada (%) | Reentrada / fluxo de entrada (%) | Reentrada / estoque de entrada em t0 (%) |
|---|---:|---:|---:|
| 1985–1990 | — | — | — |
| 1990–1995 | 97.644962 | 2.354410 | 1.610358 |
| 1995–2000 | 88.991592 | 11.007531 | 6.123229 |
| 2000–2005 | 86.475796 | 13.522736 | 9.296237 |
| 2005–2010 | 82.993088 | 17.005648 | 10.816377 |
| 2010–2015 | 84.424602 | 15.574771 | 12.891065 |
| 2015–2020 | 80.881410 | 19.117876 | 15.853277 |
| 2020–2025 (diagnóstico) | 67.511094 | 32.488051 | 17.906327 |

Cada fração usa a soma das áreas sobre o domínio. O denominador do fluxo é `entry_ha`, e o do estoque é `entry_pas_stock_ha` em t0. Não são médias de percentuais por célula nem participações no fluxo PAS→TMP total. A fração restante do fluxo de entrada é o histórico anterior incerto, preservado sem arredondamento nos CSVs.

Em 2015–2020, a reentrada observada contribui 516.010,727646 ha, equivalentes a 19,117876% do componente de entrada. Em 2020–2025, diagnóstico, contribui 541.458,935683 ha, ou 32,488051% desse componente. Os percentuais de estoque correspondentes são 15,853277% e 17,906327%; descrevem populações distintas das frações de fluxo. Não se interpreta essa comparação isolada como risco, causalidade ou teste de tendência.

## Alcance

- “Primeira entrada observada” exige ausência de PAS e cobertura anterior válida desde 1985; não significa primeira implantação histórica.
- Reentrada exige PAS observado em algum ano anterior; o rótulo é fixado na entrada e mantido durante o episódio confirmado.
- Lacunas não provam saída nem permitem unir episódios; a classe de histórico incerto preserva a informação faltante.
- Em 1985–1990 só existe origem inicial por construção. O denominador de entrada é zero, por isso as frações ficam em branco, sem imputar zero percentual.
- 2020–2025 é extensão diagnóstica. Os resultados principais terminam em 2020.
- Áreas em intervalos distintos podem incluir os mesmos pixels; sua soma não representa uma união espacial única. Os contadores anuais são equivalentes ponderados de pixels-ano.
- A garantia de idade 201 refere-se à idade auxiliar reconstruída da cobertura, inclusive reinício na reentrada. Não é validação completa dos valores do produto público de idade v2.

A matriz v4.3/events-v5 permanece inalterada neste registro. A incorporação científica desta decomposição é a etapa seguinte. Fonte numérica: `outputs/validation/entry_reentry_v1/full/canonical_entry_reentry_full_v1_summary.csv`.
