# Carga util

Autoridade sobre: o que a skill distribui, o que fica de fora e por que, como a carga e guardada e como ela e atualizada quando a raiz deste repositorio muda.

## Onde a carga fica

```text
assets/stack/          os 93 arquivos, com os nomes com ponto mapeados para dot-
assets/estrutura.json  diretorios vazios, symlinks e o hash dos arquivos manuais
```

`assets/stack/` e uma copia dos artefatos da raiz deste repositorio, nao um gerador. O instalador so copia o que esta la.

## Inventario

| Grupo | Arquivos | Conteudo |
|---|---|---|
| Raiz | 4 | `AGENTS.md`, `CLAUDE.md`, `README.md`, `.gitignore` |
| `.agents/references/` | 1 | `speckit.md`, a regra de manutencao das fases |
| `.agents/skills/` | 51 | catalogo de auditoria, os 18 arquivos da `skill-creator`, as 9 fases do SpecKit em `speckit-<fase>/` e 10 skills de apoio: `caveman`, `dicionario-dados-db-scan-codebase-docs`, `grill-me`, `grilling` e a familia `ponytail` |
| `.claude/` | 0 | so o symlink `skills` |
| `.github/` | 1 | `copilot-instructions.md` |
| `.opencode/` | 2 | `opencode.json` e `.gitignore` |
| `.specify/` | 33 | scripts em `bash/` e `powershell/`, templates, workflows, manifestos, references, `memory/constitution.md` |
| `.vscode/` | 1 | `settings.json`, so as chaves da stack |

Mais 1 symlink, declarado em `assets/estrutura.json`. Nenhum diretorio vazio: a carga nao tem mais nenhum.

Nenhuma integracao recebe arquivo do SpecKit e a carga nao leva symlink de fase. O workflow de cada fase existe uma vez so, em `.agents/skills/speckit-<fase>/SKILL.md`, que e o nivel onde a descoberta de skill procura, entao a ferramenta chega nele apontando so para `.agents/skills`. Os scripts que as fases chamam vao em `.specify/scripts/`, nas duas variantes: `bash/` para Linux, macOS e WSL e `powershell/` para Windows. Sao sete de cada lado, equivalentes um a um, da mesma versao do SpecKit. A carga leva os dois conjuntos porque o time e misto.

## O que fica de fora

| Item | Motivo |
|---|---|
| `.claude/settings.local.json` | configuracao local do desenvolvedor, ja no `.gitignore` |
| `.opencode/node_modules/`, `package.json`, `package-lock.json` | dependencias instaladas pelo npm, nunca versionadas |
| `.agents/skills/stack-ai-creator/` | skill em evolucao; enriquecimento nao e escopo desta skill |
| `.agents/skills/stack-ai-init/` | ela mesma; instalar o instalador levaria a carga junto, recursivamente |
| `specs/`, `.git/`, `__pycache__/` | trabalho do repositorio, nao artefato da stack |

`.agents/references/` entra na carga com o `speckit.md`. O `contrato-da-stack.md` da `stack-ai-creator` declara a pasta peca obrigatoria da stack; o sincronizador leva o que existir nela na raiz deste repositorio.

## Por que os nomes viram dot-

Cada componente de caminho iniciado por ponto e guardado com o prefixo `dot-` e volta ao ponto na instalacao. `.github/copilot-instructions.md` fica `dot-github/copilot-instructions.md`, `.opencode/.gitignore` fica `dot-opencode/dot-gitignore`.

Sao tres motivos:

1. `.opencode/.gitignore` contem a linha `.gitignore`. Guardado com o nome real, ele se auto-ignoraria dentro da carga e nunca chegaria ao repositorio.
2. Um `.gitignore` guardado no meio da carga passa a valer para a subarvore onde esta, o que muda o `git status` deste repositorio sem que ninguem perceba.
3. Pastas `.claude/` e `.github/` aninhadas dentro de uma skill sao candidatas a varredura por ferramenta que procura `SKILL.md` ou command.

## Diretorios vazios e symlinks

Git nao guarda diretorio vazio e a carga nao guarda symlink, entao os dois vivem em `assets/estrutura.json` e sao recriados na instalacao. Hoje a lista de diretorios vazios esta zerada e so o symlink e recriado:

- 1 symlink: `.claude/skills` para `../.agents/skills`, que e como o Claude Code enxerga as skills de uma vez, sem manutencao por skill. Ele so alcanca um nivel, que e exatamente onde as fases do SpecKit ficam, entao elas aparecem junto com as demais skills. Copilot e OpenCode chegam nelas pelo mesmo diretorio, sem segundo caminho configurado.

Recriar o symlink em vez de guarda lo tambem resolve o destino que nao aceita symlink: quando `os.symlink` falha, o instalador copia o diretorio real e reporta `symlink-degradado`.

## Os tres arquivos mantidos a mao

Sao os unicos que a carga nao copia da raiz, porque a versao daqui carrega conteudo que nao pertence a outro repositorio:

| Arquivo | Diferenca |
|---|---|
| `.vscode/settings.json` | a carga leva as chaves `chat.*`, `files.eol` e os blocos de EOL e encoding por linguagem; fica de fora o `[php]` com `iso88591` e a cor de janela do Peacock (`workbench.colorCustomizations` e `peacock.remoteColor`), que sao deste projeto |
| `.agents/skills/README.md` | a carga leva o catalogo sem as secoes da `stack-ai-creator` e da `stack-ai-init`, que nao sao distribuidas, e sem a dependencia entre elas |
| `README.md` | a carga descreve a stack que chega no destino; a versao daqui cita skills que nao sao distribuidas |

`assets/estrutura.json` guarda o hash da versao de origem que foi revisada da ultima vez. Quando a origem muda, `verificar` acusa `revisar-manualmente` ate alguem olhar a variante e decidir.

## Atualizar a carga

```bash
python3 scripts/sincronizar_payload.py verificar         # acusa deriva, sai 1 se houver
python3 scripts/sincronizar_payload.py aplicar           # reescreve a carga a partir da raiz
python3 scripts/sincronizar_payload.py aceitar-manuais   # registra o hash de origem ja revisado
```

O fluxo depois de qualquer mudanca na raiz da stack:

1. `verificar` para ver o que mudou.
2. `aplicar` para trazer os arquivos novos, alterados e removidos.
3. Se aparecer `revisar-manualmente`, abrir a variante correspondente em `assets/stack/`, decidir se a mudanca da origem pertence a ela, editar se pertencer e rodar `aceitar-manuais`.
4. `verificar` de novo, ate sair limpo.
5. Rodar os testes: `python3 -m unittest test_instalar_stack test_sincronizar_payload`.

Skill nova instalada na raiz entra na carga automaticamente. Se ela nao deve ser distribuida, acrescente o caminho a constante `EXCLUIDOS` de `scripts/sincronizar_payload.py` antes de rodar `aplicar`.
