# Sensibilidade da origem da janela — resultados completos v1

Data: 2026-10-12. **Status: FULL VALIDATION PASS. Análise descritiva de sensibilidade concluída.**

O motor determinístico foi executado com origens de janela em 1985, 1995 e 2000, mantendo a fonte de cobertura, a grade de 24.889 células e o cálculo das conversões PAS→TMP. O painel contém 19 combinações janela/intervalo e 472.891 linhas: 423.113 novas exportações nativas e 49.778 linhas aceitas reutilizadas dos dois primeiros intervalos de 1985. Os dados reutilizados mantêm seus contadores nativos ausentes; não foram apresentados como uma nova execução.

## Resultado principal: a interpretação depende da janela

Nas mesmas conversões de 2000–2020, a parcela de origem initial é 38,1006% com origem em 1985, 64,6950% com origem em 1995 e 78,0709% com origem em 2000. O denominador comum é **15.22117738 milhões de hectares**, somados por intervalo. Essa área não é uma contagem de pixels únicos ao longo do período. Entre 1985 e 2000, a atribuição initial aumenta **39.9703 pontos percentuais** por redefinição da fronteira observacional, mantendo as conversões de cada intervalo.

| baseline_year | initial_pct | entry_pct | unresolved_pct |
| --- | --- | --- | --- |
| 1985 | 38.1006 | 61.8991 | 0.0004 |
| 1995 | 64.6950 | 35.3047 | 0.0002 |
| 2000 | 78.0709 | 21.9290 | 0.0001 |

O motor não detecta que a pastagem física mudou quando trocamos a janela: muda a história disponível para atribuir a origem do episódio atual. Pastagens contínuas desde uma fronteira mais recente podem ter sido estabelecidas após 1985 e, portanto, pertencem à entrada observada na análise original. A maioria de entrada observada no calendário comum é válida sob a definição de 1985 e não se mantém sob as duas definições mais recentes.

## Mesmo calendário, por intervalo

| interval | b1985_initial_pct | b1995_initial_pct | b2000_initial_pct |
| --- | --- | --- | --- |
| 2000_2005 | 48.7592 | 81.8234 | 100.0000 |
| 2005_2010 | 41.2026 | 64.3697 | 77.0950 |
| 2010_2015 | 34.3548 | 59.8974 | 72.3990 |
| 2015_2020 | 31.0832 | 55.6977 | 66.3582 |
| 2020_2025 | 20.1156 | 38.6191 | 48.2418 |

O último intervalo, 2020–2025, é diagnóstico e está separado da comparação primária de 2000–2020. Sua limitação de fronteira da fonte permanece. A participação initial é 100% em 2000–2005 para a janela de 2000 por construção; esse ponto não é evidência de uma condição inicial do processo.

## Mesmo tempo de acompanhamento

Todas as janelas começam com 100% initial no primeiro intervalo, onde há conversão positiva. A queda reaparece nas três janelas, mas as curvas não coincidem. Os valores abaixo referem-se aos anos decorridos até o **início** do intervalo; 15 anos corresponde ao quarto intervalo, que termina no vigésimo ano de acompanhamento.

| elapsed_years | b1985_initial_pct | b1995_initial_pct | b2000_initial_pct |
| --- | --- | --- | --- |
| 0 | 100.0000 | 100.0000 | 100.0000 |
| 5 | 70.3907 | 81.8234 | 77.0950 |
| 10 | 57.2046 | 64.3697 | 72.3990 |
| 15 | 48.7592 | 59.8974 | 66.3582 |

O agregado dos primeiros quatro intervalos é:

| baseline_year | initial_pct | entry_pct | unresolved_pct |
| --- | --- | --- | --- |
| 1985 | 63.6392 | 36.3606 | 0.0002 |
| 1995 | 72.2535 | 27.7463 | 0.0002 |
| 2000 | 78.0709 | 21.9290 | 0.0001 |

Os períodos e estoques iniciais são diferentes:

| baseline_year | baseline_stock_Mha | first_t0 | last_t1 | initial_pct |
| --- | --- | --- | --- | --- |
| 1985 | 49.0359 | 1985 | 2005 | 63.6392 |
| 1995 | 79.5769 | 1995 | 2015 | 72.2535 |
| 2000 | 92.0135 | 2000 | 2020 | 78.0709 |

