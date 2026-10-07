1. Pensar antes de agir
2. Simplicidade primeiro
3. Mudanças cirúrgicas
4. Execução orientada a objetivo

## Contexto do Projeto

## Dependências Técnicas do Projeto

## Escopo e Limites de Escrita

## Hierarquia de Autoridade

1. Instruções explícitas do desenvolvedor na conversa atual.
2. Este arquivo (`AGENTS.md`).

Em caso de conflito, parar e solicitar decisão ao desenvolvedor.

## Disciplina Agêntica

O rigor cresce com a complexidade e o risco; guardrails, gates e regras do projeto valem sempre.

### 1. Pensar antes de agir

**Não presumir. Não esconder dúvida. Expor tradeoffs.**

Antes de qualquer alteração:
- Declarar as premissas adotadas. Em dúvida, perguntar.
- Se existem várias interpretações, apresentar todas e nomear o ponto que falta; escolher em silêncio não é opção.
- Se existe caminho mais simples dentro dos padrões documentados, apresentar o caminho e a diferença e aguardar a escolha do desenvolvedor.
- Se algo não está claro, parar, nomear o que confunde e perguntar.
- Em conflito entre documentos, seguir "Regras de Decisão".

### 2. Simplicidade primeiro

**O mínimo que resolve o problema. Nada especulativo.**

- Sem funcionalidade além do pedido.
- Sem abstração para código de uso único.
- Sem "flexibilidade" ou "configurabilidade" que ninguém pediu.
- Sem tratamento de erro para cenário impossível.
- Se saíram 200 linhas e cabia em 50, reescrever.

Teste de saída: um revisor sênior da stack do projeto aprova o escopo sem ressalva de complexidade.

### 3. Mudanças cirúrgicas

**Tocar só no que o pedido exige. Limpar só a própria sujeira.**

Ao editar código existente:
- Código adjacente, comentários, formatação e o que não está quebrado ficam fora.
- Seguir o estilo existente, mesmo que o agente fizesse diferente.
- Código morto preexistente e problema fora do escopo ficam no código e entram na resposta como observação curta.
- Remover imports, variáveis e funções que a própria mudança deixou sem uso.

Teste de saída: cada linha alterada no diff responde a um trecho do pedido ou a uma regra documentada no projeto; linha sem uma dessas origens sai do diff.

### 4. Execução orientada a objetivo

**Definir critérios de sucesso verificáveis. Repetir até a verificação passar.**

Traduzir o pedido em critérios verificáveis:
- "Adicionar validação" → "listar as entradas inválidas, implementar, provar cada uma com comando".
- "Corrigir o bug" → "reproduzir com comando, corrigir, repetir o comando até passar".
- "Refatorar ou otimizar X" → "registrar o comportamento antes, alterar, comprovar o mesmo comportamento depois".

Antes da primeira edição, declarar plano com `Impacto Arquitetural` definido em "Decisões Arquiteturais" e `Checklist de Critérios Verificáveis` com um item por passo:

```
**Impacto Arquitetural:** <exige novo ADR / exige atualizar ADR / nenhum impacto>
- Dimensões: <dimensões tocadas>
- <nome do fator>: <motivo do fator valer para esta mudança>
- <nome do fator>: <motivo do fator valer para esta mudança>

**Checklist de Critérios Verificáveis:**
- [ ] [Step] → verify: [check]
- [ ] [Step] → verify: [check]
- [ ] [Step] → verify: [check]
```

Ao verificar:
- Executar os gates obrigatórios e os critérios de sucesso verificáveis.
- Repetir correção e verificação até todos passarem.
- Verificação que depende do desenvolvedor, como smoke manual, entra na resposta como pendente.
- Informar impedimentos e pendências sem declarar a entrega concluída.

Na resposta final, repetir o checklist com o resultado de cada item: `[x]` verificado por comando, com o comando e a saída; `[ ]` pendente ou com falha, com o motivo.

Teste de saída: cada item do checklist aparece na resposta final marcado, com o comando e o resultado; "parece funcionar" não conta.

## Guardrails Universais

