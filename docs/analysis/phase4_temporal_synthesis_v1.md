# Síntese temporal da Fase 4: persistência, reversões e concentração

Data: 15/09/2026. Status: análises executadas e verificadas. Versão
`phase4-temporal-synthesis-v1`. Mesmos quatro grupos primários, biomas principais e
classes congeladas. Análise dos dois eixos centrais NAT→TMP e C–R, nas janelas
primária 1985–2020 e completa 1985–2025. Os produtos descritivos dos 12 eixos da
Fase 4A permanecem preservados.

## Resposta à questão central

A dominância agregada de consolidação nas células amazônicas do grupo alto em
2010–2020 tem suporte em permanência das mesmas células e também concentração
dos fluxos. Não é apenas uma troca completa de células entre quinquênios, mas
sua classificação agregada em 2015–2020 é sensível à retirada das maiores áreas
PAS→TMP. Essas duas propriedades coexistem e não estabelecem mecanismo causal.

## Permanência nas mesmas células

| Indicador do grupo alto | Amazônia | Cerrado |
|---|---:|---:|
| Células do grupo | 648 | 1.950 |
| Consolidação dominante em 2010–2015 | 478 | 757 |
| Consolidação dominante em 2015–2020 | 415 | 610 |
| Consolidação dominante em ambos | 367 | 427 |
| % do grupo dominante em ambos | 56,6 | 21,9 |
| Interseção/união dos dois conjuntos | 69,8% | 45,4% |
| % da consolidação de 2010–2015 nas células dominantes em ambos | 77,5 | 43,0 |
| % da consolidação de 2015–2020 nas células dominantes em ambos | 64,8 | 36,0 |

Esses valores tratam estados agregados de células quinquenais, não trajetórias
anuais dos mesmos pixels. A permanência das células não prova que o fluxo tenha
ocorrido continuamente durante cada ano dos dez anos observados.

## Duração de episódios

No grupo alto amazônico, 454 dos 628 episódios de consolidação dominante duram
pelo menos dois quinquênios: 72,3%. No Cerrado são 765 dos 1.627: 47,0%. As
médias de duração observada desses episódios são 11,94 e 10,29 anos,
respectivamente; não são estimativas de duração real não censurada.

Na Amazônia, 415 episódios de consolidação dominante alcançam o limite primário
de 2020; no Cerrado, 610. Censura temporal é explicitamente preservada nas
contagens de duração. Um episódio iniciado no primeiro intervalo também pode
ter começado antes da janela. Distribuições incluem episódios zero/inativos,
mas estes são separados dos indicadores de atividade persistente.

O registro completo identifica estado, início/fim observado, duração em
intervalos/anos, persistência e censura nos dois limites. Portanto, alternância
e duração multiquinquenal estão efetivamente analisadas, sem análise de
sobrevivência ou inferência sobre anos não observados.

## Transições e reversões

A matriz agrupada primária do grupo alto mostra que 80,4% das transições com
origem em consolidação dominante na Amazônia permanecem nesse estado; no
Cerrado, 62,9%. Quando a origem é mista, 58,8% passam a consolidação dominante
na Amazônia, comparados a 35,1% no Cerrado. Percentuais são por linha e agrupam
vários intervalos da mesma célula; não são probabilidades de um modelo Markov
ajustado nem observações independentes.

Na trajetória primária completa, 538 células altas amazônicas (83,0%) e 1.116
altas do Cerrado (57,2%) apresentam alguma reversão entre dominâncias R e C.
Isso não contradiz a persistência recente: uma célula pode começar com reposição
e permanecer em consolidação mais tarde. Contagens diretas e mediadas estão
separadas; uma célula pode apresentar ambas, portanto essas contagens não devem
ser somadas para obter células únicas.

| Bioma principal | Grupo | Células | Com reversão C↔R (%) | Com reentrada em algum estado (%) |
|---|---|---:|---:|---:|
| Amazon | Máxima alta | 648 | 83.0 | 34.0 |
| Amazon | Máxima baixa | 2222 | 12.3 | 10.7 |
| Amazon | Máxima moderada | 1698 | 41.3 | 18.1 |
| Amazon | Sem ocorrência | 9645 | 0.9 | 18.7 |
| Cerrado | Máxima alta | 1950 | 57.2 | 56.1 |
| Cerrado | Máxima baixa | 2665 | 15.6 | 13.5 |
| Cerrado | Máxima moderada | 4493 | 30.9 | 23.3 |
| Cerrado | Sem ocorrência | 1568 | 0.9 | 6.4 |


