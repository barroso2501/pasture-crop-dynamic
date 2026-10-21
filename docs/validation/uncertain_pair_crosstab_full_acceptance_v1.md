# Pares incertos: validação completa aceita

**21/10/2026 — PASS.** Validador original `analysis/19b_validate_uncertain_pair_crosstab_v1.py`, com `--scope full`.

## Inventário e preservação

Foram recebidos nove CSVs: oito lotes e um manifesto. A pasta de validação recebeu adicionalmente a cópia exata do CSV sintético aceito no piloto. Os três CSVs nativos e os produtos aceitos do piloto foram preservados byte a byte. Nenhuma tarefa GEE foi reexecutada. As 33 entradas do inventário SHA-256 original foram verificadas antes de qualquer atualização documental.

| Lote | Células | Linhas |
|---|---:|---:|
| canonical_uncertain_pairs_b00_v1.csv | 3168 | 6336 |
| canonical_uncertain_pairs_b01_v1.csv | 3128 | 6256 |
| canonical_uncertain_pairs_b02_v1.csv | 3061 | 6122 |
| canonical_uncertain_pairs_b03_v1.csv | 3118 | 6236 |
| canonical_uncertain_pairs_b04_v1.csv | 3104 | 6208 |
| canonical_uncertain_pairs_b05_v1.csv | 3105 | 6210 |
| canonical_uncertain_pairs_b06_v1.csv | 3088 | 6176 |
| canonical_uncertain_pairs_b07_v1.csv | 3117 | 6234 |
| Total | 24.889 | 49.778 |

Cada célula tem os pares 2023→2024 e 2024→2025. O domínio canônico de 24.889 células é distinto das 21.869 células da auditoria direcionada da idade v2.

## Critérios e resultados

- Inventário completo, chaves únicas, atribuição de células/lotes e metadados: PASS.
- Configuração, lista de 41 bandas, CRS e seis coeficientes da transformação dos três anos: PASS.
- 34 casos sintéticos nativos reutilizados, com 204 valores de erro iguais a zero.
- 149.334 valores dos três contadores de erro nas linhas reais: todos iguais a zero.
- Partições de 25 estados, suporte observado/incerto e três grupos condicionais: PASS.
- Identidades por célula com tolerância de 0,01 ha; agregados com tolerância de 0,001 ha: PASS.
- Maior resíduo celular de suporte: 1.09139364213e-11 ha; maior resíduo da partição condicional: 0 ha.
- As quatro linhas reais do piloto foram comparadas adicionalmente às correspondentes linhas completas: diferença máxima de 3.63797880709e-12 ha.
- Identidade dos hashes da configuração e dos casos sintéticos com o piloto aceito: PASS.
- Reexecução local idêntica com reutilização dos produtos imutáveis: PASS.

## Controles históricos

| Ano do evento | Tipo | Campo | Resultado (ha) | Referência (ha) | Diferença (ha) |
|---|---|---|---:|---:|---:|
| 2024 | entry | event_area_ha | 2523813.814125023 | 2523813.814120000 | 5.02308830619e-06 |
| 2024 | entry | uncertain_pair_ha | 4688518.256609377 | 4688518.256610000 | -6.23054802418e-07 |
| 2024 | termination | event_area_ha | 2539640.499419887 | 2539640.499420000 | -1.13155692816e-07 |
| 2024 | termination | uncertain_pair_ha | 4688518.256609377 | 4688518.256610000 | -6.23054802418e-07 |
| 2025 | entry | event_area_ha | 3063669.749153205 | 3063669.749150000 | 3.20468097925e-06 |
| 2025 | entry | uncertain_pair_ha | 4688463.670440795 | 4688463.670440000 | 7.95349478722e-07 |
| 2025 | termination | event_area_ha | 2783060.795957198 | 2783060.795960000 | -2.80141830444e-06 |
| 2025 | termination | uncertain_pair_ha | 4688463.670440795 | 4688463.670440000 | 7.95349478722e-07 |

O maior desvio absoluto é 5,0231 × 10⁻⁶ ha, abaixo da tolerância de 0,001 ha. A área incerta repetida nas linhas de entrada e término representa a mesma população anual; não deve ser somada. O controle reproduz totais agregados históricos. Não constitui comparação espacial por célula com os antigos eventos nem nova comparação com o raster de eventos.

## Evidência e alcance

O relatório original está em `outputs/validation/uncertain_pair_crosstab_v1/full/canonical_uncertain_pairs_full_v1_validation.json`. A revisão adicional registra inventários, hashes, comparação piloto/completo, resíduos e controles em `received_full_review_v1.json`. Todos os cinco CSVs derivados pelo validador estão na mesma pasta.

A validação avalia os arquivos fornecidos pelo operador. O hash do script fornecido está fixado, mas o hash do texto efetivamente executado e a atestação do operador continuam nulos. Não houve observação independente da execução remota. A interpretação de PAS está em `docs/results/uncertain_pair_crosstab_full_findings_v1.md`.

Esta etapa conclui a tabela de pares incertos no domínio completo. Matriz v4.3 e events-v5 continuam atuais e não foram editados. A decomposição cronológica de primeira entrada/reentrada, idade numérica auxiliar 201 e publicação DOI mantêm seu escopo e estado anteriores.
