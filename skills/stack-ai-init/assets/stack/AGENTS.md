# Diretrizes de Desenvolvimento com IA

## Contexto do Projeto

## Dependências Técnicas do Projeto

## Escopo e Limites de Escrita

## Hierarquia de Autoridade

1. Instruções explícitas do desenvolvedor na conversa atual.
2. Este arquivo (`AGENTS.md`).

Em caso de conflito, parar e solicitar decisão ao desenvolvedor.

## Disciplina de Execução Agêntica

Aplicar com rigor proporcional à complexidade e ao risco, sem flexibilizar guardrails, gates ou regras específicas deste repositório:

* **Pensar antes de alterar**: explicitar premissas, inconsistências e tradeoffs relevantes. Em ambiguidade de contrato, requisito ou conflito documental, seguir "Regras de Decisão"; não inventar.
* **Simplicidade primeiro**: implementar a menor solução correta. Não adicionar funcionalidades, abstrações, configurabilidade, generalizações futuras ou tratamento de cenários não exigidos.
* **Mudanças cirúrgicas**: alterar somente o necessário, preservar estilo e comportamento adjacentes e remover apenas órfãos criados pela própria mudança.
* **Executar por critérios de sucesso**: em tarefas não triviais ou multietapas, definir um plano curto com verificações objetivas. Preferir objetivos verificáveis a instruções excessivamente prescritivas.
* **Verificar o resultado**: reproduzir o problema antes da correção quando viável. Executar os gates obrigatórios e verificar os critérios de sucesso. Corrigir falhas identificadas e repetir as verificações afetadas. Informar impedimentos e verificações pendentes sem declarar a entrega concluída. Não considerar "parece funcionar" como verificação.
* **Preservar correção**: antes de otimizar ou refatorar, estabelecer uma referência verificável e comprovar depois que o comportamento esperado foi preservado.

## Guardrails Universais

- Aplicar `.agents/security/guia-seguranca.md` em todo código novo ou alterado, e citar o identificador do tópico (S01 em diante) em cada achado de segurança.
- Revisão de segurança por procedimento OWASP: skill `owasp-playbook`, opt-in, pedida em uma frase. A ponte dela é `.agents/security/mapa-cwe-guia.md`, que traduz CWE para tópico do guia e recebe sinais, auditores, exceções, saídas e roteamento de correção do projeto.
- Nunca incluir senhas, chaves, tokens, arquivos `.env` ou outras credenciais em commits.
- Não concatenar entradas não confiáveis em SQL, HTML, JavaScript, shell ou URLs.
- Confirmar antes de executar ações destrutivas ou difíceis de reverter.
- Executar somente o que foi solicitado, sem alterações ou refatorações adicionais.

## Qualidade Mínima

- Ler integralmente cada arquivo antes de editá-lo.
- Executar os testes e verificações documentados pelo projeto para o código alterado.
- Corrigir falhas introduzidas pela alteração antes de concluir a tarefa.
- Não entregar código incompleto, morto ou com implementação pendente.

## Regras de Decisão

- Não inventar padrões, APIs ou convenções não documentadas.
- Em caso de ambiguidade de requisito ou contrato, perguntar ao desenvolvedor.
- Em caso de conflito entre documentos, parar e solicitar decisão.

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
