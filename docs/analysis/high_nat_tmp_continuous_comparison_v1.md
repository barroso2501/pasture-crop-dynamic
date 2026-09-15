# Comparação das áreas contínuas na coorte de alta magnitude NAT→TMP

- **Data:** 15/09/2026.
- **Status:** Comparação executada e validada numericamente; interpretação exploratória.
- **Script:** `analysis/09b_compare_high_nat_tmp_continuous_areas.py`.
- **Coorte:** 2.598 células com classe alta em pelo menos um intervalo de 1985–2020.
- **Dados:** Oito tabelas GIS 08c autenticadas, 24.889 células por intervalo e 78 campos.
- **Painel selecionado:** 20.784 linhas célula–intervalo, mantendo a mesma coorte em 2020–2025.

## Resultados principais

A comparação contínua confirma que 2000–2005 foi o máximo de área NAT→TMP,
além de máximo da contagem de células altas: 2,116 Mha na coorte, equivalentes
a 92,2% da área desse processo no domínio. O período 2010–2015 apresenta uma
segunda elevação local, com 1,157 Mha. Em 2015–2020, a área cai a 0,546 Mha,
74,2% abaixo do máximo. O padrão das contagens de classes é, portanto,
confirmado para esse máximo, mas áreas e contagens continuam sendo medidas
distintas.

A coorte acumula 8,010 Mha de NAT→TMP nos sete intervalos, reproduzindo o total
exploratório anterior e representando 87,5% dos 9,151 Mha no domínio. Essas
somas são áreas de transições por intervalo, sem deduplicar pixels que possam
reaparecer no processo ao longo da série. Elas não são uma apuração de área
única cumulativa.

| Período | NAT→TMP (Mha) | % da área do domínio | Reposição (Mha) | Consolidação (Mha) | Índice agregado C–R | Pastagem detectada (%) |
|---|---:|---:|---:|---:|---:|---:|
| 1985–1990 | 1,199 | 85,5 | 1,799 | 0,360 | -0,667 | 7,22 |
| 1990–1995 | 1,036 | 87,8 | 1,720 | 0,504 | -0,547 | 6,83 |
| 1995–2000 | 1,124 | 91,8 | 1,402 | 0,693 | -0,338 | 5,05 |
| 2000–2005 | 2,116 | 92,2 | 1,575 | 1,366 | -0,071 | 5,69 |
| 2005–2010 | 0,832 | 88,0 | 0,779 | 0,948 | 0,098 | 6,45 |
| 2010–2015 | 1,157 | 85,0 | 0,769 | 1,391 | 0,288 | 7,50 |
| 2015–2020 | 0,546 | 73,7 | 0,677 | 0,830 | 0,102 | 8,49 |
| 2020–2025 * | 0,453 | 66,5 | 0,812 | 0,483 | -0,254 | 4,38 |


*2020–2025 é diagnóstico, mantido no cálculo e sinalizado; a seleção da coorte
continua baseada apenas em 1985–2020.*

## Participação da coorte e exposição inicial

A participação da coorte no total do domínio cai de 92,2% no máximo para 73,7%
em 2015–2020 e 66,5% no diagnóstico. Isso registra aumento relativo da
contribuição das demais células, não demonstra por si só dispersão geográfica
ou criação de novos clusters. A coorte foi selecionada retrospectivamente pelo
histórico de classe alta; não é uma amostra aleatória do domínio.

O máximo também permanece quando a área é normalizada pelo estoque natural
inicial agregado das células com denominador válido: a intensidade agrupada
é 6,10% em 2000–2005, comparada a 2,72% em 1985–1990 e 2,02% em 2015–2020.
Esse cálculo é uma razão entre somas, não média das taxas das células,
probabilidade anual ou ajuste estatístico da exposição.

## Redistribuição espacial ponderada pela área

O centro ponderado da coorte passa de aproximadamente 52,754° W e 14,811° S
em 1985–1990 para 49,501° W e 9,435° S em 2015–2020, uma diferença líquida de
cerca de 692 km em direção geral norte/nordeste. A trajetória não é retilínea:
há um salto de 430 km entre 2000–2005 e 2005–2010, seguido de movimentos menores
para norte e depois para noroeste.

| Período | Longitude ponderada | Latitude ponderada | Distância ao centro anterior (km) |
|---|---:|---:|---:|
| 1985–1990 | -52,754 | -14,811 | — |
| 1990–1995 | -53,012 | -13,816 | 113,5 |
| 1995–2000 | -52,164 | -12,711 | 152,9 |
| 2000–2005 | -51,884 | -12,064 | 77,8 |
| 2005–2010 | -48,091 | -10,990 | 430,4 |
| 2010–2015 | -47,910 | -10,249 | 84,3 |
| 2015–2020 | -49,501 | -9,435 | 196,4 |
| 2020–2025 * | -48,481 | -9,832 | 120,2 |


O salto para leste coincide com a queda da área associada às células de bioma
principal Amazônia, de 0,840 Mha para 0,126 Mha; sua participação na área da
coorte passa de 39,7% para 15,2%. A área associada ao Cerrado também diminui,
mas de forma proporcionalmente menor, de 1,276 Mha para 0,705 Mha. Trata-se de
redistribuição dos pesos dentro de uma população fixa, não de movimento dos
mesmos pixels, propriedades ou de uma frente espacial acompanhada diretamente.

