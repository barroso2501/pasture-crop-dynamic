# Fase 4 — resumo dos achados espaciais e encerramento

- **Data:** 15 de setembro de 2026.
- **Situação:** Fase 4 encerrada no escopo de trajetórias das células e exploração espacial e temporal descritiva acordado.
- **Destino no GitHub:** `docs/analysis/phase4_spatial_findings_and_closure_v1.md`.
- **Domínio:** 24.889 células hexagonais canônicas.
- **Períodos:** sete quinquênios primários de 1985–2020 e extensão diagnóstica 2020–2025, incluída nas análises.

## 1. Escopo e definições

As análises relacionaram a localização das células, a magnitude de conversão NAT→TMP e o balanço entre consolidação e reposição, acompanhando sua variação e persistência temporal. Foram utilizados os produtos espaciais e métricos aceitos e as classes congeladas da Fase 3. A Fase 4A produziu trajetórias descritivas para os 12 indicadores; o aprofundamento interpretativo concentrou-se nos dois eixos centrais: magnitude NAT→TMP e balanço C–R.

**NAT→TMP** é a área com vegetação natural no início e agricultura temporária ao final de um intervalo. Essa definição por estados inicial e final não exige conversão direta nem exclui pastagem intermediária. **Consolidação (C)** é PAS→TMP; **reposição (R)** é NAT→PAS. O índice C–R é `(C−R)/(C+R)`: reposição dominante abaixo de −1/3, misto entre −1/3 e +1/3, inclusive, e consolidação dominante acima de +1/3. Ausência dos dois fluxos corresponde a C–R inativo e índice indefinido pela regra canônica.

Cada célula foi atribuída a um grupo fixo segundo a **maior classe NAT→TMP atingida em 1985–2020**. A coorte de alta magnitude contém as células com classe alta em ao menos um quinquênio primário, utilizando o limite congelado de aproximadamente 357,793 hectares por intervalo. Esse conjunto é retrospectivo e não representa uma amostra aleatória ou um cluster espacial.

| Grupo primário fixo | Células no domínio | Bioma principal Amazônia | Bioma principal Cerrado |
|---|---:|---:|---:|
| Sem ocorrência NAT→TMP primária | 11.213 | 9.645 | 1.568 |
| Magnitude máxima baixa | 4.887 | 2.222 | 2.665 |
| Magnitude máxima moderada | 6.191 | 1.698 | 4.493 |
| Magnitude máxima alta — coorte | 2.598 | 648 | 1.950 |
| **Total** | **24.889** | **14.213** | **10.676** |

“Sem ocorrência” informa somente o histórico primário NAT→TMP. Essas células podem apresentar outros fluxos intensos e não devem ser chamadas genericamente de inativas.

## 2. Distribuição espacial e concentração da conversão

A coorte representa **10,44% das células**, mas responde por **87,5% da soma das áreas NAT→TMP de 1985–2020**: 8,010 milhões de hectares, frente a 9,151 milhões no domínio. Esses valores somam áreas de transições por intervalo; não são uma apuração deduplicada de hectares únicos ao longo de toda a série.

O bioma principal Cerrado concentra **75,1% da coorte**. A proporção de células selecionadas é 18,3% no conjunto de células do Cerrado e 4,6% no da Amazônia. O contraste permanece apesar de o domínio conter mais células amazônicas, mas essas frequências não controlam a disponibilidade inicial de vegetação ou a aptidão para conversão.

A inspeção dos mapas de centroides identifica conjuntos extensos de células altas no **Cerrado central e oriental e no setor sul da Amazônia e da transição Amazônia–Cerrado**, além de conjuntos menores no norte e extremo sul do domínio. No domínio completo, as células sem ocorrência primária são mais presentes em grande parte do setor ocidental; os grupos moderado e alto aparecem mais frequentemente nos setores oriental e meridional. Essas descrições não constituem delimitações de clusters estatísticos ou regiões administrativas.

O máximo de atividade da coorte ocorre em **2000–2005**, tanto na contagem de células atualmente altas — 1.349 — como na área contínua NAT→TMP — **2,116 milhões de hectares**, ou 92,2% da área desse processo no domínio. Em 2015–2020, são 486 células altas e 0,546 milhão de hectares, 74,2% abaixo do máximo. A queda da classe alta não significa desaparecimento da atividade: nesse último quinquênio primário, 2.557 células da coorte ainda registram algum NAT→TMP.

## 3. Redistribuição espacial da área ao longo do tempo

O centro ponderado pelos hectares NAT→TMP passa de aproximadamente **52,754° W e 14,811° S**, em 1985–1990, para **49,501° W e 9,435° S**, em 2015–2020. A diferença líquida é de cerca de **692 km em direção geral norte/nordeste**.

