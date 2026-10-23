# Instalar o registro de aceitação do piloto r2

Extraia `entry_reentry_pilot_acceptance_record_v1.zip` na raiz do repositório, preservando as pastas. O pacote é incremental: conserva os scripts, a configuração, as referências históricas e os testes da revisão r2, acrescentando os quatro CSVs nativos recebidos, os cinco produtos do validador, os logs, o registro de aceitação e a interpretação. O README fornecido é completo e atualizado.

Os arquivos originais do piloto, do código e das referências foram preservados. O texto anterior do README, das instruções e do método está arquivado em `docs/history/entry_reentry_before_pilot_acceptance_v1/`. O relatório original de validação não foi editado. A revisão complementar compara eventos de 2024/2025 às tabelas do piloto de pares incertos, sem nova comparação ao raster de eventos.

Os três relatórios de estágios diferentes mantêm suas funções: verificação local de software, revisão de implementação r2 e nova aceitação nativa. O novo registro é a autoridade desta etapa. O inventário `PACKAGE_SHA256.csv` cobre todos os arquivos deste ZIP, exceto ele próprio.

Não é necessário repetir tarefas GEE. Este ZIP não contém exportador completo, publicação GitHub, DOI, nova matriz científica ou revisão dos eventos de estado. A próxima etapa é preparar a ampliação às 24.889 células e oito intervalos, preservando o piloto aceito.
