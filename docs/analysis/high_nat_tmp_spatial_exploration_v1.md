# Exploração espacial da coorte com alta magnitude NAT→TMP

- **Data:** 15/09/2026.
- **Coorte fixa:** 2.598 células que receberam `positive_high` em pelo menos um dos sete intervalos de 1985–2020.
- **Limiar alto congelado:** área NAT→TMP maior que 357,7931682403865 ha no intervalo.
- **Execução de origem:** `run_20260915T091255_865443Z`, Fase 4A revisão 2.
- **Natureza:** análise descritiva exploratória dos produtos aceitos, sem nova classe, ajuste de limiar, cluster ou inferência espacial formal.

## Síntese

A coorte corresponde a 10,4% das células do domínio e associa-se a 87,5% da
soma das áreas NAT→TMP nos sete intervalos. Ela é majoritariamente classificada
como Cerrado e ocupa conjuntos extensos no Cerrado central/oriental e no setor
sul da Amazônia/transição Amazônia–Cerrado. A classe alta tem sua maior contagem
em 2000–2005. Nas mesmas células, a consolidação torna-se a classe de balanço
mais numerosa em 2005–2010, 2010–2015 e 2015–2020. Entretanto, selecionar apenas
as células atualmente na classe alta em cada período produz outra leitura,
com reposição ainda frequente. Essas leituras não devem ser confundidas.

## Onde estão

| Bioma principal da célula | Células na coorte | % da coorte | Células no domínio | % das células do bioma principal que entram na coorte |
|---|---:|---:|---:|---:|
| Cerrado | 1.950 | 75,1% | 10.676 | 18,3% |
| Amazônia | 648 | 24,9% | 14.213 | 4,6% |

O predomínio do Cerrado permanece quando consideramos que o domínio tem mais
células de bioma principal Amazônia. As proporções de seleção são descritivas;
não são uma comparação controlada pela quantidade inicial de vegetação nativa,
exposição ao processo ou área apta para conversão.

Os centroides permitem identificar dois conjuntos extensos: aproximadamente
58°–52° W e 16°–11° S no setor ocidental/central da coorte, e 50°–44° W e
18°–6° S no setor oriental. São orientações geográficas aproximadas para ler a
figura, não regiões analíticas recém-definidas. Também existem grupos menores
no norte e no extremo sul do domínio. Não foram atribuídos municípios ou UFs,
pois não houve interseção com limites administrativos.

Há 163 células que cruzam os dois biomas e 51 que se estendem para fora deles.
Os totais por bioma usam o rótulo principal da célula. Eles não localizam o fluxo
NAT→TMP dentro dos pixels de um determinado bioma em células mistas. Pela mesma
razão, os 6,23 Mha acumulados associados a células de bioma principal Cerrado e
1,78 Mha associados a células de bioma principal Amazônia não são uma apuração
pixel a pixel da conversão dentro desses biomas.

Figura: `high_nat_tmp_spatial_overview_v1.png`. Pontos são centroides geográficos;
o fundo cinza representa os centroides do domínio canônico, não um mapa de
polígonos ou densidade de área.

## Em quais períodos atingem alta magnitude

| Período | Alta: Cerrado | Alta: Amazônia | Total na classe alta | % da coorte |
|---|---:|---:|---:|---:|
| 1985–1990 | 829 | 52 | 881 | 33.9% |
| 1990–1995 | 694 | 84 | 778 | 29.9% |
| 1995–2000 | 599 | 171 | 770 | 29.6% |
| 2000–2005 | 899 | 450 | 1349 | 51.9% |
| 2005–2010 | 459 | 109 | 568 | 21.9% |
| 2010–2015 | 661 | 175 | 836 | 32.2% |
| 2015–2020 | 317 | 169 | 486 | 18.7% |
| 2020–2025 * | 220 | 73 | 293 | 11.3% |


*2020–2025 é diagnóstico e usa a mesma coorte definida no período primário.*

O maior número de células na classe alta ocorre em 2000–2005: 1.349, ou 51,9%
da coorte. Nesse intervalo, 450 células têm bioma principal Amazônia, contra 52
em 1985–1990. A participação amazônica nas células atualmente altas aumenta de
5,9% para 33,4% entre esses dois intervalos. Trata-se de mudança na distribuição
das ocorrências classificadas, não uma estimativa de deslocamento de centroides
ponderados pela área ou de migração de uma fronteira.

Em 2015–2020 apenas 486 células da coorte permanecem altas, mas 2.557 registram
algum fluxo positivo: 1.535 na classe moderada e 536 na baixa. Portanto, a queda
da contagem alta não equivale a desaparecimento do processo nessas células.

Quanto à repetição, 1.097 células atingem a classe alta em apenas um intervalo,
600 em dois, 431 em três, 317 em quatro, 111 em cinco, 39 em seis e apenas três
em todos os sete. Intervalos de ocorrência não precisam ser consecutivos.
Em 1.360 células, nenhum episódio alto supera um quinquênio; em 1.238 há pelo
menos dois quinquênios altos consecutivos. Recorrência e persistência contínua
da classe são propriedades distintas.

Esses dados temporais medem número de células e classes de magnitude. A área
contínua de cada quinquênio não está nos CSVs GIS recebidos; por isso, o máximo
de contagem alta em 2000–2005 não foi chamado de máximo da área total convertida.

## Como varia o balanço C–R da coorte fixa

