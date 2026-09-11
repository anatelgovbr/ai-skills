# Prompts de exemplo

## Sumário

- [Introdução](#introdução)
- [Como escrever um bom prompt](#como-escrever-um-bom-prompt)
- [stack-ai-init](#stack-ai-init)
  - [Instalar a stack em um repositório novo](#instalar-a-stack-em-um-repositório-novo)
  - [Conferir uma instalação antiga](#conferir-uma-instalação-antiga)
  - [Atualizar arquivos da stack que ficaram para trás](#atualizar-arquivos-da-stack-que-ficaram-para-trás)
- [stack-ai-build-project-context](#stack-ai-build-project-context)
  - [Enriquecer uma stack recém instalada](#enriquecer-uma-stack-recém-instalada)
  - [Mapear como se constrói uma unidade](#mapear-como-se-constrói-uma-unidade)
  - [Enriquecer só um subsistema](#enriquecer-só-um-subsistema)
  - [Atualizar a stack depois de uma mudança grande](#atualizar-a-stack-depois-de-uma-mudança-grande)
  - [Avaliar se algo merece virar skill](#avaliar-se-algo-merece-virar-skill)
- [dicionario-dados-db-scan-codebase-docs](#dicionario-dados-db-scan-codebase-docs)
  - [Criar o adaptador](#criar-o-adaptador)
  - [Criar o dicionário de dados](#criar-o-dicionário-de-dados)
  - [Atualizar o dicionário](#atualizar-o-dicionário)
  - [Revisar a qualidade do dicionário](#revisar-a-qualidade-do-dicionário)
  - [Gerar prints de tela como insumo complementar](#gerar-prints-de-tela-como-insumo-complementar)
- [gauntlet-loop-forge](#gauntlet-loop-forge)
  - [Forjar o prompt a partir de uma ideia](#forjar-o-prompt-a-partir-de-uma-ideia)
  - [Forjar o prompt a partir de uma especificação](#forjar-o-prompt-a-partir-de-uma-especificação)
  - [Otimizar um prompt que já existe](#otimizar-um-prompt-que-já-existe)
  - [Executar o prompt forjado](#executar-o-prompt-forjado)
- [ciclo-design](#ciclo-design)
  - [Rodar o ciclo com uma referência](#rodar-o-ciclo-com-uma-referência)
  - [Rodar o ciclo sem referência escolhida](#rodar-o-ciclo-sem-referência-escolhida)
  - [Continuar depois do limite de rodadas](#continuar-depois-do-limite-de-rodadas)

---

## Introdução

Este arquivo reúne prompts prontos para as skills deste repositório. São templates para adaptar ao seu caso e enviar, não ilustrações.

Antes de usar qualquer prompt daqui, copie a pasta da skill para o diretório de skills do seu projeto, como explica o `README.md` na raiz. O prompt cita a skill pelo nome, e o agente só encontra a skill se ela estiver instalada no projeto em que você está trabalhando.

As skills deste repositório são agnósticas: nenhuma delas depende da linguagem, do sistema ou da estrutura de um projeto específico. Por isso os prompts abaixo valem em qualquer repositório, e o que é específico do seu caso entra nos parâmetros.

---

## Como escrever um bom prompt

**Parâmetros.** Todo trecho entre `<` e `>` é um parâmetro: substitua pela informação real antes de enviar. Campo marcado como `<se souber>` ou `<se houver>` que você não tiver como preencher: apague a linha inteira. Nunca deixe o texto entre `<` e `>` dentro do prompt enviado, e não escreva "não sei" no lugar do campo. Se você não sabe, a linha não deveria estar lá.

**Adapte à vontade.** Nenhum prompt precisa ser enviado igual ao template. Linha que não se aplica ao seu caso, apague. Mande só o que você realmente tem. Quanto mais informação e validação você der junto do prompt, mais assertivo o agente tende a ser, mas isso não é obrigatório: um prompt mais enxuto também funciona.

**Trate o que você informa como pista.** O que você escreve no prompt orienta a investigação, não substitui a evidência. Peça ao agente para confirmar cada item contra o código ou a fonte estrutural e avisar quando algo divergir.

**Nunca cole segredo.** Antes de colar mensagem de erro, print de tela ou qualquer evidência bruta, remova, se forem de ambiente de produção:

- senha ou qualquer outra credencial
- dado pessoal (CPF, nome completo, e-mail, endereço)
- segredo, que são as senhas usadas pelos sistemas para conversarem entre si (token, chave de API, string de conexão)

Troque cada um desses valores por um texto genérico, mantendo claro o que está errado. Em ambiente de teste ou desenvolvimento, pode colar sem trocar nada.

**Vocabulário.** Onde os prompts pedem "a raiz do repositório", leia a pasta principal do projeto, aquela que contém todas as outras.

**A sessão continua.** Todo prompt daqui é o ponto de partida da sessão, não uma interação única. Depois do resultado, continue na mesma janela para ajustar, aprofundar ou corrigir.

---

## stack-ai-init

Prepara um repositório para trabalhar com agentes de IA. Leva para a raiz do destino a estrutura mínima da stack: os arquivos que os agentes leem, as skills que eles usam e as integrações das ferramentas suportadas.

É a primeira metade da dupla: esta põe a estrutura de pé, e a `stack-ai-build-project-context` a preenche depois com o conhecimento do sistema, em um pedido separado. Esta skill não lê o código do destino e não descreve o projeto.

Peça só o que você quer fazer. A skill já mostra o plano antes de escrever, preserva o que o destino tem e confere o que copiou, sem que isso precise entrar no prompt.

**Pré-requisito da seção:** o caminho da pasta raiz do repositório de destino em mãos. A skill nunca assume que é o repositório em que você está trabalhando.

### Instalar a stack em um repositório novo

**Prompt:**

```text
Use a skill `stack-ai-init` para instalar a stack de IA no repositório em <caminho da raiz>.
```

### Conferir uma instalação antiga

Use quando a stack já foi instalada há algum tempo e você quer saber se ela continua igual à versão distribuída hoje. A resposta é um relatório do que está diferente e do que está faltando.

**Pré-requisito:** a stack já instalada nesse repositório.

**Prompt:**

```text
Use a skill `stack-ai-init` para verificar a instalação da stack no repositório em <caminho da raiz>.
```

### Atualizar arquivos da stack que ficaram para trás

A autorização é obrigatória: sem ela, a skill preserva o que encontrar.

**Pré-requisito:** a conferência do prompt anterior já rodada, para você saber o que divergiu.

**Prompt:**

```text
Use a skill `stack-ai-init` no repositório em <caminho da raiz> para atualizar os arquivos
da stack que estão desatualizados.

Autorizo substituir os arquivos da stack que divergirem da versão distribuída hoje.
```

---

## stack-ai-build-project-context

Investiga o código de um repositório que já tem a estrutura instalada e transforma o que descobre em base de trabalho para os agentes: inventário e regras no `AGENTS.md`, skills de fluxo, references de detalhe e guardrails, todos derivados de evidência do próprio código. É a segunda metade da dupla: a `stack-ai-init` põe a estrutura de pé, esta aqui a preenche.

**Pré-requisito da seção:** a estrutura mínima já instalada pela `stack-ai-init`. Para a parte que empacota skills novas, a skill `skill-creator` precisa estar instalada junto, e a própria skill avisa antes de começar se ela faltar. Com agentes auxiliares a investigação corre em paralelo e a auditoria fica independente. Sem eles a rodada continua com independência menor, e a skill declara isso no relatório.

### Enriquecer uma stack recém instalada

**Pré-requisito:** stack instalada e ainda vazia.

**Prompt:**

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

**Prompt:**

```text
Use a skill `stack-ai-build-project-context` no repositório em <caminho da raiz>, focada em como se cria <página, endpoint, relatório, procedure> neste sistema.

Leia exemplares recentes e antigos por inteiro, reconstrua a sequência com o que é obrigatório e o que varia, e me proponha a skill de fluxo correspondente junto com os guardrails que ela deve carregar.
```

### Enriquecer só um subsistema

**Prompt:**

```text
Use a skill `stack-ai-build-project-context` no repositório em <caminho da raiz>, com escopo limitado a <subsistema, módulo ou conjunto de diretórios>.

Não investigue o resto do repositório nesta rodada. Se encontrar algo relevante fora do escopo, registre como pergunta no relatório em vez de investigar.
```

### Atualizar a stack depois de uma mudança grande

**Pré-requisito:** stack já com conteúdo escrito em rodadas anteriores.

**Prompt:**

```text
Use a skill `stack-ai-build-project-context` no repositório em <caminho da raiz>. A stack já tem conteúdo.

Leia o que já está registrado antes de investigar e me traga só o delta: o que mudou, o que passou a existir e, principalmente, o que hoje contradiz algum artefato já escrito. Rode os comandos registrados nas evidências como estão escritos e me diga quais não reproduzem o próprio número.

Contexto da mudança: <o que mudou no sistema, se souber>
```

### Avaliar se algo merece virar skill

**Prompt:**

```text
Use a skill `stack-ai-build-project-context` no repositório em <caminho da raiz> para avaliar se <tarefa recorrente> justifica uma skill própria.

Procure no código e no histórico a evidência de recorrência e a sequência que os exemplares mostram. Se a evidência não sustentar uma skill, me diga isso e proponha o destino correto em vez de criar a skill mesmo assim.
```

---

## dicionario-dados-db-scan-codebase-docs

Investiga o código do sistema, os arquivos que criam e alteram o banco e a documentação disponível para gerar e manter dicionários de dados. Além do dicionário, ela mantém o changelog estrutural, que é o histórico das mudanças na estrutura do banco. O alvo pode ser o sistema, um módulo, uma base corporativa ou um data warehouse, e todo alvo reconhecido precisa de um adaptador registrado, que é o arquivo onde a skill anota onde procurar cada coisa naquele alvo.

A ordem das seções abaixo é a ordem recomendada de uso. Crie o adaptador do alvo primeiro, em um pedido só dele. Depois, ao criar ou atualizar o dicionário, anexe os materiais complementares que você tiver (manuais, prints de tela, dicionário anterior, planilhas). Eles ajudam a confirmar a semântica de tabelas e colunas. Se ainda não tiver prints mas houver um ambiente de teste disponível, gere-os primeiro com "Gerar prints de tela como insumo complementar".

Não é preciso citar o adaptador do alvo: uma vez criado e registrado, a skill já sabe localizá-lo sozinha. Também não é preciso citar critérios de qualidade ou comandos de verificação internos à skill.

**Pré-requisito da seção:** acesso às fontes que definem a estrutura do banco, que podem ser o código do sistema, os arquivos de instalação e de migração ou o esquema do banco.

### Criar o adaptador

Use este prompt no primeiro contato com um alvo que a skill ainda não reconhece. Ele cria só o adaptador. Informe as convenções que você já souber, para reduzir as perguntas que a skill precisará fazer. O que você não souber, ela tenta descobrir no próprio código antes de perguntar.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o adaptador de <sistema ou módulo>. Investigue a codebase, crie o adaptador completo e registre-o. Não gere o dicionário de dados nem o changelog nesta etapa.

O que eu já sei sobre ele:
- pistas que identificam este sistema ou módulo (nome, caminhos, prefixo de tabela, pasta de documentação, ou o codebase/repositório em si, se for o sistema inteiro): <se souber, ex.: "prefixo pedidos_, models em app/Models/Pedido.php, migrations em database/migrations/">
- fonte estrutural e convenção de versionamento: <scripts de instalação, migrations, schema ou DDL, se souber, ex.: "migrations em migrations/Version20240115120000.php">
- precedência entre fontes, se houver mais de uma fonte estrutural para a mesma informação: <qual prevalece, se souber, ex.: "migration mais recente prevalece sobre o schema.sql legado">
- codificação, camadas e onde buscar no código: <se souber, ex.: "camadas Entity/Repository/Controller">
- títulos e pasta de destino dos dicionários: <se souber, ex.: "docs/dicionario_dados/abc/">
- particularidades ou exceções conhecidas: <se houver, ex.: "módulo tem tabela compartilhada com outro módulo, não duplicar no dicionário">

Trate os itens acima como pista, não como conclusão: confirme cada um contra a codebase e me avise se algum divergir.

Pergunte objetivamente só sobre o que não puder ser inferido nem foi informado acima. Justifique sua resposta.
```

### Criar o dicionário de dados

**Pré-requisito:** o adaptador do alvo criado e registrado, com o prompt anterior.

Use na primeira vez que for gerar o dicionário de um alvo. O material complementar pode ser de qualquer formato: esquema de banco em outra ferramenta, dicionário anterior, prints de tela, manuais, vídeos ou transcrições. A skill sempre confirma tudo contra as fontes estruturais antes de publicar qualquer descrição.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o dicionário de dados e o changelog estrutural de <sistema ou módulo>.

Investigue as fontes estruturais disponíveis (codebase, scripts de instalação, migrations, schemas ou DDLs) para identificar a convenção de versionamento e, quando houver codebase, onde ficam as regras de negócio. Aproveite também qualquer documentação já existente. Não publique como fato uma descrição cuja semântica não esteja suficientemente sustentada pelas evidências encontradas.

Considere como material complementar <se houver: arquivos anexados, esquema em outro formato, dicionário anterior, prints, manuais, vídeos, transcrições>. Dê atenção especial a <o material mais relevante, se houver mais de um>, mas confirme tudo contra a fonte estrutural disponível (código, esquema de banco ou DDL) antes de publicar qualquer descrição.

Ao final, informe explicitamente: as tabelas ou colunas cuja semântica você não conseguiu confirmar nas fontes disponíveis, o que faltou para confirmá-las, e onde algum material complementar divergiu da fonte estrutural e qual fonte você adotou. Justifique sua resposta.
```

### Atualizar o dicionário

**Pré-requisito:** dicionário e changelog já publicados para esse alvo.

Use quando quiser sincronizá-los com mudanças estruturais no alvo (novas tabelas, colunas ou regras de negócio) ou após uma nova versão. Também serve para corrigir uma descrição anterior, mas só diante de divergência estrutural confirmada ou domínio incompleto confirmado, nunca por ajuste de estilo.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para atualizar o dicionário de dados de <sistema ou módulo> para o estado mais recente da <codebase ou base>.

Compare o dicionário de dados e o changelog já existentes com a estrutura e as regras de negócio atuais e altere somente o que realmente mudou desde a última atualização, preservando o restante que não teve mudança sem alteração.

Se você souber a versão-alvo, os commits ou as migrations específicas da mudança, indique-os. Caso contrário, identifique o escopo da diferença pela própria codebase.

Considere como material complementar <se houver: arquivos anexados, esquema em outro formato, dicionário anterior, prints, manuais, vídeos, transcrições>. Dê atenção especial a <o material mais relevante, se houver mais de um>, mas confirme tudo contra a fonte estrutural disponível (código, esquema de banco ou DDL) antes de publicar qualquer descrição.

Ao final, liste o que foi alterado e o que foi preservado intencionalmente. Justifique sua resposta.
```

### Revisar a qualidade do dicionário

**Pré-requisito:** dicionário já publicado para esse alvo.

Use quando quiser avaliar se ele segue os critérios de qualidade e as convenções da própria skill, sem alterar nenhum arquivo e independentemente de o código ter mudado.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para revisar a qualidade e a consistência do dicionário de dados de <sistema ou módulo>, sem alterar nenhum arquivo.

Classifique cada achado como problema de qualidade documental (descrição incompleta, inconsistente, genérica ou fora das convenções da skill) ou como lacuna (elemento sem descrição). Liste claramente qualquer lacuna que impeça considerar a documentação completa. Justifique sua resposta.
```

### Gerar prints de tela como insumo complementar

**Pré-requisito:** um ambiente de teste do sistema no ar, uma ferramenta que controle o navegador automaticamente já configurada no projeto e uma senha de acesso que não seja a de produção.

Os prints gerados aqui podem ser apontados como material complementar em "Criar o dicionário de dados".

**Prompt:**

```text
Gere os prints de tela de <sistema ou módulo> para servir de insumo complementar ao
dicionário de dados (skill `dicionario-dados-db-scan-codebase-docs`).

O ambiente de teste de <sistema ou módulo> já está disponível em <endereço ou instrução
para subir o ambiente>. Para autenticar, leia a credencial de <variável de ambiente
ou arquivo local não versionado>. Se não houver, peça a credencial no momento do uso.
Nunca use credencial de produção.

Use <ferramenta de automação de navegador disponível no seu ambiente> para rodar um
script de automação que:

1. Faça login no ambiente de teste.
2. Navegue por todas as telas relevantes de <sistema ou módulo>, criando os dados de
   teste (seeds) necessários para preencher cada tela.
3. Capture um print de cada tela relevante (listagem, formulário vazio, formulário
   preenchido, modal, estado intermediário).
4. Salve os PNGs em <pasta de destino>/<nome-do-alvo>/screenshots/, organizados
   por subpasta.
5. Exporte os seeds/dados de teste usados no passo 2 (SQL de insert ou passo a passo
   reprodutível) em <pasta de destino>/<nome-do-alvo>/seeds/, para reaproveitar
   em futuras implementações sem recriar a massa de teste do zero.

Ao final, liste as telas que não conseguiu capturar e o motivo. Justifique sua resposta.
```

---

## gauntlet-loop-forge

Transforma uma ideia, um objetivo, uma especificação ou um prompt já existente em um único prompt pronto para colar, no método Gauntlet Loop: o agente que constrói nunca aprova o próprio trabalho, quem aprova é outro agente em conversa separada, a régua de qualidade precisa ser conferível e toda repetição tem um teto finito de esforço.

A skill entrevista antes de escrever. Ela extrai primeiro tudo que o material já responde e pergunta em blocos só o que faltar, incluindo uma pergunta em linguagem simples sobre o máximo de rodadas de melhoria e conferência. Quanto mais você trouxer no primeiro prompt, menos ela precisa perguntar.

Ela produz o prompt, não executa o trabalho descrito nele. Executar é um segundo pedido, normalmente em uma sessão nova.

### Forjar o prompt a partir de uma ideia

Use quando o ponto de partida é um objetivo na sua cabeça, sem documento nenhum.

**Prompt:**

```text
Use a skill `gauntlet-loop-forge` para transformar o objetivo abaixo em um prompt Gauntlet Loop pronto para colar. Não execute o trabalho descrito, só produza o prompt.

Objetivo: <o que precisa existir no final, em uma ou duas frases>
Onde o prompt vai rodar: <Claude Code, Codex, outro agente, ou chat comum>
Régua de qualidade que eu já tenho: <se souber, ex.: "a suíte de testes atual precisa continuar passando", "quero no nível de <exemplar concreto>">
Material que serve de fonte da verdade: <se houver: arquivos, issue, especificação, repositório>
O que não pode mudar: <se houver: comportamento, formato, compatibilidade>
O que os agentes podem fazer no ambiente: <ler, rodar teste, editar arquivo, acessar rede, publicar, gastar>
Ações que exigem minha aprovação: <se houver>

Me pergunte em bloco o que ainda faltar antes de escrever o prompt.
```

### Forjar o prompt a partir de uma especificação

Use quando já existe um documento, uma issue ou um repositório que manda no resultado.

**Pré-requisito:** o arquivo, a issue ou o repositório acessível ao agente dentro da sessão.

**Prompt:**

```text
Use a skill `gauntlet-loop-forge` para transformar <arquivo, issue ou especificação> em um prompt Gauntlet Loop pronto para colar.

Trate <arquivo, issue ou especificação> como fonte da verdade: extraia dali os critérios de aceite, as restrições e o que está fora de escopo antes de me perguntar qualquer coisa. Me avise se encontrar contradição em vez de escolher um lado sozinho.

Me pergunte só o que não estiver no material. Não prescreva arquitetura, divisão de tarefas nem ordem de implementação: isso é decisão do agente líder na hora de executar.
```

### Otimizar um prompt que já existe

Use quando você já tem um prompt de loop rodando e quer saber onde ele falha.

**Prompt:**

```text
Use a skill `gauntlet-loop-forge` para diagnosticar e reescrever o prompt abaixo.

<cole aqui o prompt atual>

Aponte onde ele deixa quem constrói aprovar o próprio trabalho, onde a régua de qualidade não é conferível, onde a repetição não tem teto finito e onde ele manda usar comando ou flag que o meu ambiente não tem. Preserve as restrições que eu já escrevi e me diga o que mudou e por quê.
```

### Executar o prompt forjado

Use em uma sessão nova, colando o prompt que a skill produziu. O trecho abaixo do prompt serve para você conferir logo no começo que os limites e o registro de evidências ficaram claros.

**Pré-requisito:** uma ferramenta de IA que consiga abrir agentes auxiliares em conversa separada. O método divide o trabalho entre dois papéis, e os dois são agentes de IA: um deles produz o resultado, e outro, em uma conversa nova e sem ter acompanhado como o primeiro trabalhou, confere se o resultado atinge a régua combinada. Quando a ferramenta não abre essa segunda conversa, o mesmo agente faz os dois papéis e acaba aprovando o próprio trabalho, que é justamente o que o método existe para evitar. O prompt ainda roda assim, com resultado mais fraco, e a skill manda avisar você de que a separação não foi real.

**Prompt:**

```text
<cole aqui o prompt forjado>

Antes de começar, confirme em uma linha: quantas rodadas de melhoria e conferência você tem por parte do trabalho, quantos agentes vai abrir ao mesmo tempo e onde vai manter o registro de evidências.

Se algum teto for atingido antes da aprovação, pare e me devolva o estado CAPPED com os achados em aberto e a próxima ação recomendada. Atingir o teto nunca é aprovação, e nenhum limite é ampliado sem eu autorizar.
```

---

## ciclo-design

Recebe um objetivo e uma referência real e identifica o que torna essa referência boa. Depois põe quatro agentes de IA para trabalhar: um agente construtor, que cria e corrige a peça, e três agentes críticos, cada um em uma conversa separada e sem saber como o construtor trabalhou. Cada crítico olha uma coisa: se foi feito o que você pediu, se as regras do projeto foram respeitadas e se o resultado está no nível da referência. A peça só passa quando os três aprovam, ou o ciclo para no limite de rodadas.

A skill começa por uma entrevista de cinco perguntas e espera a resposta. Trazer as respostas já no primeiro prompt encurta essa etapa.

A referência é a parte mais importante do pedido. Com uma referência vaga, o agente crítico inventa o próprio padrão de qualidade e aprova fácil.

**Pré-requisito da seção:** uma ferramenta de IA que consiga abrir agentes auxiliares em conversa separada, porque é assim que os três críticos avaliam sem terem participado da construção. Some-se a isso alguma forma de ver o resultado pronto (captura de tela, sequência de imagens ou PDF) e as ferramentas que o seu objetivo exigir, como geração de imagem, vídeo ou voz. A skill confere tudo isso na fase de pré-verificação e diz qual crítico fica prejudicado se algo faltar.

### Rodar o ciclo com uma referência

**Pré-requisito:** a referência acessível ao agente, seja um link que ele consiga abrir ou um arquivo local.

**Prompt:**

```text
Use a skill `ciclo-design` para criar <o que será construído e qual é o tamanho ou a duração>.

Referência que eu considero excelente: <link de página, arquivo ou peça que eu consiga abrir>
Arquivos que você deve usar: <se houver: sistema de design, guia de marca, roteiro, versão atual>
Modelos: <ex.: "custo-benefício", ou o modelo de cada agente>
Máximo de rodadas: <número>

Siga com a entrevista se ainda faltar alguma coisa.
```

### Rodar o ciclo sem referência escolhida

**Prompt:**

```text
Use a skill `ciclo-design` para criar <o que será construído>.

Ainda não tenho referência escolhida: proponha três, explique em uma linha por que cada uma serviria e espere minha escolha antes de continuar.
```

### Continuar depois do limite de rodadas

Use quando o ciclo parou no limite com alguma reprovação em aberto.

**Pré-requisito:** a mesma sessão do ciclo anterior, ou a página de progresso que ele manteve.

**Prompt:**

```text
O ciclo parou no limite de rodadas com <crítico ou peça> ainda reprovado.

Mostre a principal lacuna atual, o que já foi tentado e quantas rodadas cada peça consumiu. Depois siga por mais <número> rodadas apenas em <peça>, sem mexer no que já foi aprovado.

Nenhuma reprovação vira aprovação por causa do limite.
```