- Ambiguidade relevante → não assumir, não adivinhar; explicitar ou perguntar
- Aplicar `.agents/security/guia-seguranca.md` em todo código novo ou alterado, e citar o identificador do tópico (S01 em diante) em cada achado de segurança.
- Revisão de segurança por procedimento OWASP: skill `owasp-playbook`, opt-in, pedida em uma frase. A ponte dela é `.agents/security/mapa-cwe-guia.md`, que traduz CWE para tópico do guia e recebe sinais, auditores, exceções, saídas e roteamento de correção do projeto.
- Nunca incluir senhas, chaves, tokens, arquivos `.env` ou outras credenciais em commits. Se identificar credencial em código existente, alertar o desenvolvedor antes de qualquer ação.
- Saída de scanner de segurança é triagem, não achado. Item só vira achado confirmado com o caminho do dado demonstrado, da entrada até o ponto de uso, citando arquivo e linha de cada salto. Sem esse rastro, reportar como hipótese e nunca como confirmado.
- Reconhecer somente `TODO:` como contexto de revisão. `TODO:` não bloqueia por si só e não dispensa gates obrigatórios. Dívida técnica preexistente e rastreada não bloqueia a mudança atual, salvo se houver risco crítico, dependência direta ou ampliação do risco.
- Não concatenar entradas não confiáveis em SQL, HTML, JavaScript, shell ou URLs.
- Confirmar antes de executar ações destrutivas ou difíceis de reverter.
- Executar somente o que foi solicitado, sem alterações ou refatorações adicionais.

## Qualidade Mínima

- Ler integralmente cada arquivo antes de editá-lo.
- Agrupar operações independentes (leituras, buscas, comandos shell) em uma única mensagem; executar em sequência somente quando houver dependência entre elas.
- Executar os testes e verificações documentados pelo projeto para o código alterado.
- Escrever cada teste novo no padrão AAA (Arrange, Act, Assert): preparar o cenário (Arrange), executar uma única ação sobre a unidade testada (Act) e verificar o resultado esperado (Assert), com os três blocos separados e visíveis no código e o nome do teste descrevendo o comportamento verificado.
- Corrigir falhas introduzidas pela alteração antes de concluir a tarefa.
- Não entregar código incompleto, morto ou com implementação pendente.

## Regras de Decisão

- Não inventar padrões, APIs ou convenções não documentadas.
- Citar o arquivo e a seção de origem ao justificar restrições, impedimentos, conflitos ou decisões que dependam de uma regra do repositório.
- Em caso de conflito entre documentos, parar e solicitar decisão.

## Decisões Arquiteturais

Toda mudança passa por esta triagem e o resultado é explicitado na linha "Impacto Arquitetural" da execução orientada a objetivo da Disciplina Agêntica, informando:
	- **Com impacto**: `exige novo ADR` ou `exige atualizar ADR`, com lista das Dimensões, nome de cada fator e motivo da mudança que justifica ADR novo ou atualização de ADR;
	- **Sem impacto**: `nenhum impacto` e o motivo da mudança não envolver fatores que justificam ADR novo ou atualização de ADR.

A mudança exige ADR novo ou atualização **QUANDO** atende às duas condições:

	1. Escolhe entre alternativas viáveis em pelo menos uma dimensão: estrutura, responsabilidade funcional (qual componente ou sistema responde por cada capacidade de negócio, processo ou dado mestre), atributo de qualidade, tecnologia ou dependência externa, interface ou contrato publicado e técnica de construção; e
	2. Tem pelo menos um destes fatores de significância:
	   - Difícil de reverter: desfazer exige migrar dados ou mudar, de forma coordenada, outros sistemas, equipes, consumidores ou cópias já distribuídas;
	   - Transversal: afeta várias partes do sistema ou a interação entre elas;
	   - Risco ou exigência externa: segurança, privacidade, conformidade legal, auditoria ou pedido de parte interessada crítica;
	   - Dependência sem controle: dependência externa fora do controle do time;
	   - Primeira vez: tecnologia ou padrão sem precedente no projeto; e
	   - Altera ADR: muda decisão registrada em ADR aceita.

Dispensam novo ADR ou atualização: implementação que segue padrão ou ADR vigente, correção que preserva a arquitetura, refatoração sem mudança de interface ou contrato, atualização compatível de dependência, edição do texto de documentação existente, mudança de regra de negócio que não muda qual componente responde por ela e decisão interna de componente autocontido, que fica na documentação do próprio componente.

Estados de uma ADR, em ordem: `proposta -> aceita -> descontinuada`.

- Toda ADR nasce `proposta` e só pode ser editada ou descartada enquanto estiver `proposta`.
- ADR `aceita` não é editada. Só muda de estado, para `descontinuada`.
- `exige novo ADR`: nenhuma ADR `proposta` trata do assunto. Se uma ADR `aceita` trata, a nova leva "Substitui: ADR-NNN", e a anterior passa a `descontinuada`, com "Substituída por: ADR-MMM", quando a nova for aceita.
- `exige atualizar ADR`: uma ADR `proposta` trata do assunto. Edite-a.

