# stack-ai-build-project-context

A skill `stack-ai-build-project-context` recebe um repositório com a estrutura mínima da stack de IA instalada (um `AGENTS.md`, uma pasta `.agents/references/` e uma pasta `.agents/skills/`, mesmo vazias), investiga a codebase e transforma o que descobre em **base operacional de conhecimento**: como aquele sistema é construído e como normalmente se desenvolve nele.

O objetivo não é avaliar se a arquitetura segue boas práticas nem propor a arquitetura ideal. É descobrir o padrão real e deixá-lo escrito de forma que outro agente implemente de forma coerente com o que já existe. Padrão legado recorrente, inclusive o que parece antipadrão técnico, é convenção do sistema e é registrado como tal, com a contagem que o sustenta e sem juízo de qualidade.

Ela é agnóstica à codebase por construção: não presume arquitetura, não importa convenção de outro projeto e não carrega para o repositório de destino nenhuma regra deste repositório. Tudo o que entra na stack precisa estar sustentado por evidência do código do destino, com caminho, contagem, busca pelo que contradiz e alcance declarado.

O critério de valor de cada achado é uma pergunta só: **um agente que precisa implementar algo neste sistema decide diferente por saber disto?** O que ele descobre sozinho abrindo o arquivo que vai editar não paga o custo de ocupar contexto.

## O que a rodada precisa deixar respondido

- Como uma página, tela, endpoint ou unidade equivalente é construída aqui?
- Como se cria uma unidade autenticada, e como a permissão é verificada?
- Onde ficam as regras de negócio, e como são acionadas?
- Como o sistema acessa dados? Procedure, query direta, ORM ou abstração própria? É obrigatório ou apenas comum?
- Como transações, erros e sessão são tratados?
- Como as integrações externas são usadas deste lado?
- Quais arquivos costumam participar de uma funcionalidade?
- Quais padrões devem ser preservados ao criar código novo, e qual desvio merece alerta?

Pergunta sem resposta escrita é lacuna declarada no relatório, com um dos três motivos: não existe no sistema, não foi investigada por decisão, ou a evidência não fechou. Silêncio não é nenhum dos três.

## Como ela decide onde o conhecimento vai

O destino sai da natureza do conhecimento, não de uma cascata de reprovações. Em qualquer um deles o texto declara o sistema, não a rodada: a tecnologia, onde a unidade vive e o que o código faz, no presente do indicativo. Método, contagem e comando ficam na seção de evidências, que é onde a próxima auditoria vai procurá-los.

- **`AGENTS.md`** recebe as seções de inventário (contexto e dependências técnicas, em tópicos, alimentadas pelo censo), regra transversal curta, guardrail de alcance amplo e roteamento. Contexto global é carregado em toda tarefa, então a barra de *regra* é alta de propósito; a de *inventário* não é, porque inventário não é regra.
- **Skills** recebem fluxo de implementação ou de verificação recorrente: criar uma unidade, acessar dados, tornar uma unidade autenticada, verificar permissão, integrar com um subsistema. Toda skill responde três coisas: quando usar o padrão, como reconhecê-lo no código e como aplicá-lo numa implementação nova. Criação e evolução passam obrigatoriamente pela `skill-creator`.
- **`.agents/references/`** recebe o detalhe consultivo (arquitetura, estrutura das unidades, persistência, autenticação, integrações, convenções de módulo) com gatilho de consulta declarado e **exemplares representativos** com caminho completo e a regra que localiza o equivalente atual. O padrão é escrito de forma que a implementação não dependa de abrir nenhum exemplar: arquivo é apagado e renomeado, e a instrução precisa sobreviver a isso.
- **Guardrails** são alertas de coerência, alocados conforme o alcance: `AGENTS.md` quando transversal, dentro da skill quando são do fluxo, na reference do módulo quando são locais. Eles alertam sobre divergência em relação ao padrão identificado, nomeando o território onde ele vale e o comando que confirma o caso em mãos, e nunca proíbem nem afirmam que o padrão é tecnicamente ideal.
- **Automação da ferramenta** (hook, subagente, comando) é recomendação ao desenvolvedor, com tipo, gatilho e evidência. A skill não instala nem configura nada.
- **O eixo de invocação** é decidido para toda skill produzida: ponto de entrada de fluxo fica model-invocada e paga a descrição em toda tarefa; skill de etapa recebe `disable-model-invocation: true`, custa zero permanente e é alcançada por `/nome` ou por um artefato que mande ler o `SKILL.md` dela pelo caminho. Ativar uma skill user-invocada pelo nome não funciona, e o verificador aponta onde isso foi escrito.
- **O que foi descartado** fica escrito na seção `## Descartado` da reference de evidências, com motivo, alcance medido e o que faria a decisão mudar. Descarte só no relatório morre com a sessão, e a rodada seguinte reinvestiga o mesmo achado para chegar na mesma reprovação.

