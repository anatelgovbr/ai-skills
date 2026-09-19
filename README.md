# ai-skills

Skills agnósticas de agente de IA mantidas pela Anatel.

Uma skill agnóstica não pertence a um projeto específico: as regras, os formatos e os critérios de qualidade que ela aplica não dependem da linguagem, do sistema ou da estrutura de nenhum projeto da Anatel em particular.

## Instalação

Copie a pasta da skill desejada para o diretório de skills do seu projeto.

Depois de instalar, os prompts prontos para usar cada skill estão em [`docs/prompts-exemplo.md`](./docs/prompts-exemplo.md).

## Skills Disponíveis

Para origem, revisão e licença das skills de terceiros, consulte [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md).

| Skill | Use para | Acionamento |
|---|---|---|
| `caveman` | Comprimir o formato das respostas | `/caveman`, `/caveman lite` ou `/caveman ultra` |
| `ciclo-design` | Executar ciclo crítico de design com referência real | Automático ou `/ciclo-design` |
| `conformidade-de-escrita-normativa` | Analisar a conformidade de redação de minutas de atos normativos brasileiros e entregar apenas o relatório de conformidade | Automático ou pelo nome exato |
| `dicionario-dados-db-scan-codebase-docs` | Gerar ou verificar dicionários de dados e changelogs estruturais | Automático ou pelo nome exato |
| `docx` | Criar, editar ou analisar documentos Word | Automático ou pelo nome exato |
| `escrita-em-linguagem-simples-pt-br` | Escrever ou reescrever textos em Linguagem Simples para o cidadão ou outro público-alvo informado | Automático ou pelo nome exato |
| `frontend-design` | Projetar ou reformular interface frontend | Automático ou pelo nome exato |
| `gauntlet-loop-forge` | Criar ou otimizar prompt de execução do Gauntlet Loop | Automático ou pelo nome exato |
| `pdf` | Criar, editar ou analisar arquivos PDF | Automático ou pelo nome exato |
| `pptx` | Criar, editar ou analisar apresentações PowerPoint | Automático ou pelo nome exato |
| `recapitulacao-resumo-ata-relato-reuniao` | Produzir recapitulação e lista de ações de reunião a partir de transcrição, gravação, anotações ou URL do Teams | Automático ou pelo nome exato |
| `redacao-conformidade-de-escrita-normativa` | Redigir, reescrever ou avaliar minutas de atos normativos brasileiros conforme regras de redação legislativa, com relatório de conformidade | Automático ou pelo nome exato |
| `skill-creator` | Criar, editar, melhorar e avaliar skills | Automático ou `/skill-creator` |
| `stack-ai-build-project-context` | Investigar uma codebase e gerar ou atualizar a base operacional para agentes | Automático ou pelo nome exato |
| `stack-ai-init` | Instalar, atualizar ou verificar a stack em outro repositório | Automático ou pelo nome exato |
| `writing-for-agents` | Escrever documentação consumida por agentes e modificar `AGENTS.md` ou `CLAUDE.md` | Automático ou pelo nome exato |
| `xlsx` | Criar, editar ou analisar planilhas | Automático ou pelo nome exato |
