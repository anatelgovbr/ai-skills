# ai-skills

Skills agnósticas de agente de IA mantidas pela Anatel.

Uma skill agnóstica não pertence a um projeto específico: as regras, os formatos e os critérios de qualidade que ela aplica não dependem da linguagem, do sistema ou da estrutura de nenhum projeto da Anatel em particular.

Toda skill publicada aqui está no seu estado original, exatamente como foi criada, sem nenhum ajuste feito para um projeto específico. Se uma skill permitir algum tipo de ajuste ou configuração para o seu caso, o README dela explica como e quando fazer isso.

## Instalação

Copie a pasta da skill desejada para o diretório de skills do seu projeto.

## Referência

| Skill | Descrição |
|---|---|
| [`stack-ai-init`](./skills/stack-ai-init/README.md) | Instala a estrutura mínima da stack de IA na raiz de um repositório: `AGENTS.md`, `CLAUDE.md`, `.agents/` com skills e references, o SpecKit em `.specify/` e as integrações de Claude Code, GitHub Copilot, OpenCode e VS Code. Preserva o que o destino já tem e pode ser rodada quantas vezes for preciso. Veja o README da skill para uso. |
| [`dicionario-dados-db-scan-codebase-docs`](./skills/dicionario-dados-db-scan-codebase-docs/README.md) | Cria, atualiza e verifica dicionários de dados e changelogs estruturais de banco de dados, escrevendo apenas o que a codebase, scripts de banco e documentação comprovam. Veja o README da skill para uso. |
