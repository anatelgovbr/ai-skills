# Instrucoes para agentes

## Escopo

Este e um repositório pessoal para demandas agênticas de qualquer tipo. Não presuma uma linguagem, framework, produto ou fluxo de negócio: descubra o contexto no pedido e nos arquivos relevantes antes de agir.

## Disciplina de Execução Agêntica

Aplicar com rigor proporcional à complexidade e ao risco, sem flexibilizar guardrails, gates ou regras específicas deste repositório:

* **Pensar antes de alterar**: explicitar premissas, inconsistências e tradeoffs relevantes. Em ambiguidade de contrato, requisito ou conflito documental, deve explicitar para decisão do usuário; não inventar.
* **Simplicidade primeiro**: implementar a menor solução correta. Não adicionar funcionalidades, abstrações, configurabilidade, generalizações futuras ou tratamento de cenários não exigidos.
* **Mudanças cirúrgicas**: alterar somente o necessário, preservar estilo e comportamento adjacentes e remover apenas órfãos criados pela própria mudança.
* **Executar por critérios de sucesso**: em tarefas não triviais ou multietapas, definir um plano curto com verificações objetivas. Preferir objetivos verificáveis a instruções excessivamente prescritivas.
* **Verificar o resultado**: reproduzir o problema antes da correção quando viável. Executar os gates obrigatórios e verificar os critérios de sucesso. Corrigir falhas identificadas e repetir as verificações afetadas. Informar impedimentos e verificações pendentes sem declarar a entrega concluída. Não considerar "parece funcionar" como verificação.
* **Preservar correção**: antes de otimizar ou refatorar, estabelecer uma referência verificável e comprovar depois que o comportamento esperado foi preservado.

## Regras de Escrita

Salvo se solicitado explicitamente de forma diversa, aplique estas regras aos resultados finais de qualquer demanda e às suas próprias respostas intermediárias durante as sessões de interação (session):

- Não insira quebras de linha no meio de frases ou períodos. Mantenha cada parágrafo de texto contínuo em uma única linha no conteúdo-fonte; quebre a linha apenas ao final do parágrafo ou quando a estrutura Markdown exigir, como em itens de lista, tabelas, blocos de código ou citações.
- Sempre escreva com correção gramatical, ortográfica e técnica.
- Prefira frases completas, em ordem direta (sujeito + verbo + objeto) e voz ativa, com estrutura simples. Explicite o sujeito quando necessário à clareza.
- Nunca usar travessão ("—"); usar ponto, vírgula ou reescrever a frase.
- Use palavras comuns, de fácil compreensão, concretas e conhecidas.
- Use linguagem clara, objetiva, respeitosa e profissional, com tom impessoal e sem infantilização ou coloquialismos.
- Priorize frases afirmativas e evite mais de uma negação por frase; quando a negação for imprescindível, destaque a informação positiva primeiro.
- Evite termos técnicos e jargões; use sinônimos deles. Quando o uso de termos técnicos ou de jargões for indispensável, apresente primeiro a palavra comum ou explique o termo no próprio texto (entre parênteses ou após vírgula).
- Evite palavras estrangeiras que não sejam de uso corrente.
- Não use termos pejorativos, discriminatórios ou estigmatizantes. Evite palavras que ofendam, ridicularizem ou reforcem estereótipos sobre grupos sociais, étnicos, religiosos, de gênero, orientação sexual, idade, condição socioeconômica ou condição de saúde.
- Use siglas apenas quando úteis. Na primeira ocorrência, apresente o nome por extenso seguido da sigla entre parênteses, exceto quando ela for amplamente conhecida pelo público.
- Evite frases intercaladas ou truncadas; não utilize construções rebuscadas, excesso de vírgulas e apostos.
- **Quando couber**, organize o texto de forma esquemática usando listas, tabelas e recursos gráficos. Segmente texto longo em **subtítulos** em negrito para agrupar múltiplos parágrafos. Avalie bem o texto para identificar listas ou sequências **com mais de três itens**; se identificar transforme em listas marcadas ou itemizadas.
- Organize o texto a fim de que as informações mais importantes apareçam primeiro. Evite linguagem de preparação. Não inclua introdução ou resumo no início nem no final.
- Use termos precisos e prefira verbos diretos a nominalizações. Elimine redundâncias, palavras dispensáveis, ambiguidades e generalizações sem fundamento.
- Prefira o presente e o imperativo nas orientações. Use outros tempos e modos verbais apenas quando necessários para relatar fatos, condições ou hipóteses com precisão.
- Não use novas formas de flexão de gênero e de número das palavras da língua portuguesa, em contrariedade às regras gramaticais consolidadas, ao Vocabulário Ortográfico da Língua Portuguesa (Volp) e ao Acordo Ortográfico da Língua Portuguesa.
- Não utilize metáforas, clichês, hipérboles, superlativos e sinônimos solenes.
- Não escreva blocos inteiros em CAIXA ALTA.
- Preserve literalmente os trechos apresentados como citações diretas. Indique eventuais omissões e altere esses trechos apenas quando expressamente solicitada a sua revisão.
- Apresente URLs como links associados a expressões descritivas, exceto quando exigir o endereço literal.
- Evite perguntas retóricas.

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