Os estoques iniciais são aproximadamente 49,04, 79,58 e 92,01 Mha. Os denominadores das conversões nos respectivos primeiros 20 anos são 8.4026, 13.1143 e 15.2212 Mha. Essas diferenças impedem interpretar a comparação por acompanhamento como isolamento do efeito da janela.

## Continuidade do estoque versus origem das conversões

Após 15 anos, a fração do estoque PAS da fronteira ainda observada continuamente em PAS é:

| baseline_year | continuous_baseline_stock_retained_pct | initial_pct |
| --- | --- | --- |
| 1985 | 76.9780 | 48.7592 |
| 1995 | 76.7096 | 59.8974 |
| 2000 | 74.0393 | 66.3582 |

As frações de estoque contínuo nesse tempo são próximas (76,98%, 76,71% e 74,04%), enquanto a composição das conversões varia mais (48,76%, 59,90% e 66,36%). Isso distingue perda de continuidade do estoque e seleção das pastagens que se convertem em TMP. A proximidade das curvas de estoque é descritiva; não constitui teste de estacionariedade ou igualdade de riscos. A forma decrescente das curvas de origem não permite estimar quanto é gerado mecanicamente pela janela e quanto decorre do processo de conversão.

## O cruzamento de 50% não é um limiar do processo

Com fronteira em 1985, a entrada observada supera 50% pela primeira vez em 2000–2005. Nas janelas de 1995 e 2000, esse cruzamento não ocorre na série primária que termina em 2020; ocorre somente no intervalo diagnóstico 2020–2025. O descritor muda quando a janela muda e não sustenta um marco temporal intrínseco ou uma transição de regime. A tabela de cruzamento primário original permanece inalterada; a revisão adicional registra explicitamente os cruzamentos diagnósticos.

## Consequências para P9A035 e P9A036

A sensibilidade reforça a qualificação já registrada na errata v4.1: a origem initial é continuidade desde uma fronteira observada, e a trajetória e os cruzamentos são estatísticas condicionadas por essa definição. Os números da análise canônica de 1985 permanecem reproduzidos e utilizáveis como descrição. A redação do manuscrito deve nomear a fronteira de 1985 e evitar generalizar seus shares para estoque antigo versus pastagem recém-estabelecida ou usar 2000–2005 como limiar do processo. Não se calculou uma fração de artefato; não se demonstrou que toda a queda é mecânica, estacionariedade ou mudança de regime. A decomposição de primeira entrada versus reentrada continua pendente.

## Validação e limites de garantia

Todos os 48 CSVs e o manifesto estão presentes. Os hashes das oito referências aceitas, a população das células/lotes, versões, janelas, 41 bandas anuais e projeção nativa passaram. Os três contadores de invariância nativa são zero nas linhas novas. Os 30 testes sintéticos nativos previamente aceitos mantêm o mesmo hash e todos os contadores de divergência zerados. Estoques de fronteira são constantes no acompanhamento; o estoque contínuo não ganha membros, e as categorias respeitam o aninhamento entre janelas. Fluxos e estoques por calendário não mudam com a fronteira. A diferença máxima dos campos de controle em relação à referência é 3.2782554626464844e-07 ha por célula. Os resíduos máximos de partição por linha são 2.7284841053187847e-12 ha para fluxo e 1.4551915228366852e-11 ha para estoque.

A aritmética não valida a acurácia da classificação, os hashes de nomes de assets não autenticam seus conteúdos mutáveis e a identidade remota do texto executado não foi verificada independentemente. Sem declaração específica do operador, o hash de texto executado permanece null. O escopo nativo cobre a lógica categórica e suas invariantes; idade auxiliar 201, raster de eventos 2024/2025, fases 2–8 e decomposição de reentrada não foram reexecutados nesta análise.

Figura: `figures/window_origin_sensitivity_v1/fig01_window_origin_sensitivity_v1.png` (também SVG e PDF). Dados e hashes estão em `outputs/validation/window_origin_sensitivity_v1/full/`. O painel grande e os CSVs nativos estão no pacote de dados externo ao GitHub. Esta etapa da sensibilidade está encerrada; a liberação pública com DOI permanece independente e pendente.
