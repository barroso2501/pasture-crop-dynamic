# Instalar a implementação da execução completa

Extraia `entry_reentry_full_implementation_v1.zip` na raiz do repositório, mantendo as pastas e os arquivos anteriores. Execute somente `gee/20c_export_entry_reentry_full_v1.js` deste ZIP. A pasta `gee/` na raiz do pacote contém apenas esse novo script.

O pacote inclui exportador, validador completo, referências históricas para as 199.112 linhas, crosswalk canônico, testes, método, adendo do plano, instruções e README completo atualizado. O pacote inteiro do piloto aceito está preservado, sem alterações, em `provenance/entry_reentry_pilot_r2/`, para revalidação automática. Seus scripts não são tarefas desta etapa. O restante do repositório analítico não é repetido neste pacote incremental.

Os 73 CSVs novos devem voltar juntos em ZIP, com os nomes da lista `config/entry_reentry_full_expected_exports_v1.csv`. Os quatro arquivos do piloto não devem ser adicionados a essa pasta de entrada. Nenhuma nova execução GEE foi feita aqui; não há resultados nativos completos ou aceitação científica completa simulados.

O inventário `PACKAGE_SHA256.csv` cobre todos os arquivos deste pacote, exceto ele próprio. Os bytes críticos de código, configuração, referências e piloto são fixados também em `config/entry_reentry_full_source_snapshots_v1.json`. As tabelas de controle histórico fazem parte do pacote de reprodução; podem ser mantidas fora do Git conforme a política do repositório, mas devem acompanhar o validador.

README, instruções de início e este arquivo passam a apontar para a execução completa. O README anterior está arquivado em `docs/history/entry_reentry_before_full_handoff_v1/`; toda a versão anterior aceita permanece também dentro da pasta de proveniência. Não houve publicação GitHub, depósito DOI, alteração na matriz v4.3/events-v5 ou migração da origem analítica para o produto de idade.
