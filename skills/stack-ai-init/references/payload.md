# Carga util

Autoridade sobre: o que a skill distribui, o que fica de fora e por que, como a carga e guardada e como ela e alterada.

## Onde a carga fica

```text
assets/stack/          os 606 arquivos, com os nomes com ponto mapeados para dot-
assets/estrutura.json  diretorios vazios e symlinks a recriar na instalacao
```

`assets/stack/` e a fonte de verdade da stack e nao um gerador. Quem mantem edita esses arquivos direto. O instalador so copia o que esta la.

Duas skills sao a excecao: `dicionario-dados-db-scan-codebase-docs` e `gauntlet-loop-forge` tem a fonte em `skills/<nome>/` deste mesmo repositorio, e a copia em `assets/stack/dot-agents/skills/<nome>/` e feita a mao, sem script de sincronizacao. Para conferir que fonte e copia continuam iguais, rode a partir da raiz do repositorio `diff -rq -x __pycache__ skills/<nome> skills/stack-ai-init/assets/stack/dot-agents/skills/<nome>`; o comando precisa voltar vazio. Onde a fonte nao guarda `README.md`, o diff mostra so esse arquivo.

## Inventario

| Grupo | Arquivos | Conteudo |
|---|---|---|
| Raiz | 4 | `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `THIRD_PARTY_NOTICES.md` |
| `.agents/references/` | 2 | `speckit.md`, a regra de manutencao das fases; `template-revisao-tecnica.md`, o formato do relatorio de revisao tecnica, com estados, severidades, origem temporal e limite de cada celula |
| `.agents/security/` | 2 | `guia-seguranca.md`, os 19 topicos de risco agnosticos de linguagem; `mapa-cwe-guia.md`, a ponte da `owasp-playbook` |
| `.agents/skills/` | 562 | os 18 arquivos da `skill-creator`, as 10 fases do SpecKit em `speckit-<fase>/`, 6 skills de apoio (`caveman`, `dicionario-dados-db-scan-codebase-docs`, `gauntlet-loop-forge`, `grill-me`, `grilling` e `writing-for-agents`) e os 506 arquivos da `owasp-playbook`, dos quais 505 sao a copia do OWASP Secure Agent Playbook em `upstream/` |
| `.claude/` | 1 | `settings.json`, que registra o marketplace local e liga o plugin `stack-ai` |
| `.claude-plugin/` | 1 | `marketplace.json`, o plugin local que aponta o Claude Code para `.agents/skills/`; traz `{{MARKETPLACE}}` no lugar do nome |
| `.github/` | 1 | `copilot-instructions.md` |
| `.opencode/` | 2 | `opencode.json` e `.gitignore` |
| `.specify/` | 25 | scripts em `bash/` e `powershell/`, templates, workflows, o manifesto do SpecKit, `memory/constitution.md` |
| `.vscode/` | 1 | `settings.json`, so as chaves da stack |
| `docs/stack-ai/` | 5 | a documentacao da stack para quem usa: indice, conceito, SpecKit, manutencao e prompts genericos |

Nenhum symlink e nenhum diretorio vazio: as duas listas de `assets/estrutura.json` estao zeradas.

## O guia de seguranca em .agents/security/

Um arquivo, `guia-seguranca.md`, com 19 topicos numerados de S01 a S19. Cada topico traz a regra invariante, como o risco aparece, como verificar, o que nao e achado e a severidade, mais rastreio para OWASP Top 10:2025 e CWE.

E agnostico por construcao: nenhum topico cita funcao, biblioteca ou framework, porque a carga nao sabe a linguagem do destino. Cabe ao projeto traduzir cada regra para a sua stack e registrar a traducao nos proprios arquivos.

O `AGENTS.md` da carga aponta para ele na primeira linha de Guardrails Universais. Sem esse ponteiro o agente nao leria o arquivo sozinho, porque `.agents/security/` nao entra em contexto por conta propria. Como o `AGENTS.md` e protegido, o ponteiro so alcanca instalacao nova: destino que ja tem o seu precisa acrescentar a linha a mao.

A revisao referencia o topico pelo identificador, entao a numeracao e contrato. Topico novo entra no fim da lista; topico que sai deixa o numero vago, e o numero nao e reaproveitado.

## A skill owasp-playbook

Dois arquivos sao da carga: o `SKILL.md`, agnostico, que e o mesmo em qualquer repositorio, e a ponte `.agents/security/mapa-cwe-guia.md`. A pasta `upstream/` e copia parcial e literal do repositorio [OWASP/secure-agent-playbook](https://github.com/OWASP/secure-agent-playbook), e ninguem edita nada dentro dela: a atualizacao e substituicao da pasta inteira, e editar o conteudo cria obra derivada sob a clausula ShareAlike dos dados OWASP.

| Item | Valor instalado |
|---|---|
| Versao | v0.2.7 |
| Commit de origem | `79fea6b9115b55687818f8c4073844ee9ba907a6` |
| Data do commit | 2026-06-02 |
| Licenca do playbook | CC-BY-4.0, em `upstream/LICENSE.md` |
| Licenca dos dados OWASP em `upstream/data/` e `upstream/plugins/*/data/` | CC-BY-SA-4.0, em `upstream/THIRD_PARTY_NOTICES.md` |

A copia leva os 17 plays. Fica de fora so o que e formato de ferramenta ou insumo de teste:

| Retirado do upstream | Motivo |
|---|---|
| `plugins/*/agents/` | Subagentes no formato do Claude Code. Copilot e OpenCode ignoram |
| `.claude-plugin/` na raiz e em cada plugin | Manifesto de marketplace do Claude Code. A carga ja tem o seu |
| `.claude/skills/` | Duas skills com frontmatter `allowed-tools:`, especifico do Claude Code. Os plays correspondentes ja vem em `plugins/ai-security-skills/plays/` |
| `scripts/` | Extratores em Python que geram `data/` a partir dos repositorios OWASP. Nao sao usados em tempo de execucao |
| `template/` | Andaime para quem contribui com skill nova no upstream |
| `examples/mobile-*-fixture/` | Codigo vulneravel de proposito, em Kotlin, Swift e Dart. Gera ruido em varredura de seguranca do proprio repositorio |
| `.github/`, `.gitignore`, `CLAUDE.md` e `CONTRIBUTING.md` | Tooling e governanca do repositorio de origem |

A regra de travessao nao se aplica a `upstream/`: o conteudo e em ingles e nao e nosso.

Para atualizar a copia, rode a partir da raiz deste repositorio, trocando `VERSAO` pela tag nova:

```bash
VERSAO=v0.2.7
ORIGEM=$(mktemp -d)
DEST=skills/stack-ai-init/assets/stack/dot-agents/skills/owasp-playbook/upstream