Reentrada em algum estado inclui a volta a um estado anteriormente observado;
não equivale a reentrada na atividade. No grupo alto primário, interrupções da
atividade C–R ocorrem em sete células amazônicas e 69 do Cerrado. A baixa
frequência de interrupção pode coexistir com mudanças entre R/M/C sem inatividade.
Os quatro grupos e ambos os eixos têm resumos de persistência, reentrada,
interrupção e retomada, além de matrizes com datas e versões agrupadas.

## Concentração dos fluxos e sensibilidade do agregado

No grupo alto amazônico, os 10% de células com maior PAS→TMP respondem por 37,0%
da consolidação em 2010–2015 e 43,9% em 2015–2020. No Cerrado são 49,0% e
48,1%. A concentração dos fluxos, portanto, não é exclusiva da Amazônia.
O tamanho de cada seleção é arredondado para cima: 65 de 648 e 195 de 1.950.

Em 2010–2015, a retirada das 65 maiores células amazônicas de consolidação
mantém o índice em +0,509, ainda dominante. Em 2015–2020, a retirada das 33
maiores (seleção de 5%) reduz o índice de +0,415 para +0,317, passando a misto;
com 65 retiradas, o índice é +0,245. A conclusão de C maior que R permanece,
mas a classificação pela razão 2:1 depende dessas maiores contribuições.

Essa retirada é uma sensibilidade descritiva de uma população alterada, não
intervalo de confiança, prova de fragilidade da classificação ou exclusão
justificada de dados. As células permanecem no conjunto principal e seus fluxos
são válidos. As tabelas também examinam concentração de reposição e NAT→TMP,
com seleções de 1%, 5% e 10% em todos os oito intervalos.

## Extensão diagnóstica

Entre as 367 células amazônicas dominantes em C nos dois últimos quinquênios
primários, 245 continuam C em 2020–2025 (66,8%), 70 são mistas, 51 passam a R
e uma fica inativa. Entre as 427 do Cerrado, 198 continuam C (46,4%), 132 são
mistas e 97 passam a R. Esses números foram conferidos pelos episódios completos
terminando em 2025 e registrados no JSON de revisão independente.

Na janela completa, células altas com alguma reversão passam de 538 para 549
na Amazônia e de 1.116 para 1.199 no Cerrado. O diagnóstico entra na sétima
transição e nos episódios completos, mas não redefine o grupo nem apaga a
persistência observada no período primário.

## Síntese e situação da Fase 4

A exploração distingue magnitude, direção do balanço e persistência. As células
altas amazônicas mostram maior permanência recente em consolidação dominante,
enquanto o Cerrado combina maior rotatividade desses estados e balanço regional
misto no fim primário. Reversões históricas e persistência recente coexistem.
Há concentração relevante de áreas, com efeito na classe agregada amazônica em
2015–2020, mas sem explicar toda a consolidação como fenômeno de poucas células.

Os dois blocos temporais restantes — episódios multiquinquenais e transições/
reversões — foram executados nos dois eixos centrais para os quatro grupos e
biomas. Esta síntese pode apoiar o encerramento documental da exploração temporal
da Fase 4 após seu registro. Não se afirma atualização automática do plano ou do
GitHub; análises espaciais inferenciais ou sobrevivência não são requisitos deste
encerramento.

## Produtos e limites

CSV de episódios completos e distribuição censurada das durações; matrizes
datadas/agrupadas; resumos de persistência/reversões; concordância recente e
concentração; tabela GIS 1:1 das 2.598 células; figura de matrizes; JSONs de
execução e revisão. O script é reproduzível com os dois ZIPs existentes, sem GEE.
As contagens das janelas se sobrepõem: 647.114 registros de transição incluem as
seis transições primárias novamente na janela completa; não são eventos únicos.

Fluxos são de toda a célula atribuída ao bioma principal, sem repartir pixels
nos limites. Preserve a sensibilidade transbioma da análise anterior. Estados
C–R não representam coberturas ou conversões anuais individuais. Durações são
observadas; estados zero/inativos são substantivos. Nenhuma significância,
cluster espacial, causalidade ou conversão direta comprovada é inferida.
