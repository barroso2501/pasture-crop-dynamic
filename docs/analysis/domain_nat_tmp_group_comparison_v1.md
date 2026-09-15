# Comparação dos quatro grupos NAT→TMP no domínio completo

- Data: 15/09/2026.
- Status: execução local com insumos autenticados; descrição exploratória.
- Versão: `phase4a-domain-nat-tmp-groups-v1`.
- Domínio: 24.889 células, 199.112 registros em oito intervalos.

## Definição dos grupos

Cada célula recebe um único grupo, definido pela maior classe congelada NAT→TMP
atingida nos sete intervalos de 1985–2020. Não se calcula uma classe nova a partir
da soma, da média ou da área máxima arredondada. Os quatro grupos são excludentes,
completos e permanecem fixos no acompanhamento até 2025.

| Grupo | Células | % do domínio |
|---|---:|---:|
| Sem ocorrência primária | 11.213 | 45.05 |
| Máxima baixa | 4.887 | 19.64 |
| Máxima moderada | 6.191 | 24.87 |
| Máxima alta | 2.598 | 10.44 |


“Sem ocorrência” refere-se somente a NAT→TMP no período primário. Não significa
inatividade geral: essas células podem apresentar NAT→PAS, PAS→TMP e mudanças no
balanço C–R. NAT→TMP é uma mudança endpoint entre vegetação natural e agricultura
temporária; não exige ausência de pastagem intermediária.

## Participação na área do domínio

A tabela apresenta a participação de cada grupo na área NAT→TMP de cada intervalo,
não a participação nas contagens de células. As áreas podem ser positivas em uma
classe diferente daquela que definiu o grupo retrospectivo.

| Período | Sem ocorrência (%) | Máxima baixa (%) | Máxima moderada (%) | Máxima alta (%) |
|---|---:|---:|---:|---:|
| 1985–1990 | 0.00 | 0.22 | 14.26 | 85.52 |
| 1990–1995 | 0.00 | 0.22 | 12.03 | 87.75 |
| 1995–2000 | 0.00 | 0.25 | 7.94 | 91.82 |
| 2000–2005 | 0.00 | 0.19 | 7.61 | 92.20 |
| 2005–2010 | 0.00 | 0.51 | 11.52 | 87.97 |
| 2010–2015 | 0.00 | 0.57 | 14.47 | 84.96 |
| 2015–2020 | 0.00 | 1.07 | 25.24 | 73.69 |
| 2020–2025 * | 1.72 | 4.78 | 27.03 | 66.47 |


*2020–2025 permanece incluído e identificado como diagnóstico.*

O aumento relativo das células moderadas de 7,61% em 2000–2005 para 25,24% em
2015–2020 não indica uma expansão contínua de sua área. Elas registram 174,6 mil
ha no primeiro desses períodos, 197,2 mil em 2010–2015 e 186,9 mil em 2015–2020.
A queda da coorte alta de 1,157 milhão para 0,546 milhão de ha entre os dois últimos
períodos primários explica grande parte do aumento relativo recente das moderadas.

As células baixas representam 19,64% das células, mas somente 1,07% da área
NAT→TMP em 2015–2020. Não se deve substituir a comparação das áreas pela contagem
de células, nem interpretar os grupos como unidades de igual área ou exposição.

## Intensidade e disponibilidade de vegetação

A razão entre a soma NAT→TMP e a soma do estoque natural inicial, nas células com
denominador válido, continua muito maior no grupo alto. Em 2015–2020 ela é 2,02%
no grupo alto, 0,301% no moderado e 0,0144% no baixo. Em 2000–2005, o grupo alto
atinge 6,10%. O contraste persiste ao considerar a exposição inicial, mas a seleção
retrospectiva por magnitude favorece esse contraste por construção; não é teste
independente de uma hipótese nem evidência causal.

## Balanço consolidação–reposição

Os grupos sem ocorrência primária e de máxima baixa mantêm reposição dominante
na soma dos fluxos em todos os intervalos. O grupo moderado passa de índice −0,742
em 1985–1990 para uma faixa mista em 2005–2010, 2010–2015 e 2015–2020; no último,
o índice é −0,009, praticamente equilibrado. No diagnóstico retorna a −0,419,
compatível com reposição dominante no agregado.

