# Comparação regional dos grupos NAT→TMP por bioma principal

Data: 15/09/2026. Extensão descritiva da Fase 4A. Mesmos quatro grupos primários,
oito intervalos e classes congeladas. As regiões são os biomas principais já
atribuídos às células; não foram desenhados limites a partir dos resultados.

## Populações

| Grupo primário | Amazônia | Cerrado |
|---|---:|---:|
| Sem ocorrência | 9645 | 1568 |
| Máxima baixa | 2222 | 2665 |
| Máxima moderada | 1698 | 4493 |
| Máxima alta | 648 | 1950 |


As células de bioma principal Amazônia são 14.213; as de Cerrado, 10.676. A fração
de células altas é 4,56% e 18,27%, respectivamente. Isso é frequência de células
selecionadas retrospectivamente, não taxa de conversão ou comparação de áreas iguais.

## Diferença regional no balanço C–R

| Período | Índice C–R do grupo alto — Amazônia | Índice C–R do grupo alto — Cerrado |
|---|---:|---:|
| 1985–1990 | -0.890 | -0.635 |
| 1990–1995 | -0.796 | -0.478 |
| 1995–2000 | -0.683 | -0.193 |
| 2000–2005 | -0.237 | 0.028 |
| 2005–2010 | 0.297 | -0.025 |
| 2010–2015 | 0.621 | 0.095 |
| 2015–2020 | 0.415 | -0.037 |
| 2020–2025 * | 0.157 | -0.420 |


*2020–2025: diagnóstico incluído.*

O índice agregado positivo da coorte no domínio completo oculta diferenças:
na Amazônia, o grupo alto tem consolidação dominante pela regra 2:1 em 2010–2015
(+0,621) e 2015–2020 (+0,415). No Cerrado, os índices +0,095 e −0,037 são mistos.
Logo, o balanço agregado não sustenta afirmar consolidação dominante em toda a
coorte ou nos dois biomas. Índices regionais também não classificam todas as
células da região e não são médias dos índices individuais.

No diagnóstico, o grupo alto amazônico permanece misto (+0,157), enquanto o
Cerrado atinge reposição dominante (−0,420). O grupo moderado também difere:
Amazônia −0,192 (misto), Cerrado −0,523 (reposição dominante).

## Magnitude e participação

Os dois conjuntos de células altas apresentam máximo NAT→TMP em 2000–2005:
0,840 milhão ha associado à Amazônia e 1,276 milhão ha ao Cerrado. Entre
2010–2015 e 2015–2020, o grupo alto amazônico mantém praticamente a área
(179,6 e 179,5 mil ha), enquanto o Cerrado cai de 977,8 para 366,2 mil ha.
Essa diferença regional esclarece a queda observada na coorte completa.

A participação do grupo alto na área de todas as células de cada bioma principal
passa, entre o pico e o último intervalo primário, de 94,22% para 72,50% na
Amazônia e de 90,91% para 74,28% no Cerrado. No diagnóstico, as participações são
57,02% e 70,25%. As tabelas incluem intensidade relativa ao estoque natural
inicial, hectares por célula, composição de pastagem intermediária e estados C–R.

## Sensibilidade às células transbioma

São 582 células com frações positivas em ambos os biomas, das quais 163 pertencem
ao grupo alto: 77 de bioma principal Amazônia e 86 de Cerrado. A leitura principal
inclui todas; a sensibilidade remove essas células dos numeradores e denominadores,
sem recalcular grupos ou transferir qualquer célula entre regiões.

No grupo alto amazônico, as células transbioma respondem por 30,06% da área
em 1985–1990, 37,11% em 1990–1995 e 6,11% em 2015–2020. Seu peso inicial é
relevante e os totais não podem ser chamados de área convertida estritamente
dentro da Amazônia.

Ao removê-las, os índices amazônicos de 2010–2015 e 2015–2020 são +0,618 e
+0,409: ambos continuam consolidação dominante. No Cerrado são +0,080 e −0,039,
continuando mistos. A diferença central permanece nessa verificação descritiva;
isso não é teste de significância, independência ou prova de generalização.

## Trajetórias e suporte espacial

As sequências dos dois eixos centrais são resumidas por bioma, grupo e janela
primária/completa, com contagem de mudanças, sequências constantes e máximo
episódio consecutivo. As métricas reproduzem as mesmas regras de episódios;
não se reestima a tipologia da Fase 4A. Um episódio longo pode ser zero/inativo,
e sua duração observada não equivale à duração real além da janela.

A atribuição utiliza bioma principal, aplicando à região os fluxos de toda a
célula. A retirada das transbioma é uma sensibilidade, não uma repartição exata
dos pixels. Células de um único bioma ainda podem ter porções fora dos biomas
analisados. Não se produzem clusters, inferência causal ou significância espacial.
Ausência de pastagem detectada não comprova conversão direta.

## Produtos e próximo aprofundamento

Script `09d_compare_nat_tmp_groups_by_biome.py`; seis CSVs de populações, períodos,
estados C–R, sensibilidade, contexto por célula e resumo de trajetórias; figura
comparável com escalas iguais; JSON de validação e hashes. Não é necessário GEE.

O próximo aprofundamento pode examinar persistência e reversões do grupo alto
em cada bioma, comparando as sequências completas e o suporte dos fluxos, para
distinguir consolidação dominante recorrente de balanços concentrados em poucos
intervalos ou células. Esse passo deve manter as decisões e classes existentes.