A trajetória não é retilínea. O maior deslocamento entre centros consecutivos, de aproximadamente **430 km**, ocorre entre 2000–2005 e 2005–2010, principalmente para leste. Nesse contraste, a área associada às células amazônicas da coorte cai de 0,840 para 0,126 milhão de hectares, e sua participação na área da coorte diminui de 39,7% para 15,2%. A área associada ao Cerrado também diminui, proporcionalmente menos.

Esses movimentos descrevem **redistribuição dos pesos da atividade dentro de uma população fixa**. Não acompanham o deslocamento dos mesmos pixels, propriedades ou uma frente de conversão. Os centros foram calculados em Albers equal-area a partir dos centroides das células; são aproximações da localização dos hectares convertidos, não os centroides exatos desses pixels.

A comparação regional esclarece a queda recente: entre 2010–2015 e 2015–2020, a área NAT→TMP do grupo alto amazônico permanece praticamente constante, em 179,6 e 179,5 mil hectares; no Cerrado, cai de 977,8 para 366,2 mil hectares.

## 4. Relação entre localização, magnitude e balanço C–R

Na coorte completa, C supera R na soma dos fluxos nos três últimos quinquênios primários. Entretanto, os índices +0,098, +0,288 e +0,102 permanecem **mistos pela regra 2:1**. Índice positivo não equivale automaticamente a consolidação dominante.

A separação por bioma principal revela diferenças que o agregado ocultava:

| Período | Índice agregado do grupo alto — Amazônia | Classe | Índice agregado do grupo alto — Cerrado | Classe |
|---|---:|---|---:|---|
| 2010–2015 | +0,621 | Consolidação dominante | +0,095 | Misto |
| 2015–2020 | +0,415 | Consolidação dominante | −0,037 | Misto |
| 2020–2025 diagnóstico | +0,157 | Misto | −0,420 | Reposição dominante |

Esses índices são razões entre somas regionais dos fluxos, não médias dos índices individuais nem classes de todas as células da região. Em 2015–2020, por exemplo, 44,0% da área NAT→TMP da coorte completa ocorre em células de reposição dominante, embora C seja maior que R no agregado. A magnitude NAT→TMP e a direção C–R possuem denominadores e definições diferentes.

A maior participação recente do grupo moderado no domínio também exige qualificação: sua participação passa de 14,5% para 25,2% entre 2010–2015 e 2015–2020, enquanto sua área cai ligeiramente, de 197,2 para 186,9 mil hectares. Esse aumento relativo decorre sobretudo da queda mais intensa do grupo alto, e não de crescimento contínuo da área moderada.

A comparação com o estoque natural inicial mantém um contraste de intensidade: em 2015–2020, a razão agrupada NAT→TMP/estoque inicial válido é 2,02% no grupo alto, 0,301% no moderado e 0,0144% no baixo. A seleção retrospectiva por magnitude favorece esse contraste por construção; ele não é evidência causal independente.

## 5. Persistência regional, reversões e concentração dos fluxos

A consolidação amazônica recente tem suporte em permanência nas mesmas células. **367 das 648 células altas amazônicas** são consolidação dominante tanto em 2010–2015 como em 2015–2020, correspondendo a 56,6% do grupo. No Cerrado são **427 de 1.950**, ou 21,9%.

Essas células dominantes em ambos os quinquênios respondem por 77,5% e 64,8% da consolidação amazônica nos dois períodos, respectivamente. No Cerrado, as participações são 43,0% e 36,0%. A permanência ocorre no estado quinquenal da célula; não prova atividade contínua em cada ano ou nos mesmos pixels.

No grupo alto amazônico, **72,3% dos episódios de consolidação dominante** duram pelo menos dois quinquênios; no Cerrado, **47,0%**. As matrizes agrupadas primárias mostram manutenção de C em 80,4% das transições com origem em C na Amazônia e 62,9% no Cerrado. Cada célula pode contribuir em vários intervalos: esses percentuais não são observações independentes ou probabilidades de um modelo ajustado.

Persistência recente e reversões históricas coexistem. Em 1985–2020, 538 células altas amazônicas — 83,0% — e 1.116 do Cerrado — 57,2% — apresentam alguma reversão direta ou mediada entre dominâncias R e C. Não há uma sucessão linear universal de reposição para consolidação.

Os fluxos também são concentrados. Em 2015–2020, a seleção dos 10% de células altas com maior PAS→TMP responde por 43,9% da consolidação amazônica e 48,1% da do Cerrado. Na Amazônia, remover as 33 maiores contribuições de consolidação — seleção de 5% — reduz o índice de +0,415 para +0,317, passando a misto. Em 2010–2015, retirar as 65 maiores — seleção de 10% — mantém o índice em +0,509, ainda dominante.