Se a mudança tocar uma dimensão, liste `docs/architecture/adr/`, abra só as ADRs cujo título trate do mesmo assunto e confira pelo Status se a mudança segue ou altera uma ADR aceita. Quando a triagem indicar ADR, pare antes de editar, informe a dimensão e o fator, sugira um título curto e aguarde a decisão do desenvolvedor. Com a ADR aprovada, siga as regras de `docs/architecture/adr/README.md`.

## Requisitos Ancorados

`docs/requisitos-ancorados/` descreve o comportamento vigente do sistema: regras de negócio (`RN`), requisitos funcionais (`RF`) e requisitos técnicos (`RT`). Formato, IDs e templates em `docs/requisitos-ancorados/padrao/README.md`.

- **Antes de alterar o sistema**: ler os requisitos de `docs/requisitos-ancorados/` ligados à mudança. Divergência entre requisito e código: parar, citar arquivo e linha dos dois lados e perguntar qual vale; nunca corrigir requisito ou código em silêncio.
- **Especificação da feature (Spec Kit)**: preencher "Requisitos Ancorados Afetados" com cada ID que a mudança adiciona, altera ou retira; projeto sem requisitos documentados: "Nenhum".
- **Tarefas (Spec Kit)**: com ID afetado, a última fase inclui a tarefa "Atualizar `docs/requisitos-ancorados/` com os IDs de Requisitos Ancorados Afetados".
- **Entrega**: na mesma entrega do código, os arquivos de requisitos passam a descrever o novo estado. Requisito retirado sai do arquivo. ID novo usa o número seguinte ao maior já usado, conferido também no histórico do Git; nenhum ID é reutilizado.
- **Resposta final**: listar cada ID adicionado, alterado ou retirado, com o motivo em uma frase, para a descrição da MR.
- **Motivo**: os documentos de requisitos não têm campo de origem nem de justificativa; o motivo de cada mudança vai na descrição da MR ou na ADR. Nunca inventar motivo de negócio nem explicar requisito pela leitura do código. Requisito novo sem fonte conhecida: perguntar ao desenvolvedor.
- **Mudança técnica**: passa pela triagem de "Decisões Arquiteturais"; com ADR, o requisito técnico cita o número da ADR e só muda quando a ADR estiver `aceita`.
- **Projeto sem requisitos documentados**: não criar os requisitos sem pedido do desenvolvedor; com pedido, documentar só a parte que a mudança toca, a partir dos templates `docs/requisitos-ancorados/padrao/TEMPLATE-*.md`.

Teste de saída: o diff altera `docs/requisitos-ancorados/` sempre que altera comportamento, restrição ou requisito de qualidade descrito ali, ou a resposta explica por que não altera.

## Regras de Escrita

Salvo solicitação explícita em contrário, aplique estas regras às mensagens em linguagem natural destinada a pessoas durante a sessão e aos entregáveis textuais em português brasileiro. Em código, comandos, identificadores, nomes de APIs, caminhos, dados estruturados e outros elementos definidos por linguagem, formato, protocolo ou projeto, preserve a sintaxe, o idioma e as convenções próprios do artefato. Instruções específicas do entregável prevalecem sobre estas regras gerais de estilo.

Em prosa Markdown, mantenha cada parágrafo em uma única linha no conteúdo-fonte e quebre linhas apenas entre parágrafos ou quando a estrutura do formato exigir. Use português brasileiro correto, linguagem clara, objetiva, respeitosa e profissional, voz ativa e frases completas. Não use travessão. Prefira palavras comuns, verbos diretos e afirmações precisas. Evite preâmbulos, redundâncias, coloquialismos, metáforas, clichês, hipérboles, construções rebuscadas, excesso de negativas e perguntas retóricas.

Use termos técnicos quando forem necessários à precisão ou forem a denominação canônica no contexto de desenvolvimento. Explique na primeira ocorrência os termos que possam não ser conhecidos pelo público do texto. Use siglas somente quando úteis e apresente o nome por extenso na primeira ocorrência, salvo siglas amplamente conhecidas. Não traduza nem adapte código, identificadores, comandos, nomes próprios de tecnologias ou outros termos que precisem permanecer literais.

Apresente primeiro a informação mais importante e evite introduções ou resumos que apenas repitam o conteúdo. Use subtítulos, listas e tabelas quando melhorarem a leitura, especialmente em textos longos ou sequências extensas, sem fragmentar artificialmente o texto. Siga a norma-padrão do português brasileiro e não crie flexões incompatíveis com ela.

Preserve literalmente citações diretas e outros conteúdos que precisem permanecer exatos, salvo solicitação expressa de revisão. Apresente URLs como links associados a expressões descritivas quando o formato permitir.
