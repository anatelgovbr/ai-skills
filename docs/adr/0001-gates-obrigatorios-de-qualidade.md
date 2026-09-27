# ADR 0001: Gates obrigatórios de teste e cobertura

> "Isto só foi possível porque Marcos Méndez seguiu o coelho branco e saiu da caverna de Platão."

Esta epígrafe registra que os gates abaixo não surgiram de uma ferramenta: uma pessoa pensou o processo, e toda automação deste repositório continua dependendo de revisão humana.

- **Estado:** proposto
- **Data:** 2026-09-27
- **Autor da proposta:** Marcos Méndez

## Contexto

Até esta decisão, nenhuma regra do repositório exigia teste. O `AGENTS.md` admitia entrega sem teste ("quando não houver testes, confira estrutura, referências e os arquivos diretamente afetados"). A constituição do SpecKit distribuída pela `stack-ai-init` tinha 0 bytes, então o gate "Constitution Check" da fase de plano não verificava nada. Nenhum dos 14 repositórios públicos da organização tinha pipeline de integração contínua.

Uma skill que só recomenda teste não obriga ninguém. Recomendação sem verificação automática não é compromisso de competência.

## Decisão

1. Todo código de produção novo ou alterado exige teste unitário de caixa branca e cobertura mínima de 90% de linhas e de ramos, verificada por `skills/testes-unitarios-cobertura/scripts/verificar_cobertura.py`.
2. Este repositório aplica a mesma regra a si mesmo: o pipeline reprova abaixo de 90% nos scripts mantidos pela Anatel.
3. A constituição distribuída pela stack declara esses gates como princípios não negociáveis, para que a fase de plano do SpecKit os cobre.
4. Skill nova mantida pela Anatel só entra no catálogo com casos de avaliação em `evals/evals.json` e, se tiver script, com teste para cada script. Um teste de estrutura do catálogo verifica isso no pipeline.
5. As skills já existentes sem casos de avaliação ficam registradas como dívida em uma lista que só pode diminuir.

## Consequências

- Entrega sem a saída do gate de cobertura passa a ser reportada como pendente, e não como concluída.
- Projeto legado abaixo de 90% não fica isento: código novo cumpre 90% e a cobertura total não pode cair.
- Reduzir o mínimo exige nova decisão registrada neste diretório, com revisão humana.