A persistência em muitas células e a sensibilidade às maiores áreas são propriedades simultâneas. A retirada é uma comparação descritiva com uma população alterada, não uma justificativa para excluir células válidas nem um teste de significância.

## 6. Células transbioma e extensão diagnóstica

No domínio há **582 células que intersectam ambos os biomas**, incluindo **163 da coorte alta**. Os totais regionais atribuem os fluxos de toda a célula ao seu bioma principal; não repartem os pixels convertidos na fronteira.

A retirada das transbioma preserva a diferença recente: os índices amazônicos do grupo alto são +0,618 e +0,409 em 2010–2015 e 2015–2020, ainda consolidação dominante; no Cerrado são +0,080 e −0,039, ainda mistos. Porém, o peso das transbioma nas áreas amazônicas iniciais é relevante: 30,1% em 1985–1990 e 37,1% em 1990–1995. A sensibilidade não torna os totais uma apuração exata de conversão dentro de cada bioma.

**2020–2025 foi mantido em mapas, sequências, transições e durações**, sempre sinalizado. A coorte fixa registra 0,453 milhão de hectares NAT→TMP, 66,5% do total do domínio, e índice C–R agregado −0,254, misto.

Há 106 células que atingem alta magnitude somente no diagnóstico: 85 do grupo primário moderado, 17 do baixo e quatro sem ocorrência. Elas permanecem fora da coorte primária. Entre as células dominantes em C nos dois últimos quinquênios primários, 245 das 367 amazônicas continuam C no diagnóstico — 66,8% —, contra 198 das 427 do Cerrado — 46,4%.

## 7. Limites de interpretação

As análises permitem descrever concentração, redistribuição espacial, diferenças regionais e permanência ou mudança de estados. Sua interpretação deve preservar:

- **Suporte por célula:** mapas de centroides e centros ponderados não localizam exatamente os pixels convertidos; bioma principal não é repartição de fluxos por fronteira.
- **Grupos retrospectivos:** a coorte é selecionada pelo histórico primário, não aleatoriamente; grupo fixo e classe atual em cada intervalo são populações diferentes.
- **Contabilidade e denominadores:** contagens de células, áreas e índices agrupados são medidas distintas; somas entre períodos não deduplicam pixels.
- **Duração observada:** episódios zero/inativos são substantivos e separados da atividade persistente. Episódios nos limites da janela são censurados; não se estimam durações reais não censuradas.
- **Composição de trajetórias:** a pastagem intermediária detectada corresponde a 6,51% da área NAT→TMP somada na coorte primária; sua ausência não comprova conversão direta.
- **Natureza descritiva:** não foram realizados Moran/LISA, testes de clusters ou significância espacial, atribuição causal ou análise de sobrevivência. Essas extensões não são requisitos do encerramento acordado.

## 8. Encerramento e rastreabilidade

A Fase 4 fica encerrada no escopo executado: trajetórias das células; exploração da coorte alta; comparação contínua e dos quatro grupos no domínio; comparação por bioma e sensibilidade transbioma; episódios, persistência, reentradas, transições, reversões e concentração dos fluxos nos dois eixos centrais. Os registros e produtos aceitos das fases anteriores, as classes congeladas e as decisões 009/010 permanecem preservados.

Os produtos dispõem de verificações de população, chaves, integridade e correspondência dos estados, além de revisões numéricas e de figuras. Este documento consolida os achados e a decisão de encerramento; não substitui as validações de cada execução nem afirma que seu próprio upload ou uma atualização do plano no GitHub já ocorreu. Não é necessário reprocessar GEE ou as fases anteriores para esse encerramento.

### Documentos de origem

Os valores deste resumo foram consolidados dos relatórios executados:

1. `high_nat_tmp_spatial_exploration_v1.md` — distribuição espacial e classes da coorte.
2. [Comparação contínua da coorte](high_nat_tmp_continuous_comparison_v1.md).
3. [Comparação dos quatro grupos](domain_nat_tmp_group_comparison_v1.md).
4. [Comparação por bioma e sensibilidade transbioma](nat_tmp_groups_by_biome_v1.md).
5. [Síntese temporal, reversões e concentração](phase4_temporal_synthesis_v1.md).

Métodos e validações correspondentes devem permanecer em `docs/methods/` e `docs/validation/`, com resultados compactos e hashes nos registros de saída. A exploração espacial inicial foi entregue separadamente; seu nome acima identifica a origem sem presumir um destino de repositório que não foi conferido aqui.
