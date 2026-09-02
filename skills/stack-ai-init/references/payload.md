# Carga util

Autoridade sobre: o que a skill distribui, o que fica de fora e por que, como a carga e guardada e como ela e alterada.

## Onde a carga fica

```text
assets/stack/          os 86 arquivos, com os nomes com ponto mapeados para dot-
assets/estrutura.json  diretorios vazios e symlinks a recriar na instalacao
```

`assets/stack/` e a fonte de verdade da stack, nao uma copia de outro lugar e nao um gerador. Quem mantem edita esses arquivos direto. O instalador so copia o que esta la.

## Inventario

| Grupo | Arquivos | Conteudo |
|---|---|---|
| Raiz | 3 | `AGENTS.md`, `CLAUDE.md`, `.gitignore` |
| `.agents/references/` | 1 | `speckit.md`, a regra de manutencao das fases |
| `.agents/skills/` | 51 | os 18 arquivos da `skill-creator`, as 10 fases do SpecKit em `speckit-<fase>/` e 10 skills de apoio: `caveman`, `dicionario-dados-db-scan-codebase-docs`, `grill-me`, `grilling` e a familia `ponytail` |
| `.claude/` | 1 | `settings.json`, que registra o marketplace local e liga o plugin `stack-ai` |
| `.claude-plugin/` | 1 | `marketplace.json`, o plugin local que aponta o Claude Code para `.agents/skills/`; traz `{{MARKETPLACE}}` no lugar do nome |
| `.github/` | 1 | `copilot-instructions.md` |
| `.opencode/` | 2 | `opencode.json` e `.gitignore` |
| `.specify/` | 25 | scripts em `bash/` e `powershell/`, templates, workflows, o manifesto do SpecKit, `memory/constitution.md` |
| `.vscode/` | 1 | `settings.json`, so as chaves da stack |

Nenhum symlink e nenhum diretorio vazio: as duas listas de `assets/estrutura.json` estao zeradas.

Nenhuma integracao recebe arquivo do SpecKit. O workflow de cada fase existe uma vez so, em `.agents/skills/speckit-<fase>/SKILL.md`, que e o nivel onde a descoberta de skill procura, entao a ferramenta chega nele apontando so para `.agents/skills`. Os scripts que as fases chamam vao em `.specify/scripts/`, nas duas variantes: `bash/` para Linux, macOS e WSL e `powershell/` para Windows. Sao seis de cada lado, equivalentes um a um, da mesma versao do SpecKit. A carga leva os dois conjuntos porque o time e misto.

## O que fica de fora

| Item | Motivo |
|---|---|
| `.claude/settings.local.json` | configuracao local do desenvolvedor, ja no `.gitignore` |
| `.opencode/node_modules/`, `package.json`, `package-lock.json` | dependencias instaladas pelo npm, nunca versionadas |
| `.agents/skills/stack-ai-build-project-context/` | skill em evolucao; enriquecimento nao e escopo desta skill |
| `.agents/skills/stack-ai-init/` | ela mesma; distribuir o instalador levaria a carga junto, recursivamente |
| `specs/`, `.git/`, `__pycache__/` | trabalho do repositorio, nao artefato da stack |

`.agents/references/` entra na carga com o `speckit.md`. O `contrato-da-stack.md` da `stack-ai-build-project-context` declara a pasta peca obrigatoria da stack, entao ela sempre chega no destino, mesmo com um arquivo so.

## Por que os nomes viram dot-

Cada componente de caminho iniciado por ponto e guardado com o prefixo `dot-` e volta ao ponto na instalacao. `.github/copilot-instructions.md` fica `dot-github/copilot-instructions.md`, `.opencode/.gitignore` fica `dot-opencode/dot-gitignore`.

Sao tres motivos:

1. `.opencode/.gitignore` contem a linha `.gitignore`. Guardado com o nome real, ele se auto-ignoraria dentro da carga e nunca chegaria ao repositorio.
2. Um `.gitignore` guardado no meio da carga passa a valer para a subarvore onde esta, o que muda o `git status` deste repositorio sem que ninguem perceba.
3. Pastas `.claude/` e `.github/` aninhadas dentro de uma skill sao candidatas a varredura por ferramenta que procura `SKILL.md` ou command.

## Diretorios vazios e symlinks

Git nao guarda diretorio vazio e a carga nao guarda symlink, entao os dois vivem em `assets/estrutura.json` e sao recriados na instalacao. As duas listas estao vazias: a carga nao tem diretorio vazio e nao leva symlink nenhum.

O instalador continua sabendo criar symlink declarado em `assets/estrutura.json`, e cai para copia real quando `os.symlink` falha. A capacidade existe para o dia em que a carga precisar dela.

