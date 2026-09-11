# Manutenção da stack

> Este documento é para quem mantém ou evolui a stack de IA. Se você só quer usar a stack, leia [`stack-de-ia.md`](stack-de-ia.md) e [`speckit.md`](speckit.md).

Aqui estão as mudanças nos arquivos da stack dentro do repositório: `.agents/`, `.claude/`, `.claude-plugin/`, `.github/`, `.opencode/`, `.specify/`, `.vscode/` e `docs/stack-ai/`. Atualizações das ferramentas locais (Copilot, OpenCode, Claude Code) são responsabilidade de cada ferramenta e documentadas por elas mesmas.

Sempre crie uma branch dedicada e abra um Pull Request para revisão antes de incorporar qualquer mudança ao repositório principal.

## Sumário

- [Como o SpecKit está organizado](#como-o-speckit-está-organizado)
- [Mapa de atualização](#mapa-de-atualização)
- [Como atualizar o SpecKit](#como-atualizar-o-speckit)
- [Como atualizar o OWASP Secure Agent Playbook](#como-atualizar-o-owasp-secure-agent-playbook)
- [Como atualizar os demais arquivos da stack](#como-atualizar-os-demais-arquivos-da-stack)

---

## Como o SpecKit está organizado

Para manter e atualizar o SpecKit com segurança, é preciso entender o papel de cada grupo de arquivos.

### Skills: o que de fato executa

```text
.agents/skills/
├── speckit-specify/SKILL.md
├── speckit-clarify/SKILL.md
├── speckit-plan/SKILL.md
├── speckit-tasks/SKILL.md
├── speckit-analyze/SKILL.md
├── speckit-implement/SKILL.md
├── speckit-checklist/SKILL.md
├── speckit-constitution/SKILL.md
├── speckit-converge/SKILL.md
└── speckit-taskstoissues/SKILL.md
```

Esses arquivos são o **núcleo operacional do SpecKit**. Cada `SKILL.md` contém o fluxo completo de uma fase: o que o agente deve fazer, em que ordem, quais verificações realizar e como tratar os resultados. Quando você invoca `/speckit-specify`, é a skill correspondente que o agente executa.

As skills são autossuficientes e agnósticas de ferramenta: funcionam no Copilot, no OpenCode ou em qualquer outro assistente que consiga ler o arquivo.

As fases ficam no mesmo nível das demais skills do repositório porque a descoberta enxerga um nível abaixo do diretório configurado, no formato `<local>/<nome>/SKILL.md`. Fase nova precisa só de um diretório próprio em `.agents/skills/`, nomeado `speckit-<fase>`.

> **Tenha cautela ao alterar skills do SpecKit.** Qualquer mudança nesses arquivos afeta diretamente o comportamento do fluxo SDD para toda a equipe. Antes de editar, entenda o impacto na fase inteira. Teste o fluxo após a mudança e documente o motivo no Pull Request.

A regra que o agente segue ao editar uma fase está em `.agents/references/speckit.md`. Ela não é repetida aqui.

### Nenhuma ferramenta guarda arquivo de comando

As três ferramentas descobrem as 10 fases sozinhas lendo `.agents/skills/`, e o nome do gatilho sai do diretório da skill, igual nas três: `/speckit-specify`.

Não crie arquivo de comando em `.claude/commands/`, `.github/agents/`, `.github/prompts/` ou `.opencode/command/` para expor uma fase. Se algum dia uma ferramenta exigir isso, o arquivo aponta para o `SKILL.md` e não carrega workflow.

### A pasta `.specify/`

```text
.specify/
├── templates/         <- base de comparação para atualizar as skills
├── scripts/           <- scripts de suporte chamados em tempo de execução
├── integrations/      <- manifestos de integração
├── workflows/         <- registro de workflows
└── memory/
    └── constitution.md  <- intencionalmente vazio; não governa o fluxo
```

Os templates em `.specify/templates/` são a origem das skills em `.agents/skills/speckit-*/`. Eles não fazem parte do fluxo de execução diário e permanecem no repositório como referência para atualizações futuras: ao avaliar uma nova versão, você compara os templates novos com as skills geradas anteriormente para identificar o que mudou e precisa ser incorporado.

O que é ativo no dia a dia são os scripts em `.specify/scripts/`, chamados pelas skills em tempo de execução, por exemplo para criar a branch da funcionalidade.

O arquivo `.specify/memory/constitution.md` é mantido **intencionalmente vazio** e não governa o fluxo: as regras de governança vivem nas próprias skills de fase.

Os arquivos de configuração pessoal do SpecKit ficam no `.gitignore` e não são versionados. Cada desenvolvedor configura os seus na própria máquina conforme a ferramenta que usa, e a ausência deles não impede o uso do SpecKit: o fluxo trata a ausência como configuração padrão.

---

## Mapa de atualização

| Grupo de arquivo | Ao atualizar o SpecKit | Ao evoluir o projeto |
|---|---|---|
| Skills em `.agents/skills/speckit-*/` | Merge manual com atenção, preservando os ajustes da equipe | Raramente; abrir PR com justificativa clara |
| Templates em `.specify/templates/` | Atualizar, para servirem de base na comparação seguinte | Não se aplica |
| Scripts em `.specify/scripts/` e manifestos em `.specify/integrations/` | Substituição direta pela versão nova | Não se aplica |
| Arquivo `.specify/memory/constitution.md` | Manter vazio; não incorporar o template novo | Manter vazio; as regras vivem nas skills de fase |
| Checklists e templates criados pela equipe | Preservar, porque são da equipe e não do SpecKit | Atualizar conforme os padrões do projeto evoluem |
| Pasta `.agents/`, fora de `skills/speckit-*/` | Não se aplica | Ciclo normal do projeto |
| Arquivos `AGENTS.md` e `.github/copilot-instructions.md` | Não se aplica | Ciclo normal do projeto |
| Pasta `docs/stack-ai/` | Atualizar a versão citada em `speckit.md` e em `stack-de-ia.md` | Espelhar toda alteração na skill `stack-ai-init`, na mesma entrega |
| Pasta `.agents/skills/owasp-playbook/upstream/` | Não se aplica | Nunca editar o conteúdo; a versão nova chega pela `stack-ai-init`, conforme a seção [Como atualizar o OWASP Secure Agent Playbook](#como-atualizar-o-owasp-secure-agent-playbook) |
| Arquivo `.agents/skills/owasp-playbook/SKILL.md` | Não se aplica | Nunca receber ajuste do projeto; é o mesmo arquivo em todo repositório, e o que é do projeto vai para a ponte |
| Arquivo `.agents/security/mapa-cwe-guia.md` | Não se aplica | A tabela de tradução chega da stack; as demais seções são do projeto e são preservadas na atualização |

---

## Como atualizar o SpecKit

1. Identifique a nova versão em [github.com/github/spec-kit](https://github.com/github/spec-kit) e leia o changelog para entender o que mudou em cada fase.
2. Para cada skill em `.agents/skills/speckit-*/`, compare a skill atual com o template novo da fase correspondente. Aplique o merge manualmente, preservando qualquer ajuste que a equipe tenha feito.
3. Substitua diretamente os scripts em `.specify/scripts/`, nas duas versões: `bash/` e `powershell/`. Se a nova versão criar ou remover fase, crie ou remova o diretório correspondente em `.agents/skills/`.
4. Atualize os templates em `.specify/templates/` para refletir a nova versão: eles servem de base de comparação para a próxima atualização.
5. Mantenha `.specify/memory/constitution.md` vazio. As regras de governança vivem nas próprias skills de fase, então não incorpore o conteúdo do novo `constitution-template.md`.
6. Teste o fluxo ponta a ponta (`specify`, `plan`, `tasks`, `implement`) em uma funcionalidade de exemplo.
7. Atualize a versão registrada na nota de [`speckit.md`](speckit.md) e na tabela de skills de [`stack-de-ia.md`](stack-de-ia.md), e abra um Pull Request descrevendo o que mudou.

---

## Como atualizar o OWASP Secure Agent Playbook

A skill `owasp-playbook` tem três partes. O `SKILL.md` é agnóstico e idêntico em todo repositório. A pasta `upstream/` é cópia parcial e literal do repositório [OWASP/secure-agent-playbook](https://github.com/OWASP/secure-agent-playbook), com os 17 plays. A ponte `.agents/security/mapa-cwe-guia.md` é onde o projeto entra: tradução de CWE para tópico do guia, sinais, auditores, exceções, saídas e roteamento da correção.

Regras:

- Nunca edite arquivo dentro de `upstream/`. A atualização substitui a pasta inteira, e editar o conteúdo cria obra derivada sob a cláusula ShareAlike dos dados OWASP.
- Nunca ajuste o `SKILL.md` para o projeto. Sinais, auditores e exceções do projeto vão para a ponte, nas seções que já existem lá com os títulos que a skill procura.
- A varredura de travessão do projeto não se aplica a `upstream/`. O conteúdo é em inglês e não é nosso.
- Correção no conteúdo do playbook vira Pull Request no repositório de origem.

A versão nova não é baixada aqui: ela chega pela `stack-ai-init`, que distribui a cópia já preparada. O procedimento é o da seção [Como atualizar os demais arquivos da stack](#como-atualizar-os-demais-arquivos-da-stack), com um passo a mais, porque a `stack-ai-init` cria e substitui arquivos mas não apaga: play removido ou renomeado na versão nova ficaria órfão. Antes de autorizar a atualização, apague a pasta `upstream/` da skill; a instalação recria a pasta inteira a partir da versão distribuída.

```bash
rm -rf .agents/skills/owasp-playbook/upstream
```

Depois da atualização, confira se as seções da ponte que o projeto preencheu continuam lá. A `stack-ai-init` preserva arquivo que diverge da carga, então a ponte preenchida só muda com autorização explícita de substituição, e nesse caso o conteúdo do projeto precisa ser reaplicado à mão.

---

## Como atualizar os demais arquivos da stack

Os arquivos da stack são distribuídos pela skill `stack-ai-init`. Ela sabe comparar o que está instalado aqui com a versão que ela distribui hoje, e sabe atualizar o que ficou para trás.

**Para saber o que divergiu**, peça uma conferência. Ela não escreve nada e devolve um relatório com o que está igual, o que está diferente e o que está faltando:

```text
Use a skill `stack-ai-init` para verificar a instalação da stack no repositório em <caminho da raiz>.
```

**Para atualizar o que ficou para trás**, autorize explicitamente. Sem autorização, a skill preserva tudo que encontrar:

```text
Use a skill `stack-ai-init` no repositório em <caminho da raiz> para atualizar os arquivos
da stack que estão desatualizados.

Autorizo substituir os arquivos que divergirem da versão distribuída hoje.
```

Três arquivos nunca são substituídos por essa atualização, porque o conteúdo deles é do projeto: `AGENTS.md`, `CLAUDE.md` e o `README.md` da raiz.

Alguns arquivos divergem por natureza e vão aparecer como diferentes em toda conferência: o `.gitignore`, o `.vscode/settings.json` e o `.claude/settings.json` recebem acréscimos da stack e mantêm o que o time já tinha. Divergência neles é esperada e não é problema.
