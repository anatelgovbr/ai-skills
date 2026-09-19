# Instrucoes para agentes

## Escopo

Este e um repositório pessoal para demandas agênticas de qualquer tipo. Não presuma uma linguagem, framework, produto ou fluxo de negócio: descubra o contexto no pedido e nos arquivos relevantes antes de agir.

## Disciplina de Execução Agêntica

Trabalhar sempre nesta ordem: pensar antes de agir, planejar cirurgicamente, definir o objetivo verificável, executar e verificar. O rigor cresce com a complexidade e o risco; guardrails, gates e regras do projeto valem sempre.

### 1. Pensar antes de agir

**Não presumir. Não esconder dúvida. Expor tradeoffs.**

Antes de qualquer alteração:
- Declarar as premissas adotadas. Em dúvida, perguntar.
- Se existem várias interpretações, apresentar todas e nomear o ponto que falta; escolher em silêncio não é opção.
- Se existe caminho mais simples dentro dos padrões documentados, apresentar o caminho e a diferença e aguardar a escolha do desenvolvedor.
- Se algo não está claro, parar, nomear o que confunde e perguntar.
- Em conflito entre documentos, seguir "Regras de Decisão".

### 2. Planejar cirurgicamente

**A menor mudança correta. Nada além do pedido.**

Delimitar o que vai mudar:
- Sem funcionalidade além do pedido.
- Sem abstração para código de uso único.
- Sem "flexibilidade" ou "configurabilidade" que ninguém pediu.
- Sem tratamento de erro para cenário impossível.
- Código adjacente, comentários, formatação e o que não está quebrado ficam fora.
- Código morto preexistente e problema fora do escopo ficam no código e entram na resposta como observação curta.

Teste de saída: um revisor sênior da stack do projeto aprova o escopo sem ressalva de complexidade.

### 3. Definir o objetivo verificável

**Definir o que é "pronto" antes de executar.**

Traduzir o pedido em critério verificável:
- "Adicionar validação" → "listar as entradas inválidas, implementar, provar cada uma com comando".
- "Corrigir o bug" → "reproduzir com comando, corrigir, repetir o comando até passar".
- "Refatorar ou otimizar X" → "registrar o comportamento antes, alterar, comprovar o mesmo comportamento depois".

Em tarefa não trivial ou multietapa, declarar um plano curto:
    1. [Passo] → verificar: [checagem]
    2. [Passo] → verificar: [checagem]
    3. [Passo] → verificar: [checagem]

### 4. Executar

**Tocar apenas no que foi delimitado. Limpar só a própria sujeira.**

- Seguir o estilo existente, mesmo que o agente fizesse diferente.
- Remover imports, variáveis e funções que a própria mudança deixou sem uso.
- Se saíram 200 linhas e cabia em 50, reescrever.

Teste de saída: cada linha alterada no diff responde a um trecho do pedido ou a uma regra documentada no projeto; linha sem uma dessas origens sai do diff.

### 5. Verificar

**Verificação é comando executado pelo agente, com resultado registrado na resposta.**

- Executar os gates obrigatórios e os critérios de sucesso.
- Repetir correção e verificação até todos passarem.
- Verificação que depende do desenvolvedor, como smoke manual, entra na resposta como pendente.
- Informar impedimentos e pendências sem declarar a entrega concluída.

Teste de saída: cada critério de sucesso aparece na resposta com o comando e o resultado; "parece funcionar" não conta.

## Regras de Escrita

Salvo solicitação explícita em contrário, aplique estas regras às mensagens em linguagem natural destinada a pessoas durante a sessão e aos entregáveis textuais em português brasileiro. Em código, comandos, identificadores, nomes de APIs, caminhos, dados estruturados e outros elementos definidos por linguagem, formato, protocolo ou projeto, preserve a sintaxe, o idioma e as convenções próprios do artefato. Instruções específicas do entregável prevalecem sobre estas regras gerais de estilo.

Em prosa Markdown, mantenha cada parágrafo em uma única linha no conteúdo-fonte e quebre linhas apenas entre parágrafos ou quando a estrutura do formato exigir. Use português brasileiro correto, linguagem clara, objetiva, respeitosa e profissional, voz ativa e frases completas. Não use travessão. Prefira palavras comuns, verbos diretos e afirmações precisas. Evite preâmbulos, redundâncias, coloquialismos, metáforas, clichês, hipérboles, construções rebuscadas, excesso de negativas e perguntas retóricas.

