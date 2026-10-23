# Instalar o registro completo validado

Extraia `uncertain_pair_crosstab_full_validation_record_v1.zip` na raiz do repositório, preservando as pastas. O ZIP é incremental em relação ao repositório completo: inclui todos os arquivos do pacote de entrada, os nove CSVs recebidos, a cópia sintética aceita, os produtos derivados e os novos registros. Não remove arquivos já existentes.

O `README.md` fornecido é completo, atualizado após a aceitação da auditoria direcionada da idade v2 e a validação completa dos pares incertos em 21/10/2026. Substitui a versão correspondente do pacote de entrada. O README e as instruções anteriores foram arquivados em `docs/history/uncertain_pair_crosstab_pre_full_20261020_v1/`.

Os arquivos do piloto, scripts, testes, configurações e relatórios históricos foram preservados byte a byte. Os novos resultados completos ficam em `outputs/native/uncertain_pair_crosstab_v1/full/` e `outputs/validation/uncertain_pair_crosstab_v1/full/`. As tabelas adicionais ficam em `outputs/summary/uncertain_pair_crosstab_v1/full/`.

O inventário `PACKAGE_SHA256.csv` cobre todos os arquivos deste ZIP, exceto ele próprio. O inventário original foi arquivado junto aos documentos anteriores. Os produtos nativos são dados e podem ser mantidos fora do Git conforme a política do repositório, mas devem acompanhar o pacote de reprodução e seus hashes.

Nenhuma publicação GitHub, depósito DOI, nova execução GEE ou mudança na matriz v4.3/events-v5 foi feita. Este pacote não contém arquivos do restante do repositório que não estavam no pacote de entrada.
