# Skills — Registro de Auditoria

Este documento é o registro de auditoria de todas as skills disponíveis no repositório: origem, versão, licença e composição.

---

## Índice

- [skill-creator](#skill-creator)
- [caveman](#caveman)
- [dicionario-dados-db-scan-codebase-docs](#dicionario-dados-db-scan-codebase-docs)
- [grill-me](#grill-me)
- [grilling](#grilling)
- [ponytail](#ponytail)
- [ponytail-audit](#ponytail-audit)
- [ponytail-debt](#ponytail-debt)
- [ponytail-gain](#ponytail-gain)
- [ponytail-help](#ponytail-help)
- [ponytail-review](#ponytail-review)
- [speckit](#speckit)
- [speckit-specify](#speckit-specify)
- [speckit-clarify](#speckit-clarify)
- [speckit-plan](#speckit-plan)
- [speckit-tasks](#speckit-tasks)
- [speckit-analyze](#speckit-analyze)
- [speckit-implement](#speckit-implement)
- [speckit-checklist](#speckit-checklist)
- [speckit-taskstoissues](#speckit-taskstoissues)
- [speckit-constitution](#speckit-constitution)

---

## Tabela de Auditoria

| Skill | Tipo | Versão | Licença | Repositório |
|---|---|---|---|---|
| skill-creator | externa | 3b3fad9 (2026-08-21) | Apache-2.0 | github.com/anthropics/skills |
| caveman | externa | v1.9.0 | MIT | github.com/JuliusBrussee/caveman |
| dicionario-dados-db-scan-codebase-docs | externa | 9f8e2c7 (2026-08-25) | não declarada | git.anatel.gov.br/processo_eletronico/ai-skills |
| grill-me | externa | v1.0.1 | MIT | github.com/mattpocock/skills |
| grilling | externa | v1.0.1 | MIT | github.com/mattpocock/skills |
| ponytail | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| ponytail-audit | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| ponytail-debt | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| ponytail-gain | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| ponytail-help | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| ponytail-review | externa | v4.8.4 | MIT | github.com/DietrichGebert/ponytail |
| speckit | externa | sei-sdd 2026-07-16 | MIT | github.com/github/spec-kit |
| speckit-specify | externa | sei-sdd 2026-07-16 | MIT | github.com/github/spec-kit |
| speckit-clarify | externa | sei-sdd 2026-07-16 | MIT | github.com/github/spec-kit |
| speckit-plan | externa | sei-sdd 2026-07-16 | MIT | github.com/github/spec-kit |
| speckit-tasks | externa | sei-sdd 2026-07-16 | MIT | github.com/github/spec-kit |
| speckit-analyze | externa | sei-sdd 2026-07-16 | MIT | github.com/github/spec-kit |
| speckit-implement | externa | sei-sdd 2026-07-16 | MIT | github.com/github/spec-kit |
| speckit-checklist | externa | sei-sdd 2026-07-16 | MIT | github.com/github/spec-kit |
| speckit-taskstoissues | externa | sei-sdd 2026-07-16 | MIT | github.com/github/spec-kit |
| speckit-constitution | externa | sei-sdd 2026-07-16 | MIT | github.com/github/spec-kit |

---

## skill-creator

> **Skill externa** — mantida pela Anthropic. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/anthropics/skills/tree/main/skills/skill-creator

**Versão instalada:** commit `3b3fad9` de 2026-08-21. A origem não publica versão semântica.

**Licença:** Apache-2.0, com `LICENSE.txt` acompanhando a skill.

Cria skills novas, edita e melhora skills existentes e mede o desempenho delas com evals. Toda skill criada ou evoluída neste repositório deve passar por ela, inclusive na otimização da descrição de disparo.

**Composição:**
- `SKILL.md` com o processo de criação, edição e avaliação de skill.
- `scripts/`: `quick_validate.py` (validação de frontmatter e estrutura), `package_skill.py`, `improve_description.py`, `run_eval.py`, `run_loop.py`, `aggregate_benchmark.py`, `generate_report.py` e `utils.py`.
- `agents/`: `analyzer.md`, `comparator.md` e `grader.md`, papéis usados na avaliação.
- `references/schemas.md`, `assets/eval_review.html` e `eval-viewer/` para revisão dos resultados de eval.

**Instalação:** 18 arquivos copiados de `skills/skill-creator` da origem, sem alteração de conteúdo.

**Descoberta pelo Claude Code:** symlink `.claude/skills/skill-creator` -> `../../.agents/skills/skill-creator`, porque aqui `.claude/skills/` é diretório real.

---

## caveman

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/JuliusBrussee/caveman — repositório autoritativo para rastreio de versão.
Também distribuída em https://github.com/mattpocock/skills/tree/main/skills/productivity.

**Versão instalada:** v1.9.0

**Licença:** MIT

**Alteração local:** Pequenos ajustes de idioma na descrição do frontmatter. Conteúdo das instruções preservado integralmente.

**Composição:**
- Seis níveis de intensidade: `lite`, `full` (padrão), `ultra`, `wenyan-lite`, `wenyan-full`, `wenyan-ultra`.
- Modo `full` elimina artigos, hedging e filler preservando todo conteúdo técnico.
- Modos `wenyan-*` comprimem no registro clássico chinês (文言文).
- Regra de auto-clareza: retorna à prosa normal em warnings destrutivos, sequências ambíguas ou confirmações de ação irreversível.
- Persiste na sessão até `stop caveman` ou `normal mode`.

**Como invocar:** `/caveman`, `/caveman lite`, `/caveman ultra`, `/caveman wenyan`

---

## dicionario-dados-db-scan-codebase-docs

> **Skill externa** — mantida no repositório de skills agnósticas da Anatel. Atualizações devem ser rastreadas lá.

**Repositório:** https://git.anatel.gov.br/processo_eletronico/ai-skills

**Versão instalada:** commit `9f8e2c7` (2026-08-25)

**Licença:** não declarada no repositório de origem

Investiga a codebase, os scripts de banco e a documentação disponível para gerar e manter dicionários de dados. O alvo pode ser o sistema inteiro, um módulo, uma base corporativa ou um data warehouse.

**Composição:**
- Núcleo genérico em `references/`: trata evidência, confiança, formato e fórmulas obrigatórias de descrição sem depender de linguagem, framework ou estrutura de projeto.
- Todo conhecimento específico de um alvo fica isolado em um adaptador, que diz onde está a fonte estrutural, qual fonte prevalece quando há mais de uma, como a versão é identificada e onde buscar no código.
- Os adaptadores ficam em `adapters/<família>/<caminho>.md` e são listados em `registro-adaptadores.md`, na raiz da skill. A cópia distribuída chega com o registro vazio e sem nenhum adaptador: o primeiro passo em um repositório novo é criar o do seu alvo, com o prompt "Criar o adaptador" do README da skill.
- Alvo sem adaptador não é bloqueio: a seção 3 do `references/contrato-de-adaptador.md` dispara um protocolo que pede as informações necessárias em vez de presumir convenção.
- Materiais fornecidos pelo desenvolvedor são evidência complementar opcional; nunca substituem a busca e a comparação obrigatórias com a codebase.
- Cria, atualiza ou verifica `dicionario_tabelas.md`, `dicionario_colunas.md` e `CHANGELOG.md`, conforme a intenção inferida e limitado ao alcance estrutural comprovado pelo adaptador.
- Princípios de ISO 8000-1, ISO/IEC 25012, ISO/IEC 25024, ISO/IEC 11179-3 e ISO/IEC 11179-4 convertidos em critérios de aceitação A1 a A10; não é declaração de conformidade.
- Verificador `scripts/verificar_dicionario.py` com os subcomandos `formato`, `tabelas-colunas`, `changelog` e `diff`, coberto por 61 testes `unittest`.

**Como invocar:** cite o nome da skill no pedido, como nos exemplos do [`README.md`](dicionario-dados-db-scan-codebase-docs/README.md) dela.

---

## grill-me

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/mattpocock/skills/tree/main/skills/productivity

**Versão instalada:** v1.0.1

**Licença:** MIT

**Composição:** Alias fino que delega para `grilling`.

**Como invocar:** `/grill-me`

---

## grilling

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/mattpocock/skills/tree/main/skills/productivity

**Versão instalada:** v1.0.1

**Licença:** MIT

**Composição:**
- Entrevista socrática sobre cada aspecto do plano ou design.
- Percorre cada galho da árvore de decisão resolvendo dependências uma a uma.
- Cada pergunta acompanha uma resposta recomendada.
- Perguntas são feitas uma por vez.
- Se uma pergunta puder ser respondida explorando o código, o agente explora o código em vez de perguntar.

**Como invocar:** `/grilling` ou `/grill-me`

---

## ponytail

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Modo principal de codificação — ativo em toda resposta após invocação.
- Força solução mínima via ladder: YAGNI → reutilizar codebase → stdlib → feature nativa → dependência instalada → one-liner → apenas então escrever código novo.
- Três intensidades: `lite` (nomeia a alternativa mais simples), `full` (ladder completa, padrão), `ultra` (YAGNI extremista, desafia o requisito antes de construir).
- Marca simplificações deliberadas com comentário `ponytail: <teto>, <gatilho de upgrade>`.
- Nunca simplifica: validação de entrada, tratamento de erro que previne perda de dados, segurança, acessibilidade ou funcionalidade explicitamente solicitada.
- Desativar: `stop ponytail` / `normal mode`.

**Como invocar:** `/ponytail`, `/ponytail lite`, `/ponytail ultra`

---

## ponytail-audit

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Igual ao `ponytail-review`, mas varre o repositório inteiro em vez de um diff.
- Ranking por impacto: maior corte primeiro.
- One-shot — lista achados, não aplica.
- Tags: `delete:`, `stdlib:`, `native:`, `yagni:`, `shrink:`.

**Como invocar:** `/ponytail-audit`

---

## ponytail-debt

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Coleta todos os comentários `ponytail:` do repo em um ledger de dívida técnica.
- Comando: `grep -rnE '(#|//) ?ponytail:' .`
- Sinaliza entradas sem gatilho de upgrade com tag `no-trigger` (risco de rot silencioso).
- Fecha com `<N> markers, <M> with no trigger.` ou `No ponytail: debt. Clean ledger.`
- Pode persistir o ledger em `PONYTAIL-DEBT.md` se solicitado.

**Como invocar:** `/ponytail-debt`

---

## ponytail-gain

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Exibe scoreboard ASCII com medianas dos benchmarks publicados (5 tarefas × 3 modelos).
- Não calcula número por repositório — nunca inventa baseline de código que não foi escrito.
- One-shot; não altera modo nem persiste estado.

**Como invocar:** `/ponytail-gain`

---

## ponytail-help

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Cartão de referência rápida: todos os modos, skills e comandos ponytail.
- One-shot; não altera modo.

**Como invocar:** `/ponytail-help`

---

## ponytail-review

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/DietrichGebert/ponytail/tree/main/skills

**Versão instalada:** v4.8.4

**Licença:** MIT

**Composição:**
- Review focado **exclusivamente** em over-engineering — não avalia correção, segurança ou performance.
- Tags: `delete:`, `stdlib:`, `native:`, `yagni:`, `shrink:`.
- Um achado por linha: `L<n>: <tag> <o que cortar>. <substituto>.`
- Fecha com `net: -<N> lines possible.` ou `Lean already. Ship.`
- Por não avaliar correção nem segurança, complementa um code review comum sem sobrepor escopo.

**Como invocar:** `/ponytail-review`

---

## speckit

> **Skill externa** — mantida por terceiros. Atualizações devem ser rastreadas no repositório de origem.

**Repositório:** https://github.com/github/spec-kit

**Versão instalada:** os `SKILL.md` das 9 fases foram trazidos do repositório `sei-sdd` (cópia de 2026-08-27), que não registra a versão upstream de origem. O runtime em `.specify/` (scripts, templates, manifestos) continua em v0.16.6.dev0.

**Licença:** MIT

Framework de especificação que estrutura o fluxo SDD deste repositório. As 9 sub-skills abaixo vivem em **uma fonte única**, `.agents/skills/speckit-<fase>/SKILL.md`, neutra em relação à ferramenta.

**Nenhuma integração guarda arquivo do SpecKit.** Descoberta de skill enxerga um nível abaixo do diretório configurado (`<local>/<nome>/SKILL.md`). As fases ficam nesse nível, lado a lado com as demais skills do repositório, então as três ferramentas as encontram sem configuração extra:

| Ferramenta | Como chega em `.agents/skills/` |
|---|---|
| Claude Code | `.claude/skills`, symlink para `../.agents/skills` |
| Copilot | `chat.agentSkillsLocations` em `.vscode/settings.json` |
| OpenCode | `skills.paths` em `.opencode/opencode.json` |

Os scripts de cada fase ficam em `.specify/scripts/bash/` (Linux, macOS, WSL) e `.specify/scripts/powershell/` (Windows), equivalentes um a um. O frontmatter declara os dois caminhos em `scripts` (e em `agent_scripts`, no `speckit-plan`), e a seção `Script Selection` do corpo diz ao agente qual entrada usar conforme o shell.

Invocação: `/speckit-plan`, com hífen. O nome sai do diretório da skill, então é o mesmo nas três.

Regra de manutenção: [`.agents/references/speckit.md`](../references/speckit.md).

| Sub-skill | Fase | O que faz |
|---|---|---|
| `speckit-specify` | Especificação | Transforma a descrição em linguagem natural em uma especificação estruturada. |
| `speckit-clarify` | Clarificação | Levanta dúvidas e ambiguidades antes de planejar. |
| `speckit-plan` | Planejamento | Produz o plano técnico de implementação. |
| `speckit-tasks` | Tarefas | Decompõe o plano em tarefas granulares e sequenciadas. |
| `speckit-analyze` | Análise | Analisa riscos, dependências e impactos. |
| `speckit-implement` | Implementação | Implementa seguindo o plano e as tarefas definidos nas fases anteriores. |
| `speckit-checklist` | Checklist | Gera o checklist de implementação da funcionalidade. |
| `speckit-taskstoissues` | Issues | Converte as tarefas em issues no GitHub. |
| `speckit-constitution` | Constituição | Manutenção do arquivo `constitution.md`. |

---

## speckit-specify

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** sei-sdd 2026-07-16 | **Licença:** MIT

Cria ou atualiza a especificação da funcionalidade a partir de uma descrição em linguagem natural.

**Como invocar:** `/speckit-specify` nas três ferramentas

---

## speckit-clarify

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** sei-sdd 2026-07-16 | **Licença:** MIT

Identifica áreas subespecificadas na especificação atual, faz até 5 perguntas de clarificação direcionadas e grava as respostas de volta na especificação.

**Como invocar:** `/speckit-clarify` nas três ferramentas

---

## speckit-plan

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** sei-sdd 2026-07-16 | **Licença:** MIT

Executa o fluxo de planejamento usando o template de plano para gerar os artefatos de design.

**Como invocar:** `/speckit-plan` nas três ferramentas

---

## speckit-tasks

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** sei-sdd 2026-07-16 | **Licença:** MIT

Gera um `tasks.md` acionável e ordenado por dependência para a funcionalidade, a partir dos artefatos de design disponíveis.

**Como invocar:** `/speckit-tasks` nas três ferramentas

---

## speckit-analyze

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** sei-sdd 2026-07-16 | **Licença:** MIT

Realiza uma análise não destrutiva de consistência e qualidade entre `spec.md`, `plan.md` e `tasks.md` após a geração das tarefas.

**Como invocar:** `/speckit-analyze` nas três ferramentas

---

## speckit-implement

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** sei-sdd 2026-07-16 | **Licença:** MIT

Executa o plano de implementação, processando e executando todas as tarefas definidas em `tasks.md`.

**Como invocar:** `/speckit-implement` nas três ferramentas

---

## speckit-checklist

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** sei-sdd 2026-07-16 | **Licença:** MIT

Gera um checklist customizado para a funcionalidade atual, a partir dos requisitos informados.

**Como invocar:** `/speckit-checklist` nas três ferramentas

---

## speckit-taskstoissues

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** sei-sdd 2026-07-16 | **Licença:** MIT

Converte as tarefas existentes em issues do GitHub acionáveis e ordenadas por dependência, a partir dos artefatos de design disponíveis.

**Como invocar:** `/speckit-taskstoissues` nas três ferramentas

---

## speckit-constitution

> **Skill externa** — parte do framework [speckit](#speckit).

**Repositório:** https://github.com/github/spec-kit | **Versão:** sei-sdd 2026-07-16 | **Licença:** MIT

Cria ou atualiza a constituição do projeto a partir de princípios informados de forma interativa ou direta.

**Como invocar:** `/speckit-constitution` nas três ferramentas
