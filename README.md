# ai-skills

Curadoria de skills de agente de IA mantida pela Anatel.

Este repositório reúne, em um só lugar, skills escritas pela Anatel e skills de terceiros selecionadas, revisadas e versionadas pela Agência.

Toda skill daqui é agnóstica: as regras, os formatos e os critérios de qualidade que ela aplica não dependem da linguagem, do sistema ou da estrutura de nenhum projeto em particular, o que permite instalá-la em qualquer repositório.

## Sumário

- [Introdução e conceitos fundamentais](#introdução-e-conceitos-fundamentais)
  - [O que é desenvolvimento apoiado por IA](#o-que-é-desenvolvimento-apoiado-por-ia)
  - [Motivação](#motivação)
  - [O que são agentes de IA](#o-que-são-agentes-de-ia)
  - [O que são skills](#o-que-são-skills)
  - [Limitações e riscos](#limitações-e-riscos)
  - [Segurança, privacidade e governança](#segurança-privacidade-e-governança)
- [Instalar uma skill](#instalar-uma-skill)
- [Skills Disponíveis](#skills-disponíveis)
- [Preparar um repositório para trabalhar com agentes](#preparar-um-repositório-para-trabalhar-com-agentes)
  - [Passo 1. Instalar a estrutura com a `stack-ai-init`](#passo-1-instalar-a-estrutura-com-a-stack-ai-init)
  - [Passo 2. Preencher com o conhecimento do sistema com a `stack-ai-build-project-context`](#passo-2-preencher-com-o-conhecimento-do-sistema-com-a-stack-ai-build-project-context)
- [Referências](#referências)

## Introdução e conceitos fundamentais

Esta seção explica os termos e os cuidados que o restante do documento pressupõe. Se você já trabalha com agentes de IA e skills, vá direto para [Instalar uma skill](#instalar-uma-skill).

### O que é desenvolvimento apoiado por IA

O desenvolvimento de software apoiado por inteligência artificial usa modelos de grande linguagem (LLM, na sigla em inglês) e agentes para apoiar o ciclo de vida do software. 
Essas ferramentas entendem linguagem natural, leem código-fonte, geram trechos de código, sugerem correções e apoiam decisões técnicas.

### Motivação

O apoio da IA ao desenvolvimento se consolidou porque ajuda a:

- aumentar a produtividade das equipes e a velocidade na escrita e na refatoração de código (reorganizar código sem mudar o que ele faz)
- reduzir erros e esforço em tarefas repetitivas e de baixo valor agregado
- facilitar a compreensão de bases de código complexas
- apoiar o aprendizado de novas linguagens, frameworks e padrões
- apoiar a escrita de testes automatizados e de documentação técnica

A IA não substitui o desenvolvedor. Ela amplia a capacidade de análise e de execução de quem já conhece o projeto e as necessidades do negócio, e é tão mais efetiva quanto maior for esse conhecimento.

### O que são agentes de IA

Um agente de IA combina um modelo de linguagem com acesso a ferramentas, execução de tarefas e gerenciamento de contexto. Em um repositório, o agente interpreta o pedido, navega pelos arquivos, cria ou modifica código e automatiza fluxos de trabalho, de forma interativa ou com maior autonomia.

### O que são skills

Uma skill é um conjunto de instruções, referências e scripts que ensina o agente a executar bem uma tarefa específica. Ela fica em uma pasta com um arquivo `SKILL.md`, segue o padrão aberto Agent Skills e funciona em qualquer ferramenta compatível, como GitHub Copilot, OpenCode e Claude Code.

Sem skill, o agente responde de forma genérica. Com skill, ele segue o procedimento, os critérios e os limites definidos para aquela tarefa.

Curar significa escolher poucas skills boas em vez de acumular muitas. Cada skill deste repositório tem uma finalidade definida, é lida e revisada antes de entrar e tem origem, versão e licença registradas.

Um conjunto grande de skills sobrecarrega o contexto do agente e piora as respostas, por isso o catálogo cresce só quando uma necessidade real justifica.

### Limitações e riscos

- O código gerado pode conter erros de lógica ou falhas de segurança.
- O agente pode produzir soluções maiores ou mais complexas do que o necessário, ou fora dos padrões do projeto.
- A dependência excessiva reduz a compreensão do código por quem o mantém.
- Quanto mais autonomia o agente recebe, maior precisa ser o cuidado com o escopo do pedido e com a revisão do resultado.

Por isso, todo código e todo documento gerado por IA passam por revisão humana crítica antes de entrar em sistema ou processo de trabalho. 
Os agentes executam, o desenvolvedor decide. As skills deste repositório reforçam simplicidade e mudanças limitadas ao pedido, mas não dispensam essa revisão.

### Segurança, privacidade e governança

O uso de ferramentas públicas com código ou dados internos pode expor informação sensível. Na Anatel, a escolha de ferramentas, os cuidados com informação sensível e a governança do uso de IA seguem o guia citado no início desta seção, documento interno acessível pela rede da Agência.

Este repositório não repete essas regras. Ele fornece as skills que as ferramentas ali indicadas usam.

## Instalar uma skill

Copie a pasta da skill desejada para o diretório de skills do seu projeto.

Nos repositórios que receberam a stack pela skill `stack-ai-init`, esse diretório é `.agents/skills/`, e as três ferramentas suportadas já estão apontadas para ele:

- GitHub Copilot, pelo `.vscode/settings.json`
- OpenCode, pelo `.opencode/opencode.json`
- Claude Code, pelo `.claude-plugin/marketplace.json`

Nos demais projetos, consulte a documentação da sua ferramenta para saber em qual pasta ela procura o `SKILL.md`.

Montar a estrutura de agentes de um repositório inteiro é outra tarefa, e quem faz isso é a skill `stack-ai-init`, no [Passo 1. Instalar a estrutura com a `stack-ai-init`](#passo-1-instalar-a-estrutura-com-a-stack-ai-init).

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
| `skill-creator` | Criar, editar, melhorar e avaliar skills | Automático ou `/skill-creator` |
| `stack-ai-build-project-context` | Investigar uma codebase e gerar ou atualizar a base operacional para agentes | Automático ou pelo nome exato |
| `stack-ai-init` | Instalar, atualizar ou verificar a stack em outro repositório | Automático ou pelo nome exato |
| `writing-for-agents` | Escrever documentação consumida por agentes e modificar `AGENTS.md` ou `CLAUDE.md` | Automático ou pelo nome exato |
| `xlsx` | Criar, editar ou analisar planilhas | Automático ou pelo nome exato |

## Preparar um repositório para trabalhar com agentes

Duas skills deste catálogo trabalham em dupla, sempre nesta ordem e em pedidos separados. A `stack-ai-init` põe a estrutura de pé. A `stack-ai-build-project-context` preenche essa estrutura com o conhecimento do sistema.

Os prompts completos das duas, com variações para cada situação, estão em [`docs/prompts-exemplo.md`](./docs/prompts-exemplo.md).

### Passo 1. Instalar a estrutura com a `stack-ai-init`

Este passo é para um repositório que ainda não tem nenhuma stack de IA instalada. Se o repositório já tiver arquivos com o mesmo nome dos da stack, como um `AGENTS.md` próprio ou configurações do VS Code, do Claude Code ou do OpenCode, pode haver conflito.

A skill não sobrescreve nada nesse caso: preserva o que existe, mescla o que dá para mesclar e lista no relatório o que ficou pendente. Resolver esses conflitos é decisão sua, depois da instalação.

A skill deposita na raiz do repositório de destino:

- os arquivos que os agentes leem, `AGENTS.md` e `CLAUDE.md`
- as skills deste catálogo e outras de apoio, em `.agents/skills/`
- as fases do SpecKit, em `.specify/`
- um guia de segurança, em `.agents/security/`
- as integrações do GitHub Copilot, do OpenCode e do Claude Code
- a documentação da stack, em `docs/stack-ai/`

Ela não lê o código do destino e não escreve nada sobre o projeto. O que já existe no destino é preservado.

Para conhecer a stack antes de instalar, leia a documentação que ela leva, em [`skills/stack-ai-init/assets/stack/docs/stack-ai/README.md`](./skills/stack-ai-init/assets/stack/docs/stack-ai/README.md).

Antes de pedir, tenha em mãos o caminho da pasta raiz do repositório de destino, Python 3 instalado na máquina e uma sessão da sua ferramenta de IA com acesso a esta skill.

O jeito mais simples é abrir a sessão neste repositório clonado. Também funciona copiar a pasta `skills/stack-ai-init` para o diretório de skills de um projeto seu.

O prompt para pedir a instalação está em [`docs/prompts-exemplo.md`, seção "Instalar a stack em um repositório novo"](./docs/prompts-exemplo.md#instalar-a-stack-em-um-repositório-novo).

A skill simula a instalação, mostra o plano com o que vai criar, o que vai ignorar por já existir e o que vai mesclar, e só escreve depois da sua confirmação.

Ao terminar, ela relata o que foi criado, o que foi preservado e o que ficou pendente. `AGENTS.md`, `CLAUDE.md` e `README.md` do destino nunca são sobrescritos. Rodar de novo no mesmo repositório não muda nada.

Depois da instalação, três coisas ficam com você:

1. instalar uma das ferramentas suportadas, se ainda não usa nenhuma
2. ler `docs/stack-ai/README.md` no repositório de destino e linkar essa pasta no `README.md` do projeto
3. abrir a mudança em uma branch com Pull Request, se o repositório for versionado

No Claude Code, as skills aparecem a partir da segunda sessão aberta na pasta.

Mais tarde, a mesma skill confere se a instalação continua igual à versão distribuída hoje e, com a sua autorização explícita, atualiza os arquivos que ficaram para trás.

Os prompts estão nas seções ["Conferir uma instalação antiga"](./docs/prompts-exemplo.md#conferir-uma-instalação-antiga) e ["Atualizar arquivos da stack que ficaram para trás"](./docs/prompts-exemplo.md#atualizar-arquivos-da-stack-que-ficaram-para-trás).

### Passo 2. Preencher com o conhecimento do sistema com a `stack-ai-build-project-context`

A skill investiga o código do repositório para descobrir como o sistema é construído e como se desenvolve nele, e transforma o que encontra em base de trabalho para os agentes:

- inventário e regras no `AGENTS.md`
- skills para os fluxos que se repetem
- arquivos de referência em `.agents/references/`
- guardrails, alertas que avisam quando um código foge do padrão do projeto

Cada item vem acompanhado da evidência no código, com caminho, linha e contagem. Ela não implementa funcionalidade, não revisa código e não escreve documentação para pessoas.

Ela já vem instalada em `.agents/skills/` pelo passo 1, junto com a `skill-creator`, de que depende para empacotar skills novas. Abra a sessão da sua ferramenta de IA no repositório de destino, com Python 3 disponível.

Se a ferramenta oferecer agentes auxiliares, a investigação corre em paralelo e a auditoria fica independente. Sem eles a rodada continua, com essa limitação declarada no relatório.

O prompt para a primeira rodada está em [`docs/prompts-exemplo.md`, seção "Enriquecer uma stack recém instalada"](./docs/prompts-exemplo.md#enriquecer-uma-stack-recém-instalada).

A skill faz o inventário da stack, o censo do código e a investigação, e apresenta o plano antes de escrever. Você aprova, rejeita ou reduz item a item.

Ela escreve só o que foi aprovado e entrega um relatório com o que entrou em cada arquivo, o que ficou de fora e por quê, e as perguntas em aberto. Ela não faz commit: a revisão final é sua, no diff do versionamento.

A skill pode rodar de novo quantas vezes for preciso, e em cada rodada ela lê o que já está registrado e traz só a diferença. Os prompts para essas situações estão em `docs/prompts-exemplo.md`:

- [Atualizar a stack depois de uma mudança grande](./docs/prompts-exemplo.md#atualizar-a-stack-depois-de-uma-mudança-grande)
- [Enriquecer só um subsistema](./docs/prompts-exemplo.md#enriquecer-só-um-subsistema)
- [Mapear como se constrói uma unidade](./docs/prompts-exemplo.md#mapear-como-se-constrói-uma-unidade)
- [Avaliar se algo merece virar skill](./docs/prompts-exemplo.md#avaliar-se-algo-merece-virar-skill)

## Referências

| Referência | O que é |
|---|---|
| [Guia de Desenvolvimento de Software Apoiado por Inteligência Artificial](https://git.anatel.gov.br/informacao-e-conhecimento/desenvolvimento-apoiado-por-ia) | Guia interno da Anatel: conceitos, governança, GitHub Copilot como ferramenta corporativa padrão e uso de ferramentas de código aberto. Acesso pela rede da Agência |
| [Agent Skills](https://agentskills.io) | Padrão aberto que define o formato das skills e como as ferramentas as carregam |
| [AGENTS.md](https://agents.md) | Convenção aberta para o arquivo de instruções que os agentes leem na raiz do repositório |
| [Spec Kit](https://github.com/github/spec-kit) | Framework de desenvolvimento orientado por especificação usado pela stack |
| [anthropics/skills](https://github.com/anthropics/skills) | Coleção de skills da Anthropic, origem de `frontend-design` e `skill-creator` |
| [GitHub Copilot](https://github.com/features/copilot) | Ferramenta corporativa padrão na Anatel, usada no VS Code |
| [OpenCode](https://opencode.ai) | Ferramenta de linha de comando de código aberto, compatível com as skills |
| [Claude Code](https://claude.com/claude-code) | Ferramenta de linha de comando da Anthropic, compatível com as skills |
