# Protocolo de handoff

Handoff e a passagem de trabalho de uma skill para outra atraves de uma fronteira de contexto real: um subagente. A skill de origem produz um resumo estruturado e o subagente recebe so esse resumo e o `SKILL.md` da skill de destino. O contexto intermediario da origem nao cruza a fronteira.

## Por que usar

Duas skills carregadas no mesmo contexto disputam atencao, e o trabalho intermediario da primeira polui o da segunda. O handoff resolve:

1. A skill de origem trabalha sem ver os passos da proxima (evita premature completion).
2. A skill de destino trabalha sem o ruido da anterior (contexto limpo).
3. O agente principal recebe so o resultado, nao o processo.

## Quando usar

Use handoff quando a skill de destino precisa de contexto limpo para funcionar bem. Nao use quando a continuacao e trivial e o contexto acumulado e pequeno.

Indicadores de que handoff vale:

- A skill de origem produz muita saida intermediaria (diffs, logs, relatorios).
- A skill de destino tem seu proprio fluxo de passos que sera prejudicado pelo contexto anterior.
- As duas skills pertencem a dominios diferentes (teste e revisao, implementacao e documentacao).

## Payload de handoff

O payload e um bloco Markdown estruturado que cruza a fronteira. Ele contem so o que a skill de destino precisa e nada do processo interno da origem.

```markdown
## Handoff: <skill-origem> → <skill-destino>

### Contexto
<uma frase sobre o que foi feito>

### Arquivos alterados
- `caminho/arquivo.py`: <o que mudou>

### Decisoes tomadas
- <decisao relevante para a proxima skill>

### Pendencias para a skill de destino
- <o que a skill de destino precisa fazer>

### Dados
<metricas, saidas de gate, ou outro dado estruturado que a skill de destino consome>
```

Regras do payload:

- Maximo 50 linhas. Se nao cabe, o resumo esta ruim.
- Sem codigo fonte: cite arquivo e linha, nao copie o trecho.
- Sem instrucoes de como rodar a skill de destino: ela tem o proprio `SKILL.md`.
- Inclua somente o que a skill de destino precisa para comecar. Dados que ela pode ler dos arquivos nao entram.

## Declaracao de interface

Cada skill que participa de handoff declara uma secao `## Handoff` no seu `SKILL.md`:

```markdown
## Handoff

### Recebe de
- `skill-origem`: o que espera no payload (ex: lista de arquivos alterados, metricas de cobertura)

### Entrega para
- `skill-destino`: o que produz no payload (ex: lista de achados com severidade, arquivos revisados)
```

A secao e opcional. Skill sem `## Handoff` pode participar de handoff, mas nao documenta sua interface.

## Despacho

O agente principal despacha o handoff como subagente com o prompt:

```
Use a skill <destino> para <objetivo>.

<payload de handoff colado aqui>
```

O subagente recebe contexto limpo: so o prompt acima e os arquivos do repositorio. Ele carrega o `SKILL.md` da skill de destino e trabalha a partir do payload.

O agente principal nao espera o subagente para continuar trabalho independente. Quando o resultado volta, ele integra no fluxo.

## Cadeias comuns

| Origem | Destino | Quando |
|---|---|---|
| qualquer skill que altere codigo | `testes-unitarios-cobertura` | apos implementacao, para garantir cobertura |
| `testes-unitarios-cobertura` | `code-reviewer` ou equivalente | apos testes verdes, para revisao de qualidade |
| `skill-creator` | `testes-unitarios-cobertura` | skill nova com scripts precisa de testes |
| `stack-ai-build-project-context` | `writing-for-agents` | contexto gerado precisa de revisao de escrita |

## O que nao e handoff

- Invocar uma skill em sequencia no mesmo contexto nao e handoff: e continuacao. O contexto da primeira permanece.
- Delegar para um subagente sem payload estruturado nao e handoff: e despacho generico. O subagente nao sabe o que a skill anterior fez.
- Copiar a saida inteira da skill anterior no prompt do subagente nao e handoff: e poluicao de contexto com etapa extra.
