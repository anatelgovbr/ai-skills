---
name: stack-ai-init
description: >
  Instala a estrutura minima da stack de IA em um repositorio de destino: AGENTS.md,
  CLAUDE.md, .agents/skills/ com a skill-creator, o SpecKit completo em .specify/ e as
  integracoes de Claude Code, GitHub Copilot, OpenCode e VS Code. Copia os artefatos
  como estao, preserva symlinks e permissoes e nao toca no que o destino ja escreveu.

  Use quando o pedido for instalar, adicionar, levar, copiar, portar, provisionar ou
  atualizar a stack de IA, o SpecKit, o AGENTS.md ou as skills em outro repositorio;
  preparar um projeto para trabalhar com agentes; ou conferir se uma instalacao
  existente ainda bate com o que a skill distribui.

  Nao usar para popular o AGENTS.md com conhecimento do projeto, investigar codigo ou
  criar skill nova: isso e da stack-ai-creator e da skill-creator.
---

# stack-ai-init

Deposita a estrutura minima da stack de IA na raiz de um repositorio de destino. Nada mais.

Esta skill nao le a codebase de destino, nao infere nada sobre ela e nao escreve conteudo novo. Ela carrega uma copia dos artefatos da stack e os coloca no lugar, preservando o que ja existe la. Quem enriquece a stack com o conhecimento do sistema e a `stack-ai-creator`, depois, em outra rodada.

## Regra de nao enriquecimento

Toda a decisao ja esta tomada dentro de `assets/`. Voce nao escolhe arquivo, nao adapta conteudo, nao renomeia pasta, nao preenche `AGENTS.md`, nao ajusta caminho para a arquitetura do destino e nao acrescenta item por achar que faz sentido. Se o desenvolvedor pedir algo alem da instalacao, diga que isso e outra tarefa e siga com a instalacao.

Se voce acha que a carga precisa mudar, o caminho e alterar a carga neste repositorio e sincroniza la (ver `references/payload.md`), nunca improvisar durante a instalacao de um destino.

## O que e instalado

| Grupo | Conteudo |
|---|---|
| Raiz | `AGENTS.md`, `CLAUDE.md`, `README.md`, `.gitignore` |
| `.agents/references/` | `speckit.md`, a regra de manutencao das fases |
| `.agents/skills/` | catalogo de auditoria, a skill `skill-creator`, as 9 fases do SpecKit em `speckit-<fase>/` e 10 skills de apoio (`caveman`, `dicionario-dados-db-scan-codebase-docs`, `grill-me`, `grilling` e a familia `ponytail`) |
| `.claude/` | o symlink `skills` para `../.agents/skills` |
| `.github/` | `copilot-instructions.md` |
| `.opencode/` | `opencode.json` e `.gitignore` |
| `.specify/` | scripts, templates, workflows, manifestos e `memory/constitution.md` |
| `.vscode/` | as tres chaves `chat.*` que apontam o Copilot para `.agents/skills/` |

Inventario completo, exclusoes e o motivo de cada uma: `references/payload.md`.

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

Diga o que foi criado, o que foi preservado e por que, e o que ficou pendente. Depois aponte os dois proximos passos que pertencem ao desenvolvedor:

1. preencher o `AGENTS.md` com contexto, dependencias e limites de escrita do projeto;
2. instalar uma das ferramentas suportadas, se ainda nao usar nenhuma.

Se o repositorio de destino ja for versionado, lembre que a mudanca deve ir em branch propria e Pull Request.

## Regras de colisao

| Situacao | O que acontece |
|---|---|
| Arquivo da stack ausente no destino | criado |
| Arquivo da stack identico ao da carga | ignorado, sem ruido |
| Arquivo da stack diferente | preservado; so muda com `--sobrescrever` |
| `AGENTS.md`, `CLAUDE.md`, `README.md` ja existentes | preservados sempre, mesmo com `--sobrescrever` |
| `.gitignore` do destino | recebe so as linhas que faltam, sob o cabecalho `# Stack de IA` |
| `.vscode/settings.json` do destino | recebe so as chaves e subchaves que faltam; valor ja definido nao muda |
| `.vscode/settings.json` com comentario ou virgula sobrando | nao e tocado; o relatorio traz as chaves para acrescentar a mao |
| Symlink ja existente apontando para outro lugar | preservado e reportado |
| `os.symlink` indisponivel (Windows sem privilegio) | copia real no lugar, reportada como `symlink-degradado` |

Rodar de novo no mesmo destino nao muda nada e sai com codigo 0.

## Vocabulario do relatorio

`criado`, `substituido`, `mesclado`, `symlink`, `ignorado-igual` sao resultados limpos. `ignorado-existe`, `ignorado-protegido`, `symlink-degradado`, `manual`, `divergente` e `ausente` sao pendencias que o desenvolvedor precisa ver. `erro` interrompe a confianca no resultado e deve ser investigado antes de qualquer outra coisa.

Codigos de saida: `0` sem pendencia, `1` com pendencia, `2` erro.

## Conferir uma instalacao antiga

```bash
python3 <caminho-desta-skill>/scripts/instalar_stack.py verificar --destino <raiz do destino>
```

Nao escreve nada. Compara arquivo a arquivo por sha256 e devolve `igual`, `divergente` ou `ausente`. `AGENTS.md`, `CLAUDE.md` e `README.md` aparecem como `proprio-do-destino`, porque ali divergir e o esperado.

## Manutencao da carga

A carga e uma copia dos artefatos da raiz deste repositorio e envelhece quando a raiz muda. `scripts/sincronizar_payload.py verificar` acusa a deriva e `aplicar` a corrige. Detalhes e as duas excecoes mantidas a mao estao em `references/payload.md`.