Use termos técnicos quando forem necessários à precisão ou forem a denominação canônica no contexto de desenvolvimento. Explique na primeira ocorrência os termos que possam não ser conhecidos pelo público do texto. Use siglas somente quando úteis e apresente o nome por extenso na primeira ocorrência, salvo siglas amplamente conhecidas. Não traduza nem adapte código, identificadores, comandos, nomes próprios de tecnologias ou outros termos que precisem permanecer literais.

Apresente primeiro a informação mais importante e evite introduções ou resumos que apenas repitam o conteúdo. Use subtítulos, listas e tabelas quando melhorarem a leitura, especialmente em textos longos ou sequências extensas, sem fragmentar artificialmente o texto. Siga a norma-padrão do português brasileiro e não crie flexões incompatíveis com ela.

Preserve literalmente citações diretas e outros conteúdos que precisem permanecer exatos, salvo solicitação expressa de revisão. Apresente URLs como links associados a expressões descritivas quando o formato permitir.

## Acionamento da stack

- A raiz deste repositório e o contexto geral; o guia de uso e o catálogo ficam no [README.md](README.md).
- Cada skill publicada fica em `skills/<nome>/SKILL.md`. O nome do diretório é o nome exato usado para acioná-la.
- Antes de responder, planejar ou editar, classifique o pedido e verifique no catálogo do README se existe uma skill aplicável. Quando existir, acione-a pelo nome exato, leia seu `SKILL.md` e siga o fluxo definido por ela.
- Para acionamento explicito, use `Use a skill <nome> para <objetivo>` ou o comando `/nome` quando a skill oferecer um comando. Não carregue todas as skills sem necessidade.
- `caveman` é um modo de acionamento explicito; use o comando indicado no README e não espere que seja escolhido automaticamente.
- Use `stack-ai-init` somente para instalar, atualizar ou verificar a stack em outro repositório. Esta raiz é a fonte da skill e não é um destino válido para ela.
- Se nenhuma skill se aplicar, siga as regras deste arquivo e mantenha a mudança proporcional ao pedido.

## Roteamento rápido

- Criar, editar, validar ou avaliar uma skill: `skill-creator`.
- Escrever documentação consumida por agentes ou modificar `AGENTS.md` ou `CLAUDE.md`: `writing-for-agents`.
- Gerar dicionário de dados ou changelog estrutural a partir de codebase e banco: `dicionario-dados-db-scan-codebase-docs`.
- Projetar ou reformular uma interface frontend com direção visual intencional: `frontend-design`.
- Executar um ciclo crítico de design com referência real e críticos independentes: `ciclo-design`.
- Criar, editar ou analisar documento Word (`.docx` ou `.dotx`): `docx`; arquivo PDF: `pdf`; apresentação, deck ou arquivo `.pptx`/`.potx`: `pptx`; planilha (`.xlsx`, `.xlsm`, `.xltx`, `.csv` ou `.tsv`): `xlsx`.
- Escrever ou reescrever texto em Linguagem Simples em português brasileiro: `escrita-em-linguagem-simples-pt-br`.
- Produzir recapitulação, resumo, ata ou lista de ações de reunião: `recapitulacao-resumo-ata-relato-reuniao`.
- Analisar a conformidade de redação de minuta de ato normativo brasileiro: `conformidade-de-escrita-normativa`.
- Criar ou otimizar prompt de execução do Gauntlet Loop: `gauntlet-loop-forge`.
- Instalar, atualizar ou verificar a stack em outro repositório: `stack-ai-init`.
- Investigar a codebase e gerar ou atualizar a base operacional para agentes de um repositório com a stack instalada: `stack-ai-build-project-context`.
- Responder de forma comprimida: `caveman`.

## Hierarquia e guardrails

1. Instruções explicitas do usuário ou desenvolvedor.
2. Este arquivo.
3. O `SKILL.md` da skill acionada.
4. O [README.md](README.md) e demais documentações de apoio.

Em caso de conflito ou ambiguidade relevante, pare e solicite uma decisão:

- Leia cada arquivo antes de editá-lo e preserve alterações existentes.
- Não invente tecnologias, comandos ou convenções que não estejam documentados.
- Nunca inclua credenciais, tokens ou arquivos `.env` em alterações.
- Confirme antes de executar uma ação destrutiva ou difícil de reverter.
- Valide a mudança com a verificação mais próxima disponível; quando não houver testes, confira estrutura, referencias e os arquivos diretamente afetados.