| Período | Reposição dominante | Misto | Consolidação dominante | Inativo |
|---|---:|---:|---:|---:|
| 1985–1990 | 1922 | 235 | 104 | 337 |
| 1990–1995 | 1737 | 369 | 272 | 220 |
| 1995–2000 | 1500 | 476 | 467 | 155 |
| 2000–2005 | 1226 | 545 | 729 | 98 |
| 2005–2010 | 897 | 596 | 1016 | 89 |
| 2010–2015 | 755 | 547 | 1235 | 61 |
| 2015–2020 | 840 | 696 | 1025 | 37 |
| 2020–2025 * | 1218 | 603 | 754 | 23 |


Reposição dominante significa NAT→PAS maior que duas vezes PAS→TMP;
consolidação dominante significa a relação inversa. Misto inclui ambas as
fronteiras 2:1; inativo significa ausência dos dois fluxos pela regra canônica.
A comparação é de fluxos agregados na célula, não de trajetórias individuais.

Na mesma população de 2.598 células, a reposição dominante passa de 1.922
(74,0%) em 1985–1990 para 840 (32,3%) em 2015–2020. A consolidação dominante
passa de 104 (4,0%) para 1.025 (39,5%), com máximo de contagem em 2010–2015:
1.235 (47,5%). A consolidação é a classe mais numerosa nos três últimos
intervalos primários, embora não alcance metade da coorte nesses intervalos.

A variabilidade individual é relevante: 1.654 células (63,7%) apresentam ao
menos uma reversão direta ou mediada entre dominâncias no período primário.
Apenas 273 têm balanço constante nos sete intervalos: 231 com reposição,
23 com consolidação, 18 inativas e uma mista. Assim, a mudança da composição
da coorte não deve ser resumida como uma sucessão linear universal.

A seleção olha retrospectivamente para células que alguma vez foram altas.
Ela evidencia associação descritiva entre histórico de alta conversão e
variação do balanço, não comprova que a conversão alta causou a consolidação.
A área natural inicial e os demais fluxos ainda precisam acompanhar uma
interpretação dos mecanismos.

## Balanço nas células atualmente altas

A leitura acima mantém as 2.598 células em todos os períodos, mesmo quando já
não estão altas. Se restringimos cada intervalo às atualmente altas, a
composição muda. Em 2015–2020, entre as 486 altas há 234 com reposição dominante
(48,1%), 122 com consolidação (25,1%), 122 mistas (25,1%) e oito inativas.

É possível registrar NAT→TMP alto e C–R inativo: o primeiro fluxo não integra
a soma NAT→PAS + PAS→TMP que define atividade C–R. Isso não é automaticamente
um erro nem permite deduzir a composição anual da trajetória NAT→TMP.

Figura: `high_nat_tmp_cr_temporal_distributions_v1.png`, com a coorte fixa à
esquerda e a seleção atualmente alta à direita. Os painéis usam escalas
verticais diferentes. Figura cartográfica por intervalo:
`high_nat_tmp_cr_balance_by_period_v1.png`, em que o contorno preto identifica
as células atualmente altas e as cores representam o balanço C–R.

## Extensão diagnóstica

Das 2.598 células primárias, 293 estão altas em 2020–2025. Outras 106 células
do domínio tornam-se altas pela primeira vez nesse intervalo e não entram
retroativamente na coorte primária; elas constituem a diferença entre as
2.598 células da coorte primária e as 2.704 alguma vez altas na série completa.

Na coorte fixa, 2020–2025 altera a tipologia C–R de 850 células e a de magnitude
NAT→TMP de 548. O balanço apresenta nova elevação da reposição dominante na
coorte; esse resultado é mantido e sinalizado, sem redefinir a leitura primária.

## Arquivos e reprodução

- `high_nat_tmp_2598_cells_v1.csv`: uma linha por `cell_id`, com contexto espacial, frequência/períodos altos, classes de magnitude e balanço nos oito intervalos. Permite join textual no ArcGIS.
- `high_nat_tmp_period_summary_v1.csv`: contagens por período, separando a coorte fixa da seleção atualmente alta.
- `high_nat_tmp_period_by_primary_biome_v1.csv`: contagens de classe alta por bioma principal e período.
- `high_nat_tmp_exploration_summary_v1.json`: métricas exploratórias e hashes dos insumos.
- Três PNGs descritos acima e `explore_high_nat_tmp_cohort.py` para reprodução.

Os quatro CSVs GIS foram autenticados durante a revisão da Fase 4A. A tabela
espacial tem 24.889 células únicas, população exatamente igual às dos CSVs GIS,
e SHA-256 igual ao registro aceito da Fase 1:

```text
70068e7ccf4bc8f91d5278a358343f5f336cf71b7a89c4466171986bcd094653
```

A seleção retorna exatamente 2.598 células; o vínculo espacial não perde ou
duplica nenhuma. O código usa os nomes reais das classes congeladas e preserva
a seleção primária durante o diagnóstico. Figuras foram inspecionadas
visualmente. Não foram calculados clusters ou significância espacial.

```bash
python explore_high_nat_tmp_cohort.py --gis-zip GIS.zip --support-csv canonical_spatial_support_attributes_v1.csv --output-dir OUTPUT
```

Para ArcGIS, crie a camada a partir da grade canônica usando o join por
`cell_id`; o CSV contém campos de texto longos e nomes que não devem ser
truncados. Prefira geodatabase ou GeoPackage se exportar a camada associada.

A próxima extensão útil é obter `nat_tmp_endpoint_ha` por célula e intervalo
para esta coorte a partir do painel Phase 2 ou das oito tabelas 08c. Isso
permitirá localizar a área convertida por período, ponderar centroides por
área e comparar atividade alta, composição de trajetórias e estoque natural
inicial sem substituir magnitude contínua por contagens de classes.
