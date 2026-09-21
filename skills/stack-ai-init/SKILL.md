---
name: stack-ai-init
description: >
  Instala a estrutura minima da stack de IA em um repositorio de destino: AGENTS.md,
  CLAUDE.md, .agents/skills/ com a skill-creator, o SpecKit completo em .specify/ e as
  integracoes de Claude Code, GitHub Copilot, OpenCode e VS Code. Copia os artefatos
  como estao, preserva permissoes e nao toca no que o destino ja escreveu.

  Use quando o pedido for instalar, adicionar, levar, copiar, portar, provisionar ou
  atualizar a stack de IA, o SpecKit, o AGENTS.md ou as skills em outro repositorio;
  preparar um projeto para trabalhar com agentes; ou conferir se uma instalacao
  existente ainda bate com o que a skill distribui.

  Nao usar para popular o AGENTS.md com conhecimento do projeto, investigar codigo ou
  criar skill nova: isso e da stack-ai-build-project-context e da skill-creator.
---

# stack-ai-init

Deposita a estrutura minima da stack de IA na raiz de um repositorio de destino. Nada mais.

Esta skill nao le a codebase de destino, nao infere nada sobre ela e nao escreve conteudo novo. Ela carrega uma copia dos artefatos da stack e os coloca no lugar, preservando o que ja existe la. Quem enriquece a stack com o conhecimento do sistema e a `stack-ai-build-project-context`, depois, em outra rodada.

## Regra de nao enriquecimento

Toda a decisao ja esta tomada dentro de `assets/`. Voce nao escolhe arquivo, nao adapta conteudo, nao renomeia pasta, nao preenche `AGENTS.md`, nao ajusta caminho para a arquitetura do destino e nao acrescenta item por achar que faz sentido. Se o desenvolvedor pedir algo alem da instalacao, diga que isso e outra tarefa e siga com a instalacao.

Se voce acha que a carga precisa mudar, o caminho e editar `assets/` desta skill (ver `references/payload.md`), nunca improvisar durante a instalacao de um destino.

## O que e instalado

| Grupo | Conteudo |
|---|---|
| Raiz | `AGENTS.md`, `CLAUDE.md`, `.gitignore` |
| `.agents/references/` | `speckit.md`, a regra de manutencao das fases; `template-revisao-tecnica.md`, o formato do relatorio de revisao tecnica, para a skill de revisao do projeto |
| `.agents/security/` | `guia-seguranca.md`, 19 topicos de risco agnosticos de linguagem, com rastreio para OWASP Top 10:2025 e CWE; `mapa-cwe-guia.md`, ponte da `owasp-playbook`, com a traducao de CWE para topico e as secoes que o projeto preenche |
| `.agents/skills/` | 29 skills: a `skill-creator`, as 10 fases do SpecKit em `speckit-<fase>/`, a `owasp-playbook`, com o OWASP Secure Agent Playbook copiado em `upstream/`, e 17 skills de apoio: 4 de terceiros (`caveman`, `grill-me`, `grilling` e `writing-for-agents`), 5 da Anthropic (`frontend-design`, `docx`, `pdf`, `pptx` e `xlsx`) e 8 mantidas pela Anatel no repositorio `ai-skills` (`ciclo-design`, `conformidade-de-escrita-normativa`, `dicionario-dados-db-scan-codebase-docs`, `escrita-em-linguagem-simples-pt-br`, `gauntlet-loop-forge`, `recapitulacao-resumo-ata-relato-reuniao`, `redacao-conformidade-de-escrita-normativa` e `stack-ai-build-project-context`) |
| `.claude/` | `settings.json`, que registra o marketplace local e liga o plugin `stack-ai` |
| `.claude-plugin/` | `marketplace.json`, o plugin local que aponta o Claude Code para `.agents/skills/`; o nome do marketplace sai do diretorio de destino |
| `.github/` | `copilot-instructions.md` |
| `.opencode/` | `opencode.json` e `.gitignore` |
| `.specify/` | scripts, templates, workflows, manifestos e `memory/constitution.md` |
| `.vscode/` | as tres chaves `chat.*` que apontam o Copilot para `.agents/skills/` |
| `docs/stack-ai/` | a documentacao da stack para quem usa: indice, conceito, SpecKit, manutencao e prompts genericos |

Inventario completo, exclusoes e o motivo de cada uma: `references/payload.md`.

## Como cada ferramenta chega nas skills

Nenhuma das tres usa symlink. Cada uma tem um caminho proprio de configuracao, todos apontando para `.agents/skills/`:

| Ferramenta | Caminho |
|---|---|
| Claude Code | plugin local `stack-ai`, do marketplace local do repositorio, declarado em `.claude-plugin/marketplace.json` e ligado em `.claude/settings.json` |
| Copilot | chave `chat.agentSkillsLocations` em `.vscode/settings.json` |
| OpenCode | chave `skills.paths` em `.opencode/opencode.json` |

No Claude Code o plugin so vale a partir da segunda sessao: a primeira abertura na pasta registra o marketplace, a seguinte ja carrega as skills. Avise isso ao desenvolvedor no relatorio final.

### Nome do marketplace

O plugin chama-se sempre `stack-ai`, entao a invocacao e `/stack-ai:<skill>` em qualquer repositorio. O marketplace, nao: cada repositorio tem o seu.

O Claude Code guarda os marketplaces em um registro da maquina, em `~/.claude/plugins/known_marketplaces.json`, com um caminho so por nome. Dois repositorios com o mesmo nome de marketplace disputam a mesma entrada: o segundo perde, e passa a receber as skills do primeiro sem aviso nenhum. Como a chave de plugin e `<plugin>@<marketplace>`, basta o marketplace ser unico.