## Como ela trabalha

O censo levanta a superfície da codebase, o perfil de codificação e os **sinais de dependência** declarados no próprio código: componentes instanciados, includes mais frequentes, driver de dados, bibliotecas com versão no nome, formatos de ferramenta. Manifesto não é a única forma de declarar dependência e, em sistema legado, quase nunca é a usada.

Depois, a rodada identifica **as unidades que o sistema produz repetidamente** por uma tabela de sinal para unidade, parando no primeiro sinal dominante e registrando qual foi, com os caminhos que o comprovam, e escolhe exemplares representativos (recentes, antigos, de módulos diferentes), que são lidos por inteiro antes de qualquer busca. O histórico do versionamento entra como fonte própria: arquivo que concentra correção é onde o sistema erra, e frequência da operação é a evidência de recorrência que sustenta uma skill. As frentes de investigação saem do cruzamento entre esses recortes e os **eixos obrigatórios**: estrutura, ciclo da requisição, autenticação, autorização, construção da unidade, validação, persistência, regra de negócio, integrações, erro e log, configuração, e padrões equivalentes.

Cada frente vira um subagente com escopo limitado, eixos atribuídos e proibição de escrever. O dossiê que ele devolve traz três coisas, e as três importam: padrões com finalidade, **processos observados** (a sequência reconstruída, que é de onde nasce skill) e **candidatos a guardrail**.

Antes de qualquer coisa ser gravada, os artefatos passam por verificação proporcional ao custo do erro: ciclo completo do Gauntlet Loop para regra de `AGENTS.md` e guardrail, avaliação da proposta contra os exemplares para skill, conferência dirigida para reference descritiva. Nada é escrito antes de um plano aprovado pelo desenvolvedor, e o plano inclui a tabela de cobertura por eixo e os critérios de conclusão da rodada. Quando o desenvolvedor autoriza explicitamente a rodada a aplicar sem aprovação prévia, o gate não some: ele passa para depois da escrita, o plano continua sendo registrado, a auditoria final sobre o diff vira obrigatória, e remover ou reduzir o que já estava escrito continua exigindo aprovação.

Quatro papéis rodam em contexto separado e têm prompt próprio em `agents/`: o revisor do que investigar, o investigador, o auditor do rascunho e o medidor de conformidade.

Toda rodada tem um **registro** criado na Fase 0, fora do repositório de destino, preenchido fase a fase. Na Fase 7 ele já é o plano.

A skill é idempotente: pode rodar de novo conforme o sistema evolui, atualizando o que já existe em vez de duplicar. Achado que contradiz artefato antigo é o item mais importante da rodada.

## Comando reproduzível

Todo comando publicado numa seção de evidências é **executado como está escrito** antes de entrar no artefato, e precisa devolver o número registrado ao lado dele. Sem isso, a medição de conformidade da próxima rodada lê contradição onde há erro de comando e derruba artefato correto.

Um detalhe que já custou uma rodada real: no `grep` vale a última opção passada, e `-I` anula `-a`. `grep -aRIl` pula arquivo tratado como binário e devolve contagem menor sem avisar. A forma que não depende de ordem é `--binary-files=text`.

## Verificador

`scripts/inventario_stack.py` responde de forma determinística onde as coisas estão e o que está mecanicamente quebrado:

```bash
python3 scripts/inventario_stack.py stack     --raiz <repo>   # peças da stack e orçamento de contexto
python3 scripts/inventario_stack.py censo     --raiz <repo>   # superfície, codificação e sinais de dependência
python3 scripts/inventario_stack.py verificar --raiz <repo>   # checagens mecânicas dos artefatos
python3 scripts/inventario_stack.py validar-achado --arquivo <dossiê>   # campos, contagens, processos e guardrails
```

O `validar-achado` lê o dossiê devolvido por um investigador e **calcula** a classificação do padrão a partir dos números, em vez de aceitar a declarada: `convencao`, `dominante-com-excecoes`, `concorrentes` ou `isolado`. Ele recusa campo devolvido como molde, contagem que não fecha, contraexemplo sem quantidade, comando de contraexemplo idêntico ao de confirmação, guardrail sem contagem visível e processo sem sequência. Dossiê sem a seção de processos observados sai com aviso: é ela que alimenta a fase de skill, e sem ela a rodada termina sem nenhuma.

