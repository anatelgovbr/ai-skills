# ai-skills

Skills agnósticas de agente de IA mantidas pela Anatel.

Uma skill agnóstica não pertence a um projeto específico: as regras, os formatos e os critérios de qualidade que ela aplica não dependem da linguagem, do sistema ou da estrutura de nenhum projeto da Anatel em particular.

Toda skill publicada aqui está no seu estado original, exatamente como foi criada, sem nenhum ajuste feito para um projeto específico. Se uma skill permitir algum tipo de ajuste ou configuração para o seu caso, o `SKILL.md` dela e o [`docs/prompts-exemplo.md`](./docs/prompts-exemplo.md) explicam como e quando fazer isso.

## Instalação

Copie a pasta da skill desejada para o diretório de skills do seu projeto.

Depois de instalar, os prompts prontos para usar cada skill estão em [`docs/prompts-exemplo.md`](./docs/prompts-exemplo.md).

## Referência

| Skill | Descrição |
|---|---|
| [`stack-ai-init`](./skills/stack-ai-init/) | Instala a estrutura mínima da stack de IA na raiz de um repositório: `AGENTS.md`, `CLAUDE.md`, `.agents/` com skills e references, a skill `owasp-playbook` com o OWASP Secure Agent Playbook, o SpecKit em `.specify/` e as integrações de Claude Code, GitHub Copilot, OpenCode e VS Code. Preserva o que o destino já tem e pode ser rodada quantas vezes for preciso. É a estrutura sobre a qual a [`stack-ai-build-project-context`](./skills/stack-ai-build-project-context/) trabalha depois. [Prompts de exemplo](./docs/prompts-exemplo.md#stack-ai-init). |
| [`stack-ai-build-project-context`](./skills/stack-ai-build-project-context/) | Investiga a codebase de um repositório que já tem a stack de IA instalada e transforma o que descobre em base operacional para agentes: inventário e regras no `AGENTS.md`, skills de fluxo, references de detalhe e guardrails, todos derivados de evidência do próprio código. Roda depois da [`stack-ai-init`](./skills/stack-ai-init/), que é quem deixa essa estrutura no repositório. [Prompts de exemplo](./docs/prompts-exemplo.md#stack-ai-build-project-context). |
| [`dicionario-dados-db-scan-codebase-docs`](./skills/dicionario-dados-db-scan-codebase-docs/) | Cria, atualiza e verifica dicionários de dados e changelogs estruturais de banco de dados, escrevendo apenas o que a codebase, scripts de banco e documentação comprovam. [Prompts de exemplo](./docs/prompts-exemplo.md#dicionario-dados-db-scan-codebase-docs). |
| [`gauntlet-loop-forge`](./skills/gauntlet-loop-forge/) | Transforma uma ideia, um objetivo, uma especificação ou um prompt já existente em um prompt pronto para colar, com a técnica de loop de verificação acrescentada. O resultado tem sempre duas partes: o prompt original, reproduzido sem alteração, e um bloco de loop escrito depois dele. No método Gauntlet Loop, quem constrói não aprova o próprio trabalho, o padrão de qualidade precisa ser conferível e toda repetição tem um limite finito de rodadas. [Prompts de exemplo](./docs/prompts-exemplo.md#gauntlet-loop-forge). |
| [`ciclo-design`](./skills/ciclo-design/) | Recebe um objetivo e uma referência real, identifica o que torna essa referência boa e executa um construtor com três críticos independentes, cada um olhando uma coisa, até que todos aprovem o resultado ou o limite de rodadas seja atingido. [Prompts de exemplo](./docs/prompts-exemplo.md#ciclo-design). |
| [`recapitulacao-resumo-ata-relato-reuniao`](./skills/recapitulacao-resumo-ata-relato-reuniao/) | Transforma transcrição, anotações ou gravação de uma reunião em uma recapitulação e em uma lista de ações com responsável, usando só o que está na fonte, sem decisão, prazo ou responsável inventado. [Prompts de exemplo](./docs/prompts-exemplo.md#recapitulacao-resumo-ata-relato-reuniao). |
| [`reescrita-em-linguagem-simples-pt-br`](./skills/reescrita-em-linguagem-simples-pt-br/) | Reescreve texto, arquivo ou página em Linguagem Simples, em português do Brasil, para o público informado ou para o cidadão, preservando fatos, condições, prazos e citações. [Prompts de exemplo](./docs/prompts-exemplo.md#reescrita-em-linguagem-simples-pt-br). |
| [`redacao-conformidade-de-escrita-normativa`](./skills/redacao-conformidade-de-escrita-normativa/) | Redige, reescreve e avalia minutas de ato normativo brasileiro conforme regras fixas de redação legislativa, com relatório de conformidade em dezessete dimensões; não opina sobre mérito, competência ou constitucionalidade. [Prompts de exemplo](./docs/prompts-exemplo.md#redacao-conformidade-de-escrita-normativa). |
| [`conformidade-de-escrita-normativa`](./skills/conformidade-de-escrita-normativa/) | Entrega só o relatório de conformidade da redação de uma minuta de ato normativo, nas mesmas dezessete dimensões, com as regras dentro do próprio `SKILL.md`, em arquivo único. [Prompts de exemplo](./docs/prompts-exemplo.md#conformidade-de-escrita-normativa). |