O grupo alto apresenta C maior que R nos três últimos intervalos primários,
mas seus índices +0,098, +0,288 e +0,102 permanecem mistos pela regra 2:1.
A tabela de estados C–R preserva separadamente as contagens das células e a área
NAT→TMP associada a cada estado. O índice de somas não é a média dos índices nem
uma classificação de todas as células do grupo.

## Persistência temporal

Foram reconstruídas 99.556 sequências: 24.889 células × dois eixos centrais
NAT→TMP/C–R × duas janelas, primária e completa. A reconstrução preserva os estados
congelados, e seus indicadores de mudanças e episódios foram comparados aos
produtos GIS aceitos da Fase 4A. Ela não redefine a tipologia de trajetórias.

No eixo NAT→TMP primário, o número médio de mudanças de classe é 2,945 no grupo
alto, 2,713 no moderado, 1,950 no baixo e zero no grupo sem ocorrência. O grupo alto
registra atividade NAT→TMP em média em 6,00 dos sete intervalos, o moderado em 4,84
e o baixo em 2,28. O grupo alto tem somente três sequências de magnitude constantes;
isso não equivale a ausência de atividade nas demais.

Um episódio significa permanência consecutiva na mesma classe. Episódios longos
podem ser de classe zero ou inativa; não são automaticamente atividade persistente.
A duração observada em anos é cinco vezes o número de intervalos e não estima a
duração real além das fronteiras da janela. Não se realiza análise de sobrevivência
ou redefinição da censura da Fase 4A nesta comparação.

## Extensão diagnóstica

As 106 células que atingem alta magnitude somente em 2020–2025 pertencem aos
grupos primários: 85 moderadas, 17 baixas e quatro sem ocorrência. O indicador
`diagnostic_only_high_flag` registra essa condição sem transferi-las de grupo.

No grupo sem ocorrência primária, 674 células passam a ter algum NAT→TMP no
diagnóstico, somando 11,74 mil ha; somente quatro atingem a classe alta. Portanto,
“nova ocorrência” e “nova alta magnitude” são condições distintas.

## Distribuição espacial e limites

O mapa apresenta os centroides das células coloridos pelos grupos primários. O
contraste visual mostra maior presença de grupos moderado/alto no setor oriental
e meridional do domínio e de células sem ocorrência em grande parte do setor
ocidental. Existem exceções e conjuntos altos ao norte; não se definem clusters,
regiões administrativas ou frentes históricas por inspeção visual.

Os centros ponderados e raios quadráticos médios são calculados em Albers equal-area
para cada grupo e intervalo com área positiva. O grupo sem ocorrência não possui
centro ponderado NAT→TMP no período primário: campos vazios significam indefinido,
não coordenadas zero. Essas localizações aproximam a distribuição da área por
centroides de células, sem localizar exatamente os pixels convertidos.

Bioma principal associa a área à célula, não à porção dos pixels dentro do bioma.
Áreas somadas entre intervalos não são deduplicadas espacialmente. Ausência de
pastagem intermediária detectada não comprova conversão direta. A análise é
descritiva e não inclui significância, autocorrelação ou atribuição causal.

## Produtos e continuidade

- `domain_nat_group_cells_v1.csv`: 24.889 linhas, vínculo 1:1 por `cell_id`.
- `schema.ini`: configuração dessa tabela, sem a opção CharacterSet rejeitada.
- `domain_nat_group_period_summary_v1.csv`: 32 linhas, quatro grupos × oito períodos.
- `domain_nat_group_cr_states_v1.csv`: 128 linhas, contagens e áreas por estado.
- `domain_nat_group_primary_biome_v1.csv`: áreas associadas ao bioma principal.
- `domain_nat_group_trajectory_summary_v1.csv`: 16 combinações grupo/eixo/janela.
- `domain_nat_group_cell_trajectories_v1.csv`: 99.556 registros; não associar 1:1
  sem filtrar eixo e janela.
- Duas figuras: comparação temporal e distribuição espacial dos grupos.
- JSON separado de validação e hashes dos produtos.

O aprofundamento seguinte pode comparar esses grupos em unidades regionais
previamente definidas, mantendo as mesmas métricas, para avaliar a heterogeneidade
espacial sem escolher limites apenas para explicar os resultados observados.
