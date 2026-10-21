# Execução completa — pares incertos v1

**Piloto aprovado em 15/10/2026. Agora execute a etapa completa.** Não é necessário repetir o piloto nem alterar o código.

1. Abra `gee/19a_export_uncertain_pair_crosstab_full_v1.js` deste ZIP.
2. Copie o conteúdo completo para o Code Editor do GEE, usando o mesmo acesso aos assets e ao módulo de constantes do piloto.
3. Clique **Run**. Na aba **Tasks**, inicie as **nove tarefas** criadas.
4. Aguarde todas terminarem e os arquivos serem efetivamente gravados no Drive.
5. Envie os **nove CSVs novos juntos em um ZIP**, com seus nomes originais.

| Arquivos esperados na pasta do Drive `uncertain_pair_crosstab_v1` | Quantidade |
|---|---:|
| `canonical_uncertain_pairs_b00_v1.csv` até `canonical_uncertain_pairs_b07_v1.csv` | 8 |
| `canonical_uncertain_pairs_manifest_full_v1.csv` | 1 |

Não precisa reenviar os três CSVs do piloto: eles já foram recebidos, validados e estão preservados neste pacote. Confira a presença dos oito lotes, inclusive o último; a gravação no Drive pode terminar depois da tarefa no GEE. Se houver erro, envie a mensagem e o nome da tarefa. Evite editar parâmetros ou trocar a projeção para contornar falhas.

O conjunto completo deve ter **49.778 linhas: 24.889 células × dois pares anuais**. A análise verificará as partições e os totais do audit anterior antes de interpretar a decomposição por PAS. O resultado do piloto não encerra essa análise.

## Validação opcional no computador ou Colab

Ao validar por conta própria, coloque os nove CSVs novos em uma pasta contendo apenas eles e adicione a cópia exata de:

`outputs/native/uncertain_pair_crosstab_v1/pilot/canonical_uncertain_pairs_native_synthetic_v1.csv`

Com os arquivos deste pacote/repositório presentes, execute a partir da raiz:

```bash
python3 analysis/19b_validate_uncertain_pair_crosstab_v1.py \
  --scope full \
  --export-dir dados/uncertain_pairs_full \
  --pilot-validation outputs/validation/uncertain_pair_crosstab_v1/pilot/canonical_uncertain_pairs_pilot_v1_validation.json \
  --output-dir outputs/validation/uncertain_pair_crosstab_v1/full
```

Python 3.10 ou mais recente, sem dependências adicionais. Pode simplesmente enviar os nove novos arquivos para fazermos essa validação.