O cálculo usa centroides de células transformados para o Albers equal-area do
projeto e ponderados pelos hectares NAT→TMP. O resultado é uma aproximação
espacial por célula, não o centro geométrico exato dos pixels convertidos.
As distâncias entre os centros foram calculadas no elipsoide GRS 1980. Mapas
exibem os pontos em coordenadas geográficas, com a mesma escala logarítmica
de magnitude em todos os intervalos.

Os rótulos de bioma principal atribuem a área à célula e não aos pixels dentro
de cada bioma. As 163 células transbioma da coorte exigem essa qualificação;
não se apresentam esses totais como conversão pixel a pixel dentro dos biomas.
Não foram definidos clusters, UF/municípios ou testes de significância espacial.

## Balanço C–R: soma dos fluxos e composição das células

Na coorte, a soma da consolidação PAS→TMP supera a soma da reposição NAT→PAS
nos três últimos intervalos primários. O índice agrupado muda de −0,667 no
primeiro período para +0,098 em 2005–2010, +0,288 em 2010–2015 e +0,102 em
2015–2020. Isso reforça a mudança do balanço observada pelas contagens.

Todavia, valores positivos não são automaticamente consolidação dominante
pela regra 2:1. Nos quatro últimos intervalos primários o índice agrupado
permanece na faixa mista, −1/3 a +1/3. O valor máximo +0,288 corresponde a
consolidação aproximadamente 1,81 vez maior que reposição, abaixo de 2:1.

Há outra leitura complementar: em 2015–2020, 44,0% da área NAT→TMP da coorte
ocorre em células classificadas como reposição dominante, 27,7% em células de
consolidação dominante, 26,2% em mistas e 2,2% em inativas. Portanto, a maior
soma de PAS→TMP na coorte não significa que a maioria da área NAT→TMP esteja
em células de consolidação dominante. São agregações e denominadores distintos.

O índice agrupado é `(ΣC−ΣR)/(ΣC+ΣR)`, não a média do índice das células nem
um índice ponderado por NAT→TMP. A associação de área NAT→TMP aos estados C–R
não altera a definição: NAT→TMP não compõe diretamente a soma C+R.

## Pastagem intermediária detectada

A participação da área com alguma pastagem intermediária detectada varia de
5,05% a 8,49% nos sete períodos primários. Na soma do período primário,
ela é 6,51%; a participação com dois anos consecutivos de pastagem é 6,21%.

Essas participações são razões entre somas de áreas de trajetórias e área
endpoint, incluindo todos os fluxos válidos da coorte, sem aplicar a exclusão
de baixo suporte usada para classificar proporções individuais na Fase 3.
A regra de suporte de cerca de 20 ha protege a leitura da proporção por célula,
não elimina pequenas áreas da contabilidade agregada.

A maior parte da área endpoint não teve pastagem intermediária detectada nas
observações anuais do intervalo. Isso não autoriza chamar o complemento de
conversão direta comprovada: uma etapa curta, anterior ao intervalo ou não
resolvida pelas classes anuais pode não aparecer. A composição aqui também
não substitui o fluxo PAS→TMP medido em outros pixels da mesma célula.

## Extensão diagnóstica

Em 2020–2025, a coorte soma 0,453 Mha NAT→TMP, 66,5% da área do domínio.
A reposição supera novamente a consolidação na soma da coorte; o índice
agrupado é −0,254, ainda misto. A pastagem intermediária detectada representa
4,38% da área endpoint, e a definição de dois anos consecutivos, 4,12%.

Esses resultados permanecem nos gráficos e tabelas com flag diagnóstico.
Não foram usados para selecionar novas células ou redefinir os resultados
primários. As 106 células que só atingem classe alta no diagnóstico continuam
fora da coorte primária fixa, embora suas áreas integrem o denominador do domínio.

## Figuras e tabelas

- `high_nat_tmp_area_flows_composition_v1.png`: magnitude contínua, fluxos, balanço e composição.
- `high_nat_tmp_continuous_spatial_panels_v1.png`: oito mapas de centroides coloridos pela área e centro ponderado.
- `high_nat_tmp_weighted_centroid_trajectory_v1.png`: trajetória do centro ponderado com o diagnóstico separado.
- `high_nat_tmp_continuous_period_summary_v1.csv`: resultados numéricos por período.
- `high_nat_tmp_continuous_primary_biome_v1.csv`: áreas associadas ao bioma principal das células.
- `high_nat_tmp_continuous_cr_state_v1.csv`: área NAT→TMP associada a cada estado C–R.
- `high_nat_tmp_continuous_cell_interval_v1.csv`: painel selecionado, com IDs, contexto, áreas e denominadores.
- `gis/`: oito tabelas com uma linha por célula e intervalo separado, mais `schema.ini` sem a opção CharacterSet rejeitada pelo ArcGIS.
- `high_nat_tmp_weighted_centroids_v1.geojson`: oito centros ponderados em coordenadas geográficas.

A comparação valida e complementa a exploração por classes; não modifica o
desenho da Fase 4A nem exige reexecutar GEE ou seus produtos aceitos.
O próximo aprofundamento é separar geograficamente os conjuntos ocidental e
oriental com unidades ou critérios previamente documentados, e avaliar as
mesmas medidas no conjunto completo do domínio. Isso permitirá verificar se a
redistribuição dos pesos reflete diferenças regionais sem transformar uma
inspeção visual em fases históricas ou clusters escolhidos após os resultados.
