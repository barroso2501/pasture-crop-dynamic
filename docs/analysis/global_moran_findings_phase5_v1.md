# Fase 5 — achados de autocorrelação espacial global

- Data da revisão: 15/09/2026.
- Execução aceita: `2026-09-15T19:41:37.990348+00:00`.
- Situação: produção global revisada e aceita; interpretação descritiva dos valores de Moran’s I.
- Domínio: 24.889 células; sete intervalos primários e 2020–2025 diagnóstico incluído.
- Método: grafo canônico de borda compartilhada, pesos padronizados por linha, 9.999 permutações e correção Benjamini–Yekutieli em quatro famílias previamente definidas.

## Achado principal

Todos os 104 testes apresentam Moran’s I positivo e significância após a correção.
Os valores medidos têm associação espacial positiva sob o grafo definido: células
vizinhas tendem a apresentar valores semelhantes. Essa conclusão não localiza
clusters, não implica consolidação dominante e não demonstra causalidade.

Em todos os testes, nenhuma permutação foi tão extrema quanto o observado pela
regra bilateral de distância à esperança nula. O p Monte Carlo é 0,0001, a resolução
mínima de 9.999 permutações com correção de uma unidade. Isso não significa que os
p-valores verdadeiros sejam idênticos ou exatamente 0,0001. Sua igualdade observada
não ordena a força da associação; a comparação deve considerar I e o suporte.

## Magnitudes absolutas no domínio completo

| Período | Consolidação | Reposição | NAT→TMP | Atividade bruta C–R | Balanço líquido C–R |
|---|---:|---:|---:|---:|---:|
| 1985–1990 | 0,799 | 0,770 | 0,550 | 0,783 | 0,760 |
| 1990–1995 | 0,728 | 0,734 | 0,592 | 0,736 | 0,731 |
| 1995–2000 | 0,655 | 0,700 | 0,546 | 0,695 | 0,699 |
| 2000–2005 | 0,639 | 0,689 | 0,577 | 0,672 | 0,688 |
| 2005–2010 | 0,610 | 0,681 | 0,405 | 0,647 | 0,682 |
| 2010–2015 | 0,618 | 0,659 | 0,471 | 0,628 | 0,648 |
| 2015–2020 | 0,559 | 0,614 | 0,361 | 0,595 | 0,597 |
| 2020–2025 * | 0,552 | 0,589 | 0,422 | 0,584 | 0,582 |


*2020–2025 é diagnóstico, mantido com o mesmo desenho.*

Consolidação, reposição, atividade bruta e balanço líquido apresentam valores
menores ao final primário do que no início. Reposição, atividade bruta e balanço
líquido diminuem em todos os passos primários; consolidação tem pequena elevação
em 2010–2015. NAT→TMP oscila, com I=0,592 em 1990–1995, queda a 0,405 em 2005–2010,
recuperação a 0,471 em 2010–2015 e 0,361 em 2015–2020.

Essas são diferenças observadas de autocorrelação. Os testes realizados avaliam
cada intervalo contra seu nulo de permutação, não a significância da diferença
entre datas ou de uma tendência. Menor I não demonstra dispersão geográfica,
migração de uma frente, redução da área ou desaparecimento de clusters.

O máximo NAT→TMP de área encontrado na Fase 4 em 2000–2005 não corresponde ao
máximo de I: volume do processo e semelhança entre vizinhos são medidas distintas.

## Ocorrência e magnitude contam histórias diferentes

A ocorrência de consolidação mantém associação elevada, de I=0,723 no primeiro
intervalo para 0,744 no último primário, enquanto a área de consolidação passa de
0,799 para 0,559. A ocorrência NAT→TMP também se mantém próxima entre essas
extremidades, 0,654 e 0,648, embora o I da área diminua de 0,550 para 0,361.

Esses contrastes mostram que o padrão de presença/ausência e o padrão das áreas
não são equivalentes. Não permitem inferir que os mesmos clusters ou as mesmas
células permaneceram sem mudança; a localização exige mapas e análise local.
A ocorrência de reposição cai de 0,654 para 0,552, e a de atividade C–R, de 0,655
para 0,561. Todas permanecem significativamente autocorrelacionadas.

## Métricas condicionais

O índice C–R tem I entre 0,755 e 0,799 no período primário. Isso mostra associação
entre valores semelhantes de balanço em células vizinhas ativas, não predomínio
universal de reposição ou consolidação. Sua amostra aumenta de 17.626 para 21.206
células entre as extremidades primárias, com ilhas e componentes variando.

A taxa de consolidação tem suporte crescente de 16.421 para 21.160 células; seu
I passa de 0,598 para 0,546, com valores intermediários diferentes. Taxas baseadas
no estoque natural têm suporte quase completo, entre 24.883 e 24.886 células
primárias. Ainda assim, permanecem análises condicionais com denominadores próprios.
Nenhum valor ausente foi tratado como zero e nenhuma ligação artificial foi
adicionada para atravessar lacunas de suporte.

As comparações condicionais entre datas são secundárias: além do atributo, mudam
população, conectividade e padronização dos pesos sobreviventes. Não devem ser
tratadas como diretamente equivalentes às estatísticas do domínio completo.

## Diagnóstico 2020–2025

O diagnóstico continua positivo e significativo nos 13 testes: nove completos e
quatro condicionais. NAT→TMP absoluto sobe de I=0,361 no último primário para 0,422;
consolidação absoluta passa a 0,552 e reposição a 0,589. O índice C–R condicional é
0,747 em 22.050 células ativas. Essas observações são incluídas e sinalizadas;
não substituem resultados primários nem resolvem a comparabilidade da cobertura
terminal 2025 registrada no plano.

## Alcance da validação e situação da fase

A revisão reproduziu os p-valores e todos os resumos das 104 distribuições,
contendo 1.039.896 estatísticas simuladas. Hashes do desenho, CSVs e NPZ coincidem
com a execução; ajustes BY e diagnósticos de suporte foram reconciliados.
O I observado não foi recalculado independentemente a partir dos Parquets de
origem e do grafo, não recebidos nesta revisão. A identidade do script executado
e os registros dos insumos foram conferidos. A figura de interpretação foi
recriada dos CSVs autenticados; a PNG original não foi recebida.

A Fase 5 pode ser registrada como concluída no escopo global. A próxima etapa é
Fase 6: associação local seletiva, com métricas, permutações, suporte e controle
de testes locais definidos antes de interpretar mapas. A significância global
não autoriza executar LISA automaticamente para todos os campos. O planejamento
também permite uma análise local previamente justificada sem significância
global, pois estruturas locais opostas podem se compensar.