O `stack` reporta o **orçamento de contexto permanente**: quanto o `AGENTS.md` custa em toda tarefa, quanto as descrições de skill custam em toda tarefa, e quanto os corpos das references custam apenas quando abertos. O orçamento existe contra inflação de regra global, nunca contra a skill de fluxo ou a reference de arquitetura que ensinam a construir.

Coberto por 88 testes `unittest` em `scripts/test_inventario_stack.py`. O verificador não avalia conteúdo: julgamento de conteúdo é do Gauntlet Loop.

A própria skill tem mais 8 testes de estrutura em `scripts/test_estrutura_skill.py`: conferem o frontmatter, se todo caminho citado entre crases resolve para um arquivo que existe e se toda reference, agente e template é acionado em algum lugar. Rode os dois juntos depois de editar a skill:

```bash
cd scripts && python3 -m unittest test_inventario_stack test_estrutura_skill
```

## Preflight

Antes de prometer qualquer coisa, a skill confere o que o runtime oferece: raiz do repositório, `python3`, `rg` ou `grep`, `file` e `iconv`, subagentes e `skill-creator`. Ausência descoberta no fim custa a rodada inteira.

Skill é destino esperado desta rodada, então a ausência da `skill-creator` é dita ao desenvolvedor **antes de começar**, junto com o que a instala. Sem subagentes, a investigação vira passagens inline separadas e o relatório declara que a independência foi limitada.

No mesmo momento ficam definidos o escopo de escrita, os **não objetivos** (por padrão: branches, promoção entre ambientes, deploy, agendamento e ambiente de execução, que não estão no código e não mudam o que o agente escreve) e a lista de sistemas externos consumidos, cujo uso local é investigado deste lado da fronteira.

## Prompts de Exemplo

Todo trecho entre `<` e `>` é um parâmetro: substitua antes de enviar, e apague a linha inteira quando não tiver como preencher.

### Enriquecer uma stack recém instalada

```text
Use a skill `stack-ai-build-project-context` no repositório em <caminho da raiz>. A stack mínima já está instalada e está vazia.

Descubra como este sistema é construído e como se desenvolve nele, e me traga o plano antes de escrever qualquer coisa.

O que eu já sei sobre ele:
- o que o sistema faz: <se souber>
- partes que costumam dar problema para quem chega: <se souber>
- pontos que eu considero fora do escopo desta rodada: <se houver>

Trate os itens acima como pista, não como conclusão: confirme cada um contra o código e me avise se algum divergir.
```

### Mapear como se constrói uma unidade

Use quando o que você quer é a receita de implementação, não o retrato do sistema inteiro.

```text
Use a skill `stack-ai-build-project-context` no repositório em <caminho da raiz>, focada em como se cria <página, endpoint, relatório, procedure> neste sistema.

Leia exemplares recentes e antigos por inteiro, reconstrua a sequência com o que é obrigatório e o que varia, e me proponha a skill de fluxo correspondente junto com os guardrails que ela deve carregar.
```

### Enriquecer só um subsistema

```text
Use a skill `stack-ai-build-project-context` no repositório em <caminho da raiz>, com escopo limitado a <subsistema, módulo ou conjunto de diretórios>.

Não investigue o resto do repositório nesta rodada. Se encontrar algo relevante fora do escopo, registre como pergunta no relatório em vez de investigar.
```

### Atualizar a stack depois de uma mudança grande

```text
Use a skill `stack-ai-build-project-context` no repositório em <caminho da raiz>. A stack já tem conteúdo.

Leia o que já está registrado antes de investigar e me traga só o delta: o que mudou, o que passou a existir e, principalmente, o que hoje contradiz algum artefato já escrito. Rode os comandos registrados nas evidências como estão escritos e me diga quais não reproduzem o próprio número.

Contexto da mudança: <o que mudou no sistema, se souber>
```

### Avaliar se algo merece virar skill

```text
Use a skill `stack-ai-build-project-context` no repositório em <caminho da raiz> para avaliar se <tarefa recorrente> justifica uma skill própria.

Procure no código e no histórico a evidência de recorrência e a sequência que os exemplares mostram. Se a evidência não sustentar uma skill, me diga isso e proponha o destino correto em vez de criar a skill mesmo assim.
```