**Destino que ainda nao tem nome.** Os dois arquivos da carga trazem `{{MARKETPLACE}}` no lugar do nome, e a instalacao troca pelo nome do diretorio de destino reduzido a `[a-z0-9-]`, com o prefixo `stack-ai-`. Um destino em `sdta` recebe `stack-ai-sdta`. Nenhum parametro a informar.

**Destino que ja tem nome.** O nome do destino vale, seja ele qual for. A derivacao e so o padrao de criacao, nao um formato a impor: o que o nome precisa e ser unico entre repositorios, e um que ja existe e funciona ja cumpre isso. A instalacao le o nome em `.claude-plugin/marketplace.json`, cai para a chave `stack-ai@<marketplace>` de `enabledPlugins` quando aquele arquivo falta, e usa o que achar nos dois arquivos. Nada e acrescentado ao lado do que ja esta la, e o `verificar` nao acusa divergencia por causa do nome.

Renomear uma instalacao existente nao traz ganho: quebraria a chave `stack-ai@<marketplace>` ja ligada e deixaria uma entrada orfa no registro da maquina.

## Fluxo

### 1. Confirme o destino

O caminho da raiz do repositorio de destino e informado pelo desenvolvedor. Nunca assuma o repositorio atual, nunca deduza o destino de um arquivo aberto. Sem caminho, pergunte.

### 2. Simule

```bash
python3 <caminho-desta-skill>/scripts/instalar_stack.py simular --destino <raiz do destino>
```

Use o caminho absoluto da propria skill: o diretorio de trabalho da sessao e quase sempre o
destino ou outro repositorio, e `scripts/` relativo aponta para o lugar errado ou para nada.

### 3. Mostre o plano e peca confirmacao

Apresente o resumo por acao: quantos arquivos seriam criados, o que seria ignorado por ja existir, o que seria mesclado. Escrever na raiz de outro repositorio e acao dificil de reverter; so instale depois do "pode ir".

### 4. Instale

```bash
python3 <caminho-desta-skill>/scripts/instalar_stack.py instalar --destino <raiz do destino>
```

Use `--sobrescrever` somente quando o desenvolvedor pedir explicitamente para atualizar arquivos da stack que ja existem e divergem. Ele nunca alcanca `AGENTS.md`, `CLAUDE.md` e `README.md`.

### 5. Relate

Diga o que foi criado, o que foi preservado e por que, e o que ficou pendente. Depois aponte os tres proximos passos que pertencem ao desenvolvedor:

1. preencher o `AGENTS.md` com contexto, dependencias e limites de escrita do projeto;
2. instalar uma das ferramentas suportadas, se ainda nao usar nenhuma;
3. ler `docs/stack-ai/README.md`, que explica a stack recem-instalada, e linkar a pasta do `README.md` do projeto. Esse passo e do desenvolvedor porque a carga nunca escreve no `README.md` do destino, entao sem o link a documentacao chega e ninguem descobre que ela existe.

Se o repositorio de destino ja for versionado, lembre que a mudanca deve ir em branch propria e Pull Request.

## Regras de colisao

| Situacao | O que acontece |
|---|---|
| Arquivo da stack ausente no destino | criado |
| Arquivo da stack identico ao da carga | ignorado, sem ruido |
| Arquivo da stack diferente | preservado; so muda com `--sobrescrever` |
| `AGENTS.md`, `CLAUDE.md`, `README.md` ja existentes | preservados sempre, mesmo com `--sobrescrever` |
| `.gitignore` do destino | recebe so as linhas que faltam, sob o cabecalho `# Stack de IA` |
| `.gitignore` de destino que ja tem pasta `specs/` | recebe as linhas que faltam, menos a que ignora `specs/`: o destino fica como esta, ignorando ou versionando |
| `.vscode/settings.json` do destino | recebe so as chaves e subchaves que faltam; valor ja definido nao muda |
| `.claude/settings.json` do destino | recebe so as chaves e subchaves que faltam; marketplace e plugin ja declarados pelo time nao mudam |
| Destino que ja declara marketplace com nome diferente do derivado | o nome do destino vale; a carga adota ele nos dois arquivos e nao acrescenta chave nenhuma |
| `.vscode/settings.json` ou `.claude/settings.json` com comentario ou virgula sobrando | nao e tocado; o relatorio traz as chaves para acrescentar a mao |

Rodar de novo no mesmo destino nao muda nada e sai com codigo 0.

## Vocabulario do relatorio

`criado`, `substituido`, `mesclado`, `ignorado-igual` sao resultados limpos. `ignorado-existe`, `ignorado-protegido`, `manual`, `divergente` e `ausente` sao pendencias que o desenvolvedor precisa ver. `erro` interrompe a confianca no resultado e deve ser investigado antes de qualquer outra coisa.

Codigos de saida: `0` sem pendencia, `1` com pendencia, `2` erro.

## Conferir uma instalacao antiga

```bash
python3 <caminho-desta-skill>/scripts/instalar_stack.py verificar --destino <raiz do destino>
```

Nao escreve nada. Compara arquivo a arquivo por sha256 e devolve `igual`, `divergente` ou `ausente`. `AGENTS.md`, `CLAUDE.md` e `README.md` aparecem como `proprio-do-destino`, porque ali divergir e o esperado.

## Manutencao da carga

`assets/stack/` e a fonte de verdade da stack: quem mantem edita esses arquivos direto, com o nome mapeado para `dot-` onde houver ponto. Nao existe repositorio molde de onde puxar. Toda skill de `skills/` deste repositorio, menos a propria `stack-ai-init`, esta na carga e e copiada a mao, sem script de sincronizacao. O inventario, as exclusoes e o passo a passo de uma alteracao estao em `references/payload.md`.
