# Executar e validar o piloto de entrada/reentrada

## Execução nativa

Use somente `gee/20a_export_entry_reentry_pilot_v1.js`, com os parâmetros distribuídos. Ele cria quatro tarefas na pasta Drive `entry_reentry_pilot_v1`. A lista e a quantidade de linhas estão em `COMECE_AQUI_PT.md`. As duas células coincidem com os pilotos anteriores, mas as saídas desta etapa são novas. Não repita a extração de pares incertos.

A reconstrução lê apenas `coverage_v3`. A fonte de idade de pastagem, antiga ou v2, não é lida. O módulo de constantes instalado precisa reproduzir os assets, classes e parâmetros distribuídos. O arquivo `config/constants_entry_reentry_reference_v1.js` é um snapshot de referência, não uma instrução para substituir o módulo instalado ou seus assets de idade.

A projeção nativa é conferida nos 41 anos. A redução mantém o CRS e a transformação canônicos, `tileScale: 16` e `maxPixelsPerRegion: 100000000`. Não altere escala, domínio ou tolerâncias para contornar falhas. Os 31 casos sintéticos são reduzidos juntos em uma única região pequena.

## Validação local opcional

Pode simplesmente enviar os quatro CSVs. Se quiser validar localmente, extraia este pacote, coloque somente os quatro CSVs em `dados/entry_reentry_pilot_v1` e execute, a partir da raiz:

```bash
python3 analysis/20b_validate_entry_reentry_pilot_v1.py   --scope pilot   --export-dir dados/entry_reentry_pilot_v1   --output-dir outputs/validation/entry_reentry_v1/pilot
```

Requer Python 3.10 ou mais recente, sem pacotes adicionais. A validação do piloto deve retornar `PASS`, 2 células, 4 linhas, 2 linhas de auditoria histórica, 31 casos sintéticos e 302 passos sintéticos. O sinalizador de decomposição completa do domínio continuará falso.

O validador confere os hashes dos quatro arquivos nativos históricos de referência, a aceitação histórica, o subconjunto de quatro linhas, o código fornecido, a configuração e os casos sintéticos. Reconstitui as linhas de referência diretamente dos arquivos históricos antes de comparar o novo resultado.

Os produtos são aditivos e imutáveis. Uma reexecução com resultados idênticos é aceita; resultados diferentes não são sobrescritos. A saída inclui tabelas de células, resumo do piloto, controles históricos, auditoria e JSON de validação.

## Critérios

- Inventário exato de quatro CSVs, sem duplicatas de tentativa.
- Identidades das duas células, lotes, dois intervalos e sinalização diagnóstica.
- Assets, classes, 41 bandas, 41 projeções e parâmetros canônicos.
- Três categorias auxiliares exclusivas, cobrindo exatamente o componente de entrada pós-1985, tanto no estoque PAS em t0 como no fluxo PAS→TMP.
- Preservação dos totais e dos três componentes de origem aceitos em cada célula/intervalo.
- Controles de área com tolerância de 0,01 ha por célula e 0,001 ha nos agregados do piloto.
- Contadores de erro iguais a zero nas quatro linhas reais, nas duas auditorias e nos 31 casos sintéticos com suporte positivo.
- Suporte de teste e contagens em equivalentes de pixel ponderados: podem ser fracionários. Nenhum valor é truncado para inteiro.

## Depois do piloto

Somente após aceitar os quatro CSVs será preparado o exportador completo. A ampliação prevista cobre os oito intervalos e as 24.889 células, com referências completas e os mesmos critérios. Este pacote não contém um exportador completo nem autoriza chamar o piloto de resultado do domínio. A verificação nativa da idade auxiliar nesta etapa é limitada aos testes e às duas células; sua garantia no domínio completo permanece pendente.
