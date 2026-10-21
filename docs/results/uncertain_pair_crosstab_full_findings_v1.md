# Participação de PAS na área de pares incertos

**Domínio completo validado em 21/10/2026.** São 24.889 células e dois pares anuais da extensão diagnóstica. Todos os números abaixo usam áreas somadas; não são médias das proporções celulares.

| Par anual | Área incerta (ha) | PAS no início (ha) | PAS no fim (ha) | PAS observado em um extremo (ha) | Participação na área incerta (%) |
|---|---:|---:|---:|---:|---:|
| 2023→2024 | 4688518.256609 | 11.914080 | 9.019542 | 20.933621 | 0.00044649 |
| 2024→2025 | 4688463.670441 | 6.205013 | 12.186375 | 18.391388 | 0.00039227 |

Os grupos com PAS observado no início e no fim são disjuntos dentro do conjunto incerto: o outro extremo precisa ser inválido. Assim, sua soma mede PAS observado em qualquer um dos dois extremos sem duplicação.

## O que compõe os aproximadamente 4,69 Mha

| Par anual | Ambos os extremos mascarados (ha) | % da área incerta | Sem PAS observado nos extremos (%) |
|---|---:|---:|---:|
| 2023→2024 | 4688357.422835 | 99.99656962 | 99.99955351 |
| 2024→2025 | 4688366.056147 | 99.99791799 | 99.99960773 |

Todas as parcelas incertas não nulas envolvem máscara em pelo menos um extremo. As parcelas que envolvem NODATA (código 27) ou códigos inesperados somam zero nesses arquivos. Os aproximadamente 4,69 Mha por par são dominados pela categoria mascarado→mascarado.

A interseção com PAS **observado** é muito pequena. Entretanto, “sem PAS observado” inclui pixels sem observação nos dois extremos: não significa cobertura conhecida como não pastagem. Essa tabela não estima a cobertura real desses pixels, não demonstra ausência de pastagem em outros anos e não permite concluir que toda a incerteza relevante para PAS se limita aos 20,93/18,39 ha. A causa geográfica ou técnica da grande parcela mascarada→mascarada não foi investigada por esta validação agregada.

## Denominadores condicionais

| Par anual | Suporte PAS inicial (ha) | Incerto / PAS inicial (%) | Suporte PAS final (ha) | Incerto / PAS final (%) |
|---|---:|---:|---:|---:|
| 2023→2024 | 108684231.566991 | 0.0000109621 | 108668401.987159 | 0.0000083001 |
| 2024→2025 | 108668401.987159 | 0.0000057100 | 108949016.921717 | 0.0000111854 |

Essas taxas condicionais dividem a área incerta com PAS observado naquele extremo pelo suporte total de PAS observado no mesmo extremo. Medem perda ou ausência da observação oposta quando PAS está observado, e não a chance de existir PAS sob a máscara.

Os pares anuais podem contar os mesmos pixels em anos diferentes. Não se deve somar as duas áreas para obter uma área espacial única. Da mesma forma, as entradas e os términos da tabela histórica repetem a mesma área incerta de cada par.

## Relação com a contabilidade

A área incerta de toda a cobertura e os 62,568807 ha históricos de conversão PAS→TMP com origem não resolvida pertencem a populações e definições temporais distintas. A comparação direta entre os valores não é uma medida de erro, fração de artefato ou parcela a redistribuir entre origens.

A etapa confirma e explica a composição observacional dos totais históricos de incerteza. Ela usa apenas `coverage_v3`, não o asset de idade de pastagem v2. Não fornece motivo, isoladamente, para recalcular a contabilidade corrigida ou migrar sua origem para o asset de idade v2. A origem analítica continua sendo o episódio observado reconstruído da cobertura anual.

Matriz v4.3 e events-v5 permanecem inalterados. Primeira entrada/reentrada, idade numérica 201, atestação histórica de execução e DOI mantêm seus estados anteriores.

Fontes locais: cinco CSVs de saída do validador em `outputs/validation/uncertain_pair_crosstab_v1/full/`, referências históricas fixadas em `config/` e a tabela adicional `outputs/summary/uncertain_pair_crosstab_v1/full/observed_pas_in_uncertain_area_v1.csv`. A aceitação e as limitações de execução estão em `docs/validation/uncertain_pair_crosstab_full_acceptance_v1.md`.
