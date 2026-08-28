# Stack de IA para Desenvolvimento

Artefatos para integrar agentes de IA e o fluxo SpecKit a um repositório.

---

## Sumário

- [Stack de IA](#stack-de-ia)
  - [Introdução](#introdução)
  - [Filosofia e origem da stack](#filosofia-e-origem-da-stack)
  - [O que são modelos de IA](#o-que-são-modelos-de-ia)
  - [O que são agentes de IA](#o-que-são-agentes-de-ia)
    - [Skills disponíveis](#skills-disponíveis)
  - [O que é SDD](#o-que-é-sdd)
  - [Ferramentas de IA suportadas](#ferramentas-de-ia-suportadas)
  - [O que é o SpecKit](#o-que-é-o-speckit)
    - [Quando usar o SpecKit](#quando-usar-o-speckit)
    - [Fases do SpecKit](#fases-do-speckit)
    - [Como invocar as fases](#como-invocar-as-fases)
    - [Integrações por ferramenta](#integrações-por-ferramenta)
  - [Estrutura da stack](#estrutura-da-stack)
  - [Como começar](#como-começar)
- [Atualizações da stack](#atualizações-da-stack)
  - [Como o SpecKit está organizado neste repositório](#como-o-speckit-está-organizado-neste-repositório)
  - [Arquivos e pastas no .gitignore](#arquivos-e-pastas-no-gitignore)
  - [Mapa de atualização](#mapa-de-atualização)
  - [Como atualizar o SpecKit](#como-atualizar-o-speckit)
- [Referências](#referências)

---

## Stack de IA

### Introdução

Esta seção explica a camada de inteligência artificial integrada ao repositório. Mesmo que você nunca tenha trabalhado com IA antes, a leitura a seguir vai mostrar o que existe, como está organizado e como você pode começar a usar.

Exemplos práticos do que você pode pedir ao assistente:

- *"Explique o que o arquivo `<caminho>` faz, sem alterar nada."*
- *"Crie um plano de implementação para adicionar a funcionalidade X."*
- *"Revise o código que acabei de escrever e verifique se segue os padrões definidos em `AGENTS.md`."*

### Filosofia e origem da stack

A stack de IA deste repositório foi construída sobre um padrão aberto adotado por comunidades de desenvolvimento ao redor do mundo: o [AGENTS.md](https://agents.md). Esse padrão, hoje mantido pela Agentic AI Foundation sob a Linux Foundation e presente em mais de 60 mil projetos de código aberto (projetos cujo código-fonte é público e pode ser inspecionado por qualquer pessoa), propõe uma separação clara entre o que é escrito para humanos e o que é escrito para agentes de IA:

- **README.md**: para humanos (visão geral, contexto, como começar)
- **AGENTS.md**: para agentes (regras de codificação, restrições, padrões do projeto)

Ao seguir esse padrão, a stack se torna **agnóstica de ferramenta**: qualquer assistente de IA que respeite o `AGENTS.md` consegue trabalhar neste repositório sem configuração adicional. O contexto do projeto viaja junto com o código, não fica preso a uma ferramenta específica.

Ferramentas como GitHub Copilot, OpenCode e outras da comunidade já seguem esse padrão nativamente, o que significa que o investimento feito na stack funciona independentemente de qual ferramenta o desenvolvedor escolher usar.

> **Origem da convenção:** o `AGENTS.md` deste repositório foi estruturado com base na convenção publicada em [agents.md](https://agents.md). O padrão não possui versionamento formal; a referência de atualização é o próprio site.

O arquivo [`CLAUDE.md`](CLAUDE.md) existe apenas como ponteiro de compatibilidade para `AGENTS.md`.

### O que são modelos de IA

Um **modelo de IA** é o "cérebro" por trás do assistente: o sistema que entende o que você escreve e gera respostas. Modelos conhecidos incluem Claude, GPT e outros modelos compatíveis com ferramentas de desenvolvimento.

Neste projeto, os modelos de IA são acessados por meio de ferramentas já integradas ao fluxo de trabalho. Você não precisa acessar o modelo diretamente; a ferramenta faz isso por você.

| Ferramenta | Modelo / Provedor |
|---|---|
| GitHub Copilot | Modelos GPT ou Claude, dependendo do plano da conta |
| OpenCode | Configurável, compatível com múltiplos modelos |
| Claude Code | Modelos Claude (Anthropic) |

Os modelos evoluem com frequência. O que importa para o uso do dia a dia é a **ferramenta**; o modelo é apenas o motor por baixo.

### O que são agentes de IA

Um **agente de IA** é um assistente configurado para operar com um conjunto específico de instruções, contexto e regras. Diferente de um modelo genérico de IA que você acessa pelo navegador, um agente:

- Conhece o projeto em que está trabalhando
- Segue **guardrails** (regras que definem o que ele pode e não pode fazer, como quais arquivos pode modificar e quais padrões de código deve seguir)
- Segue um fluxo estruturado em vez de responder de forma livre

Neste repositório, as regras do agente vêm do `AGENTS.md` e as skills ficam em `.agents/skills/`, integradas às ferramentas via `.github/` (Copilot), `.opencode/` (OpenCode) e `.claude/` (Claude Code). Elas não são programas independentes; são instruções que ensinam a ferramenta de IA a agir como um especialista no contexto do projeto.

**Na prática:** quando você abre o repositório com uma dessas ferramentas e pede *"revise este código segundo os padrões do projeto"*, o agente carrega automaticamente as regras do `AGENTS.md` e entrega uma revisão contextualizada, não genérica.

#### Skills disponíveis

As **skills** são agentes especializados em uma tarefa específica. Para acionar uma, mencione o nome dela na conversa com o assistente ou use o comando correspondente (ver [Como invocar as fases](#como-invocar-as-fases)).

As skills do fluxo SpecKit são estas:

| Skill | Fase | O que faz |
|---|---|---|
| `speckit-specify` | Especificação | Transforma a descrição em linguagem natural em uma especificação estruturada |
| `speckit-clarify` | Clarificação | Levanta dúvidas e ambiguidades antes de planejar |
| `speckit-plan` | Planejamento | Produz o plano técnico de implementação |
| `speckit-tasks` | Tarefas | Decompõe o plano em tarefas granulares e sequenciadas |
| `speckit-analyze` | Análise | Analisa riscos, dependências e impactos |
| `speckit-implement` | Implementação | Implementa seguindo o plano e as tarefas definidos nas fases anteriores |
| `speckit-checklist` | Checklist | Gera o checklist de implementação da funcionalidade |
| `speckit-taskstoissues` | Issues | Converte as tarefas em issues no GitHub |
| `speckit-constitution` | Constituição | Manutenção do arquivo `constitution.md` |


Além das fases, o repositório traz skills de apoio, que não fazem parte do fluxo SDD e são acionadas quando você quiser:

| Skill | Para que serve |
|---|---|
| `skill-creator` | Cria, edita e avalia skills novas |
| `dicionario-dados-db-scan-codebase-docs` | Gera e mantém dicionário de dados e changelog estrutural a partir da codebase, dos scripts de banco e da documentação |
| `grilling`, `grill-me` | Entrevista você sobre um plano ou design antes de construir, uma pergunta por vez |
| `ponytail`, `ponytail-lite`, `ponytail-ultra` | Modo de codificação que força a solução mínima; `/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`, `/ponytail-gain` e `/ponytail-help` completam a família |
| `caveman` | Modo de resposta comprimida, em seis intensidades |

As de apoio são opt-in: nenhuma delas é acionada sozinha. A `ponytail` e a `caveman` ficam ativas na sessão até você mandar `stop ponytail` ou `stop caveman`.

`.agents/skills/` é o diretório reservado para novas skills específicas do projeto conforme forem criadas. Toda skill adicionada deve ser registrada no catálogo de auditoria em [`.agents/skills/README.md`](.agents/skills/README.md), que traz origem, versão, licença e composição de cada uma.

### O que é SDD

**[SDD](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)** (Specification-Driven Development, ou Desenvolvimento Orientado por Especificação) é uma abordagem de trabalho que coloca a especificação antes da implementação.

A ideia central é simples: antes de escrever código (implementar = traduzir uma necessidade em instruções que o computador executa), você produz uma descrição clara e estruturada do que precisa ser feito, e o agente de IA parte sempre dessa descrição. Isso evita o problema mais comum no uso de IA para código: pedir para implementar algo sem ter definido direito o que é esse "algo". Com SDD, o raciocínio vem antes da implementação.

Neste repositório, o SDD é implementado pelo framework **SpecKit** (veja [O que é o SpecKit](#o-que-é-o-speckit)). O fluxo completo vai de `especificar → clarificar → planejar → decompor → implementar`.

### Ferramentas de IA suportadas

Este repositório é **agnóstico de ferramenta**: você pode usar qualquer assistente de IA, desde que ele consiga ler o contexto do repositório (especialmente `.agents/skills/` e `AGENTS.md`).

| Ferramenta | Como instalar | Arquivos de configuração |
|---|---|---|
| **[GitHub Copilot](https://github.com/features/copilot)** | Instale a extensão "GitHub Copilot" pelo marketplace do [VS Code](https://code.visualstudio.com) e faça login com sua conta GitHub | `.github/copilot-instructions.md` e `.vscode/settings.json` |
| **[OpenCode](https://opencode.ai)** | Instale via terminal com `npm install -g opencode-ai` e configure o modelo desejado | `.opencode/opencode.json` |
| **[Claude Code](https://claude.com/claude-code)** | Instale via terminal com `curl -fsSL https://claude.ai/install.sh \| bash` e faça login com sua conta Claude | `.claude/skills` (symlink para `.agents/skills`) |

> **O que é npm?** É o gerenciador de pacotes do Node.js, uma ferramenta de linha de comando usada para instalar softwares de desenvolvimento.

Se você optar por uma ferramenta diferente das listadas acima, confirme antes que ela consegue ler `.agents/skills/` e seguir as instruções de `AGENTS.md`.

### O que é o SpecKit

> **Não é necessário instalar o SpecKit.** Toda a estrutura já está presente neste repositório. O único requisito é ter uma das ferramentas de IA listadas em [Ferramentas de IA suportadas](#ferramentas-de-ia-suportadas) instalada e configurada.

**SpecKit** é o framework de especificação que estrutura o fluxo SDD neste repositório. Ele divide o trabalho em fases sequenciais e produz documentos padronizados (especificação, plano técnico e lista de tarefas) que servem de contexto para a implementação.

> **Não substitua os arquivos do SpecKit no repositório.** Se houver uma nova versão disponível, a atualização deve ser coordenada pela equipe seguindo o processo descrito em [Atualizações da stack](#atualizações-da-stack). Substituir os arquivos sem revisão pode quebrar o fluxo para as ferramentas integradas.

> **Versão instalada:** `v0.16.6.dev0`.

#### Quando usar o SpecKit

Use o SpecKit quando a demanda for **maior, nova ou ambígua**, quando você sente que precisa pensar antes de implementar. Para correções pontuais e pequenas alterações, o fluxo direto (conversa com o agente) é suficiente.

#### Fases do SpecKit

| Fase | Comando | O que faz |
|---|---|---|
| 1. Especificação | `/speckit-specify` | Transforma a descrição em linguagem natural em uma especificação estruturada |
| 2. Clarificação | `/speckit-clarify` | Levanta dúvidas e ambiguidades antes de planejar |
| 3. Planejamento | `/speckit-plan` | Produz o plano técnico de implementação |
| 4. Tarefas | `/speckit-tasks` | Decompõe o plano em tarefas granulares e sequenciadas |
| 5. Análise | `/speckit-analyze` | Analisa riscos, dependências e impactos |
| 6. Implementação | `/speckit-implement` | Implementa seguindo o plano e as tarefas definidos nas fases anteriores |

Além das fases principais, há comandos auxiliares: `/speckit-checklist`, `/speckit-taskstoissues` e `/speckit-constitution` (mantém o arquivo `constitution.md`, hoje vazio, que pode ser preenchido pela equipe conforme o projeto evolui).

Os documentos gerados (especificação, plano, tarefas) ficam em `specs/<nome-da-funcionalidade>/`. Nesta stack, essa pasta é criada sob demanda pelo próprio SpecKit e é versionada normalmente junto com o restante do repositório.

#### Como invocar as fases

- **No Copilot (VS Code):** abra o painel de chat do Copilot, clique no nome do agente atual e selecione a skill correspondente, como `speckit-specify`.
- **No OpenCode (terminal):** digite o comando diretamente, como `/speckit-specify`.
- **No Claude Code (terminal ou app):** digite o comando diretamente, como `/speckit-specify`.

O nome é `speckit-<fase>`, com hífen, e sai do diretório da skill, então é o mesmo nas três ferramentas. Veja os caminhos em [Integrações por ferramenta](#integrações-por-ferramenta).

#### Integrações por ferramenta

**Nenhuma integração guarda arquivo do SpecKit.** O fluxo de cada fase existe uma única vez, em `.agents/skills/`, escrito de forma neutra em relação à ferramenta:

```text
.agents/skills/speckit-<fase>/SKILL.md         <- fonte única, o núcleo operacional
.specify/scripts/bash/*.sh                     <- os scripts das fases, no Linux/macOS/WSL
.specify/scripts/powershell/*.ps1              <- os mesmos scripts, no Windows
```

Não existe symlink de fase e não existe cópia. Descoberta de skill enxerga um nível abaixo do diretório configurado (`<local>/<nome>/SKILL.md`). As fases ficam nesse nível, lado a lado com as demais skills do repositório, então cada ferramenta as encontra sem configuração extra:

| Ferramenta | Como chega em `.agents/skills/` |
|---|---|
| Claude Code | `.claude/skills`, symlink para `../.agents/skills` |
| Copilot | `chat.agentSkillsLocations` em `.vscode/settings.json` |
| OpenCode | `skills.paths` em `.opencode/opencode.json` |


Regra de manutenção: [`.agents/references/speckit.md`](.agents/references/speckit.md).

### Estrutura da stack

```text
.agents/
├── references/     # Conhecimento consultivo, carregado sob demanda
│   └── speckit.md  # Regra de manutenção das fases do SpecKit
└── skills/         # Skills do projeto; catálogo de auditoria em .agents/skills/README.md
    └── speckit-<fase>/   # Fonte única do SpecKit: o fluxo de cada fase, uma vez só

.claude/
└── skills -> ../.agents/skills   # Symlink; é assim que o Claude Code enxerga as skills

.github/
└── copilot-instructions.md   # Instrução curta carregada pelo Copilot, aponta para AGENTS.md

.opencode/
└── opencode.json    # Configuração do OpenCode; aponta as skills para .agents/skills

.specify/
├── integrations/    # Manifestos com o hash de cada arquivo instalado por ferramenta
├── memory/
│   └── constitution.md   # Preenchido pela equipe via /speckit-constitution
├── references/      # Formato dos hooks de extensão e política de ignore file
├── scripts/         # Scripts chamados pelas skills em tempo de execução; bash/ e powershell/, equivalentes
├── templates/       # Templates-base dos documentos gerados pelas fases (spec, plano, tarefas, checklist, constituição)
└── workflows/        # Fluxo orquestrado specify → plan → tasks → implement, com gates de revisão

specs/               # Documentos gerados pelo SpecKit por funcionalidade (criado sob demanda)
AGENTS.md            # Regras do projeto para agentes de IA (leia antes de contribuir)
CLAUDE.md            # Ponteiro de compatibilidade para AGENTS.md
```

**O que cada pasta faz na prática:**

- `.agents/references/`: conhecimento consultivo, carregado sob demanda pelo agente em vez de vir sempre no contexto.
- `.agents/skills/`: skills do projeto. Contém a `skill-creator`, as fases do SpecKit e o catálogo de auditoria; skills específicas do projeto entram aqui conforme forem criadas.
- `.specify/integrations/`: manifestos com o hash de cada arquivo instalado por ferramenta, usados para detectar arquivos desatualizados em relação à versão instalada.
- `.specify/references/`: `extension-hooks.md`, com o formato de `.specify/extensions.yml` e as regras de leitura dos hooks, e `ignore-files.md`, com a política de ignore file usada pela fase de implementação.
- `.specify/scripts/`: scripts chamados pelas skills em tempo de execução, como a criação de branch ao especificar uma funcionalidade. Vêm em duas variantes equivalentes, `bash/` para Linux, macOS e WSL e `powershell/` para Windows.
- `.specify/templates/`: templates-base usados pelas skills sempre que uma fase gera um documento em `specs/<funcionalidade>/`. Servem também de referência ao comparar com uma nova versão do SpecKit.
- `.specify/workflows/`: define o fluxo orquestrado specify → plan → tasks → implement, com gates de aprovação entre as fases.

### Como começar

**Passo 1: Adicione a stack ao seu repositório.** Copie a estrutura para a raiz do projeto.

**Passo 2: Preencha o `AGENTS.md`** com o contexto do projeto, as dependências técnicas e o escopo e limites de escrita. Inclua skills específicas do projeto em `.agents/skills/` e registre-as em [`.agents/skills/README.md`](.agents/skills/README.md).

**Passo 3: Instale uma ferramenta** entre as listadas em [Ferramentas de IA suportadas](#ferramentas-de-ia-suportadas). A ferramenta detecta automaticamente os arquivos de configuração do projeto: ao abrir a pasta, ela lê o `AGENTS.md` e as pastas de integração correspondentes, carregando as regras do projeto sem nenhuma ação adicional sua.

**Passo 4: Para uma demanda simples,** abra o chat da ferramenta e descreva o que precisa. Exemplo:
> *"Explique como o projeto está estruturado, sem alterar nada."*

**Passo 5: Para uma demanda maior ou ambígua,** use o fluxo SpecKit, começando por `/speckit-specify`. Exemplo:
> *"Preciso adicionar uma nova funcionalidade de exportação de relatórios."*

Você **não** precisa instalar o SpecKit nem qualquer componente adicional da stack. Tudo já está configurado no repositório; o único passo é instalar a ferramenta de IA (Passo 3).

---

## Atualizações da stack

Esta seção trata de mudanças nos arquivos da stack de IA dentro do repositório (`.agents/`, `.claude/`, `.github/`, `.opencode/`, `.specify/`). Atualizações das ferramentas locais (Copilot, OpenCode, Claude Code) são responsabilidade de cada ferramenta e documentadas por elas mesmas.

Sempre crie uma branch dedicada e abra um Pull Request para revisão antes de incorporar qualquer mudança ao repositório principal.

### Como o SpecKit está organizado neste repositório

Para manter e atualizar o SpecKit com segurança, é preciso entender o papel de cada grupo de arquivos.

```text
.agents/skills/speckit-<fase>/SKILL.md             <- fonte única: o fluxo de cada fase
.specify/scripts/bash/*.sh                         <- os scripts das fases, no Linux/macOS/WSL
.specify/scripts/powershell/*.ps1                  <- os mesmos scripts, no Windows
```

O `SKILL.md` de cada fase contém o fluxo completo: o que o agente deve fazer, em que ordem, quais verificações realizar e como tratar os resultados. Ele é escrito de forma neutra em relação à ferramenta e não cita `/speckit-plan` nem `/speckit.plan`: refere a fase de forma genérica e deixa a ferramenta resolver o gatilho.

O frontmatter declara o script da fase nas duas plataformas, com o caminho completo a partir da raiz do repositório, e o corpo escolhe entre eles pela seção `Script Selection`:

```yaml
scripts:
  sh: .specify/scripts/bash/setup-plan.sh --json
  ps: .specify/scripts/powershell/setup-plan.ps1 -Json
```

As duas variantes existem porque o time é misto. São sete scripts de cada lado, equivalentes um a um, vindos da mesma versão do SpecKit. Ao atualizar, os dois conjuntos andam juntos.

As fases ficam um nível abaixo de `.agents/skills/`, que é exatamente onde a descoberta de skill procura, então nenhuma ferramenta precisa de um segundo diretório configurado. Fase nova precisa do diretório `.agents/skills/speckit-<fase>/` e de `name: speckit-<fase>` no frontmatter.

> **Tenha cautela ao alterar a fonte única.** Uma mudança em `.agents/skills/speckit-<fase>/` afeta as três ferramentas de uma vez, porque não existe segunda cópia. Teste o fluxo após a mudança e documente o motivo no Pull Request.

Os manifestos em `.specify/integrations/` guardam o hash de cada arquivo que o CLI do SpecKit instalou. Eles descrevem o layout de cópia por ferramenta, anterior à consolidação em fonte única, e ficaram históricos: servem para saber o que o CLI instalou originalmente, não o que está no disco. Nenhuma das três ferramentas tem pasta de comando aqui. Os scripts em `.specify/scripts/` e os templates em `.specify/templates/` continuam ativos, chamados pelas skills em tempo de execução a cada fase.

### Arquivos e pastas no .gitignore

Alguns itens do repositório existem apenas localmente em cada máquina e estão listados no `.gitignore` para não serem versionados. Eles devem permanecer assim:

| Item | Por que não é versionado |
|---|---|
| `.claude/settings.local.json` | Configuração local do Claude Code, não compartilhada com o time |
| `.specify/feature.json` | Ponteiro local para a funcionalidade em edição no momento; reescrito a cada troca de feature |
| `.specify/extensions/*/local-config.yml` | Configuração de extensões por máquina |
| `.opencode/node_modules/`, `.opencode/package.json`, `.opencode/package-lock.json` | Dependências do OpenCode instaladas via npm; nunca devem ser salvas no repositório |

`.specify/init-options.json` e `.specify/integration.json` **não** estão no `.gitignore`: registram a configuração de integração já instalada no repositório e são versionados normalmente.

Antes de remover qualquer item do `.gitignore`, avalie se a remoção é realmente necessária. Na dúvida, mantenha.

### Mapa de atualização

| Grupo de arquivo | Ao atualizar o SpecKit |
|---|---|
| `.agents/skills/speckit-<fase>/SKILL.md` | Merge com atenção. Comparar a fonte única com o template novo da fase, preservando ajustes feitos pela equipe. Uma comparação por fase, não três |
| `.specify/scripts/bash/` e `.specify/scripts/powershell/` | Substituição direta dos dois conjuntos na mesma versão, mantendo os nomes citados no `scripts.sh` e `scripts.ps` de cada fase |
| `.specify/templates/` | Atualizar para refletir a nova versão; servem de referência para a próxima comparação |
| `.specify/memory/constitution.md` | Manter como está — não incorporar o template novo |
| `.specify/integrations/` | Atualizado automaticamente pela ferramenta de instalação do SpecKit ao aplicar a nova versão |
| `AGENTS.md`, `.github/copilot-instructions.md` | Não se aplica |

### Como atualizar o SpecKit

1. Identifique a nova versão em [github.com/github/spec-kit](https://github.com/github/spec-kit) e leia o changelog para entender o que mudou em cada fase.
2. Para cada fase, compare o `SKILL.md` em `.agents/skills/speckit-<fase>/` com o template novo correspondente e aplique o merge, preservando qualquer ajuste que a equipe tenha feito. É uma comparação por fase; os adapters não entram nessa etapa.
2a. Fase nova precisa do diretório `.agents/skills/speckit-<fase>/` e de `name: speckit-<fase>` no frontmatter. Sem o `name` a fase não aparece com o nome certo.
3. Atualize os scripts em `.specify/scripts/bash/` e `.specify/scripts/powershell/`, sempre os dois na mesma versão, e os templates em `.specify/templates/`.
4. Mantenha `.specify/memory/constitution.md` como está.
5. Teste o fluxo ponta a ponta (`specify` → `clarify` → `plan` → `tasks` → `implement`) em uma feature de exemplo.
6. Atualize a versão registrada em [O que é o SpecKit](#o-que-é-o-speckit) e no catálogo [`.agents/skills/README.md`](.agents/skills/README.md), e abra um Pull Request descrevendo o que mudou.

---

## Referências

**Documentação interna do projeto:**

| Documento | O que contém |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Regras centrais do projeto para agentes: o que pode ser feito, padrões de código e regras de decisão |
| [`.agents/skills/README.md`](.agents/skills/README.md) | Catálogo de auditoria das skills: origem, versão, licença e composição |

**Ferramentas e padrões externos:**

| Ferramenta / Padrão | Link |
|---|---|
| VS Code | [code.visualstudio.com](https://code.visualstudio.com) |
| GitHub Copilot | [github.com/features/copilot](https://github.com/features/copilot) |
| OpenCode | [opencode.ai](https://opencode.ai) |
| Claude Code | [claude.com/claude-code](https://claude.com/claude-code) |
| Git | [git-scm.com](https://git-scm.com) |
| SpecKit | [github.com/github/spec-kit](https://github.com/github/spec-kit) |
| Padrão AGENTS.md | [agents.md](https://agents.md) |