git clone --depth 1 --branch "$VERSAO" https://github.com/OWASP/secure-agent-playbook "$ORIGEM"
git -C "$ORIGEM" rev-parse HEAD
git -C "$ORIGEM" log -1 --format=%cs

rm -rf "$DEST"
cp -r "$ORIGEM" "$DEST"
rm -rf "$DEST/.git" "$DEST/.github" "$DEST/.claude" "$DEST/.claude-plugin" \
       "$DEST/.gitignore" "$DEST/CLAUDE.md" "$DEST/CONTRIBUTING.md" \
       "$DEST/scripts" "$DEST/template" \
       "$DEST"/plugins/*/.claude-plugin "$DEST"/plugins/*/agents \
       "$DEST"/examples/mobile-*-fixture
rm -rf "$ORIGEM"
find "$DEST" -type l -delete
find "$DEST" -name '.*'
```

O upstream traz symlinks `references -> data` dentro de `plugins/code-security-skills/skills/*/`, e a carga nao os guarda: o `find -type l -delete` apaga so o link, nunca a pasta `data/` de destino. O `find` no fim precisa voltar vazio: componente de caminho iniciado por ponto dentro de `upstream/` teria de ser mapeado para `dot-`, e a lista de exclusao acima ja remove todos os que o upstream tem hoje. Depois:

1. Registre o commit e a data na tabela desta secao e a versao na tabela de skills de `docs/stack-ai/stack-de-ia.md`.
2. Confira a tabela de plays disponiveis do `SKILL.md` contra `ls upstream/plugins/*/plays/`. Play novo, removido ou renomeado exige ajuste na tabela de plays, na tabela de sinais e na de intencao.
3. Confira a coluna ASVS de `mapa-cwe-guia.md` contra o indice de `upstream/plugins/code-security-skills/skills/security-guidance/SKILL.md`.
4. Rode os testes e uma instalacao em destino descartavel, como em qualquer alteracao da carga.
5. Atualize o inventario deste arquivo.

## As demais skills de terceiros

Quatro skills de apoio sao copia de projeto de terceiro, e a versao instalada fica registrada aqui e na tabela de skills de `docs/stack-ai/stack-de-ia.md`:

| Skill | Versao instalada | Origem | Licenca |
|---|---|---|---|
| `caveman` | v1.9.0 | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | MIT |
| `grill-me` | v1.2.3 | [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity) | MIT |
| `grilling` | v1.2.3 | [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity) | MIT |
| `writing-for-agents` | v1.2.3 | [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity) | MIT |

Para atualizar uma delas, substitua a pasta da skill inteira pela versao nova da origem, registre a versao nesta tabela e na tabela de `docs/stack-ai/stack-de-ia.md`, e rode os testes e uma instalacao em destino descartavel, como em qualquer alteracao da carga.

## A documentacao em docs/stack-ai/

Cinco arquivos `.md` que explicam a stack para quem vai usar: o indice, o conceito, o SpecKit, a manutencao e os prompts genericos. E a unica parte da carga escrita para pessoa, e nao para agente.

O conteudo e generico e nao cita projeto nenhum. Ele descreve so o que esta nesta carga: os oito diretorios instalados e as 18 skills. Regra de projeto continua no `AGENTS.md`, e a regra que o agente segue ao editar uma fase continua em `.agents/references/speckit.md`, que a documentacao cita em vez de repetir.

A pasta e namespaced de proposito. O destino quase sempre ja tem `docs/`, e um subdiretorio proprio nunca colide com o que ja esta la.

Ela existe porque a carga nao escreve no `README.md` do destino. Sem um lugar proprio, a explicacao da stack nao teria como chegar em repositorio nenhum.

Nenhuma integracao recebe arquivo do SpecKit. O workflow de cada fase existe uma vez so, em `.agents/skills/speckit-<fase>/SKILL.md`, que e o nivel onde a descoberta de skill procura, entao a ferramenta chega nele apontando so para `.agents/skills`. Os scripts que as fases chamam vao em `.specify/scripts/`, nas duas variantes: `bash/` para Linux, macOS e WSL e `powershell/` para Windows. Sao seis de cada lado, equivalentes um a um, da mesma versao do SpecKit. A carga leva os dois conjuntos porque o time e misto.

## O que fica de fora

| Item | Motivo |
|---|---|
| `.claude/settings.local.json` | configuracao local do desenvolvedor, ja no `.gitignore` |
| `.opencode/node_modules/`, `package.json`, `package-lock.json` | dependencias instaladas pelo npm, nunca versionadas |
| As demais skills de `skills/` deste repositorio: `ciclo-design`, `conformidade-de-escrita-normativa`, `redacao-conformidade-de-escrita-normativa`, `recapitulacao-resumo-ata-relato-reuniao`, `reescrita-em-linguagem-simples-pt-br` e `stack-ai-build-project-context` | nao entram na carga por decisao. A `stack-ai-build-project-context` e skill em evolucao, e enriquecimento nao e escopo da `stack-ai-init` |
| `.agents/skills/stack-ai-init/` | ela mesma; distribuir o instalador levaria a carga junto, recursivamente |
| `specs/`, `.git/`, `__pycache__/` | trabalho do repositorio, nao artefato da stack |
| Partes do OWASP Secure Agent Playbook listadas na secao "A skill owasp-playbook" | formato de ferramenta ou insumo de teste |

`.agents/references/` entra na carga com o `speckit.md` e o `template-revisao-tecnica.md`. O `contrato-da-stack.md` da `stack-ai-build-project-context` declara a pasta peca obrigatoria da stack, entao ela sempre chega no destino com esses dois arquivos.

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

Sao os dois unicos arquivos da carga que nao chegam byte a byte: ambos trazem o placeholder `{{MARKETPLACE}}`, que a instalacao troca pelo nome do marketplace daquele destino. A lista esta em `SUBSTITUIVEIS`, em `scripts/instalar_stack.py`.

O `source` aponta para `./.agents` e nao para a raiz. Com a raiz, um `claude plugin install` copia o repositorio inteiro para o cache do desenvolvedor; com `.agents`, copia so a stack.

O primeiro start do Claude Code na pasta registra o marketplace e o segundo ja carrega as skills. As skills sao lidas ao vivo de `.agents/skills/`: skill nova ou editada vale na hora, sem comando de atualizacao.

O plugin e sempre `stack-ai` e o marketplace e um por repositorio. O registro de marketplaces do Claude Code, em `~/.claude/plugins/known_marketplaces.json`, e da maquina e guarda um caminho so por nome: dois repositorios que se batizassem igual disputariam a mesma entrada, e o perdedor carregaria as skills do outro sem nenhum aviso. Com o marketplace unico e o plugin fixo, a chave `stack-ai@<marketplace>` nao colide e a invocacao continua `/stack-ai:<skill>` em todo lugar.

O requisito e ser unico, e nao seguir um formato. Por isso o nome que o destino ja declara vale, e a derivacao `stack-ai-<diretorio de destino>` e so o padrao de quem ainda nao tem nome. `nome_do_marketplace` le o nome em `.claude-plugin/marketplace.json`, cai para a chave `stack-ai@<marketplace>` de `enabledPlugins` quando aquele arquivo falta, e so entao deriva do diretorio. O nome sai resolvido uma vez por execucao, antes da primeira escrita, para que os dois arquivos recebam o mesmo valor mesmo quando um deles nasce naquela rodada.

Marketplace de outro plugin, declarado pelo time, nao e adotado: a busca em `enabledPlugins` exige que o plugin da chave seja `stack-ai`.

A carga nao leva symlink porque symlink quebra fora do Linux. No Windows o Git so materializa symlink com `core.symlinks=true` mais Modo de Desenvolvedor, e sem isso o checkout deixa um arquivo de texto no lugar do diretorio, que o Claude Code descarta. Pasta sincronizada por OneDrive, Dropbox ou iCloud tem o mesmo efeito no macOS.

## Tres arquivos que o destino nunca recebe por cima

A carga nao leva `README.md` de raiz e nao leva `README.md` em `.agents/skills/`: documentacao de projeto e do destino, e catalogo de skill vira arquivo que ninguem atualiza. O instalador ainda protege o nome, entao um `README.md` de raiz que ja exista no destino nunca e tocado.

A protecao e por caminho e nao por nome de arquivo: `PROTEGIDOS` guarda `README.md`, e a comparacao usa o caminho inteiro. Entao `docs/stack-ai/README.md` nao e protegido, e cai na regra dos demais arquivos da stack. Isso e proposital: aquele arquivo e da carga, e precisa poder ser atualizado com `--sobrescrever`.

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

Edite `assets/stack/` direto, com o nome mapeado para `dot-` onde houver ponto. Nao existe repositorio molde de onde puxar. As duas skills com fonte em `skills/<nome>/` deste repositorio, `dicionario-dados-db-scan-codebase-docs` e `gauntlet-loop-forge`, sao copiadas a mao para a carga, sem script de sincronizacao.

O fluxo de qualquer mudanca:

1. Editar o arquivo em `assets/stack/`, ou criar o diretorio da skill nova.
2. Se a mudanca for em `dicionario-dados-db-scan-codebase-docs` ou em `gauntlet-loop-forge`, editar a fonte em `skills/<nome>/`, copiar a pasta inteira para `assets/stack/dot-agents/skills/<nome>/` e conferir com o `diff -rq` da secao "Onde a carga fica".
3. Se a mudanca envolver diretorio vazio ou symlink, declarar em `assets/estrutura.json`. As duas listas estao vazias hoje.
4. Rodar os testes: `cd scripts && python3 -m unittest test_instalar_stack`.
5. Instalar em um destino descartavel e conferir: `python3 scripts/instalar_stack.py instalar --destino <pasta vazia>`.
6. Atualizar o inventario deste arquivo quando a contagem mudar.

Para saber se um repositorio ja instalado ficou para tras, o comando e `python3 scripts/instalar_stack.py verificar --destino <raiz>`. Ele compara arquivo a arquivo por sha256 e devolve `igual`, `divergente` ou `ausente`.