## Como o Claude Code enxerga as skills

Por plugin local, nao por symlink. Sao dois arquivos versionados, ambos na carga:

| Arquivo | Papel |
|---|---|
| `.claude-plugin/marketplace.json` | declara o plugin `stack-ai`, com `source` em `./.agents`, o que faz o Claude Code varrer `.agents/skills/` |
| `.claude/settings.json` | registra o marketplace do proprio repositorio e liga o plugin para quem clonar |

Sao os dois unicos arquivos da carga que nao chegam byte a byte: ambos trazem o placeholder `{{MARKETPLACE}}`, que a instalacao troca pelo nome derivado do destino. A lista esta em `SUBSTITUIVEIS`, em `scripts/instalar_stack.py`.

O `source` aponta para `./.agents` e nao para a raiz. Com a raiz, um `claude plugin install` copia o repositorio inteiro para o cache do desenvolvedor; com `.agents`, copia so a stack.

O primeiro start do Claude Code na pasta registra o marketplace e o segundo ja carrega as skills. As skills sao lidas ao vivo de `.agents/skills/`: skill nova ou editada vale na hora, sem comando de atualizacao.

O plugin e sempre `stack-ai` e o marketplace e sempre `stack-ai-<diretorio de destino>`. O registro de marketplaces do Claude Code, em `~/.claude/plugins/known_marketplaces.json`, e da maquina e guarda um caminho so por nome: dois repositorios que se batizassem igual disputariam a mesma entrada, e o perdedor carregaria as skills do outro sem nenhum aviso. Com o marketplace unico e o plugin fixo, a chave `stack-ai@stack-ai-<repo>` nao colide e a invocacao continua `/stack-ai:<skill>` em todo lugar.

A carga nao leva symlink porque symlink quebra fora do Linux. No Windows o Git so materializa symlink com `core.symlinks=true` mais Modo de Desenvolvedor, e sem isso o checkout deixa um arquivo de texto no lugar do diretorio, que o Claude Code descarta. Pasta sincronizada por OneDrive, Dropbox ou iCloud tem o mesmo efeito no macOS.

## Tres arquivos que o destino nunca recebe por cima

A carga nao leva `README.md`, nem na raiz nem em `.agents/skills/`: documentacao de projeto e do destino, e catalogo de skill vira arquivo que ninguem atualiza. O instalador ainda protege o nome, entao um `README.md` que ja exista no destino nunca e tocado.

Estes dois chegam so quando faltam no destino, porque o destino escreve conteudo proprio neles:

| Arquivo | Regra |
|---|---|
| `AGENTS.md` | preservado sempre, mesmo com `--sobrescrever`; e onde o destino descreve o proprio projeto |
| `CLAUDE.md` | preservado sempre, mesmo com `--sobrescrever` |

Outros dois nao sao substituidos, sao somados: `.gitignore` recebe as linhas que faltam e `.vscode/settings.json` e `.claude/settings.json` recebem as chaves que faltam.

O `.gitignore` tem uma excecao, a linha `/specs`, decidida em tres casos:

| Destino | O que a instalacao faz |
|---|---|
| Sem pasta `specs/` | acrescenta `/specs`; a stack e spec first e trata a spec como descartavel |
| Com pasta `specs/` ja no `.gitignore` | nao mexe, e a pasta segue ignorada pela regra que o destino ja tinha |
| Com pasta `specs/` versionada | nao acrescenta, e a pasta segue versionada |

A constante e `LINHA_CONDICIONAL_SPECS`, em `scripts/instalar_stack.py`.

## Alterar a carga

Edite `assets/stack/` direto, com o nome mapeado para `dot-` onde houver ponto. Nao existe script de sincronizacao e nao existe repositorio molde de onde puxar.

O fluxo de qualquer mudanca:

1. Editar o arquivo em `assets/stack/`, ou criar o diretorio da skill nova.
2. Se a mudanca envolver diretorio vazio ou symlink, declarar em `assets/estrutura.json`. As duas listas estao vazias hoje.
3. Rodar os testes: `cd scripts && python3 -m unittest test_instalar_stack`.
4. Instalar em um destino descartavel e conferir: `python3 scripts/instalar_stack.py instalar --destino <pasta vazia>`.
5. Atualizar o inventario deste arquivo quando a contagem mudar.

Para saber se um repositorio ja instalado ficou para tras, o comando e `python3 scripts/instalar_stack.py verificar --destino <raiz>`. Ele compara arquivo a arquivo por sha256 e devolve `igual`, `divergente` ou `ausente`.
