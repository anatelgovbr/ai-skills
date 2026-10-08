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
  - [Atualizar a stack depois de uma mudança grande](#atualizar-a-stack-depois-de-uma-mudança-grande)
- [configuracao-de-testes-unitarios](#configuracao-de-testes-unitarios)
  - [Projeto sem testes](#projeto-sem-testes)
  - [Projeto que já tem testes](#projeto-que-já-tem-testes)
  - [Projeto que roda em Docker](#projeto-que-roda-em-docker)
  - [Projeto sem Docker](#projeto-sem-docker)
  - [Analisar o repositório e planejar os testes unitários](#analisar-o-repositório-e-planejar-os-testes-unitários)
- [dicionario-dados-db-scan-codebase-docs](#dicionario-dados-db-scan-codebase-docs)
  - [Criar o adaptador](#criar-o-adaptador)
  - [Criar o dicionário de dados](#criar-o-dicionário-de-dados)
  - [Atualizar o dicionário](#atualizar-o-dicionário)
  - [Revisar a qualidade do dicionário](#revisar-a-qualidade-do-dicionário)
  - [Gerar prints de tela como insumo complementar](#gerar-prints-de-tela-como-insumo-complementar)
- [manual-creator-scan-codebase](#manual-creator-scan-codebase)
  - [Preparar o adaptador do manual](#preparar-o-adaptador-do-manual)
  - [Criar um manual de uso](#criar-um-manual-de-uso)
  - [Atualizar um manual de uso](#atualizar-um-manual-de-uso)
  - [Verificar um manual sem escrita](#verificar-um-manual-sem-escrita)
- [gauntlet-loop-forge](#gauntlet-loop-forge)
  - [Criar o prompt a partir de uma ideia](#criar-o-prompt-a-partir-de-uma-ideia)
  - [Criar o prompt a partir de uma especificação](#criar-o-prompt-a-partir-de-uma-especificação)
  - [Otimizar um prompt que já existe](#otimizar-um-prompt-que-já-existe)
  - [Executar o prompt criado](#executar-o-prompt-criado)
- [ciclo-design](#ciclo-design)
  - [Rodar o ciclo com uma referência](#rodar-o-ciclo-com-uma-referência)
  - [Rodar o ciclo sem referência escolhida](#rodar-o-ciclo-sem-referência-escolhida)
  - [Continuar depois do limite de rodadas](#continuar-depois-do-limite-de-rodadas)
- [recapitulacao-resumo-ata-relato-reuniao](#recapitulacao-resumo-ata-relato-reuniao)
  - [Registrar uma reunião a partir da transcrição](#registrar-uma-reunião-a-partir-da-transcrição)
  - [Registrar uma reunião a partir da gravação no Teams](#registrar-uma-reunião-a-partir-da-gravação-no-teams)
- [escrita-em-linguagem-simples-pt-br](#escrita-em-linguagem-simples-pt-br)
  - [Reescrever um texto colado](#reescrever-um-texto-colado)
  - [Reescrever um arquivo ou uma página](#reescrever-um-arquivo-ou-uma-página)
- [conformidade-de-escrita-normativa](#conformidade-de-escrita-normativa)
  - [Analisar a minuta inteira](#analisar-a-minuta-inteira)
  - [Analisar só alguns dispositivos](#analisar-só-alguns-dispositivos)

---

## Introdução

Este arquivo reúne prompts prontos para as skills deste repositório. São templates para adaptar ao seu caso e enviar, não ilustrações.

Antes de usar qualquer prompt daqui, copie a pasta da skill para o diretório de skills do seu projeto, como explica o `README.md` na raiz. O prompt cita a skill pelo nome, e o agente só encontra a skill se ela estiver instalada no projeto em que você está trabalhando. A exceção é a `stack-ai-init`, que você também pode rodar a partir deste repositório clonado, informando o caminho do destino.

As skills deste repositório são agnósticas: nenhuma delas depende da linguagem, do sistema ou da estrutura de um projeto específico. Por isso os prompts abaixo valem em qualquer repositório, e o que é específico do seu caso entra nos parâmetros.

---

## Como escrever um bom prompt

O `AGENTS.md` do projeto é carregado em toda sessão e concentra as regras dele, então os prompts abaixo não repetem o que já está lá. Repita uma orientação do `AGENTS.md` dentro de um prompt só quando quiser reforçar um ponto muito crítico, para reduzir o risco de o agente falhar justamente nesse ponto.

O `AGENTS.md` e as skills definem as regras de execução. Os prompts informam o objetivo, o alvo e as escolhas específicas de cada pedido.

**Parâmetros.** Nos blocos para copiar, os campos entre `<` e `>` são informações que você deve preencher. Se um campo trouxer uma condição, como "se souber", "se houver", "se existir", "se não for" ou "opcional", e ela não valer para o seu caso, apague a linha inteira. Substitua os demais campos antes de enviar e nunca envie um prompt com texto entre `<` e `>` ainda dentro dele. Quando faltar uma informação necessária, descreva o que você sabe; o agente pode investigar ou pedir o dado que falta. Datas, identificadores e nomes de arquivos de saída são gerados pelo agente.

**Adapte à vontade.** Nenhum prompt precisa ser enviado igual ao template. Apague a linha que não se aplica ao seu caso e mande só o que você tem de fato: quanto mais informação e validação você der, mais assertivo o agente tende a ser, mas um prompt enxuto também funciona.

**Trate o que você informa como pista.** O que você escreve no prompt orienta a investigação, não substitui a evidência. Apresente suspeitas como hipóteses e peça ao agente para confirmar cada item contra o código ou a fonte estrutural e avisar quando algo divergir.

**Nunca cole segredo.** Antes de enviar mensagem de erro, print de tela ou qualquer evidência bruta, oculte estes valores reais, independentemente do ambiente:

- senha ou qualquer outra credencial
- dado pessoal (CPF, nome completo, e-mail, endereço)
- segredo, que são as senhas usadas pelos sistemas para conversarem entre si (token, chave de API, credencial na configuração de conexão)

Troque cada valor por um texto genérico, mantendo claro o que está errado. Ambientes de teste e desenvolvimento também podem conter credenciais válidas ou dados reais.

**Regra de negócio não documentada.** Se a regra não estiver escrita em lugar nenhum do repositório, escreva a regra no próprio prompt.

**Vocabulário.** Onde os prompts pedem "a raiz do repositório", leia a pasta principal do projeto, aquela que contém todas as outras.

**A sessão continua.** Todo prompt daqui é só o ponto de partida da sessão, não uma interação única. Depois do resultado, continue na mesma janela para ajustar, aprofundar ou corrigir o que vier. Se quiser guardar o conteúdo da sessão (achados, relatório, decisão), peça ao agente para salvar em um arquivo Markdown (`.md`) na pasta `specs/`. Ela fica fora do versionamento quando o `.gitignore` do projeto a ignora, como faz a `stack-ai-init` quando o projeto ainda não tem essa pasta.

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
Use a skill `stack-ai-init` no repositório em <caminho da raiz> para atualizar os arquivos da stack que estão desatualizados.

Autorizo substituir os arquivos da stack que divergirem da versão distribuída hoje.
```

---

## stack-ai-build-project-context

Investiga o código de um repositório que já tem a estrutura instalada e transforma o que descobre em base de trabalho para os agentes: inventário e regras no `AGENTS.md`, skills de fluxo, references de detalhe e guardrails, todos derivados de evidência do próprio código. É a segunda metade da dupla: a `stack-ai-init` põe a estrutura de pé, esta aqui a preenche.

**Pré-requisito da seção:** a estrutura mínima já instalada pela `stack-ai-init`. Para a parte que empacota skills novas, a skill `skill-creator` precisa estar instalada junto, e a própria skill avisa antes de começar se ela faltar. Com agentes auxiliares a investigação corre em paralelo e a auditoria fica independente. Sem eles a rodada continua com independência menor, e a skill declara isso no relatório.

### Enriquecer uma stack recém instalada

**Pré-requisito:** stack instalada.

**Prompt:**

```text
Use a skill `stack-ai-build-project-context` no repositório em <caminho da raiz>. A stack mínima já está instalada.

Descubra como este sistema é construído e como se desenvolve nele.

O que eu já sei sobre ele:
- o que o sistema faz: <se souber>
- partes que costumam dar problema para quem chega: <se souber>
- pontos que eu considero fora do escopo desta rodada: <se houver>
```

### Atualizar a stack depois de uma mudança grande

Use quando o sistema mudou e o conhecimento que a skill escreveu precisa acompanhar. Para atualizar os arquivos que a `stack-ai-init` distribui, use [Atualizar arquivos da stack que ficaram para trás](#atualizar-arquivos-da-stack-que-ficaram-para-trás).

**Pré-requisito:** stack já com conteúdo escrito em rodadas anteriores.

**Prompt:**

```text
Use a skill `stack-ai-build-project-context` no repositório em <caminho da raiz>. A stack já tem conteúdo.

Contexto da mudança: <o que mudou no sistema, se souber>
```

---

## configuracao-de-testes-unitarios

Lê o projeto e devolve um plano para configurar os testes unitários e a cobertura, sem meta de cobertura. A skill só lê: quem executa o plano é você, com o agente, depois de aprovar.

Os prompts de situação, com ou sem testes, e os de ambiente, com ou sem Docker, se combinam: junte em um só pedido as linhas que descrevem o seu projeto.

### Projeto sem testes

Use quando o projeto nunca teve teste automatizado.

**Prompt:**

```text
Use a skill `configuracao-de-testes-unitarios` para planejar a configuração de testes unitários no repositório em <caminho da raiz>.
- Situação do projeto: ainda não tem nenhum teste
```

### Projeto que já tem testes

Use quando o projeto já tem testes e você quer saber como rodá-los e como medir quanto do código eles exercitam.

**Prompt:**

```text
Use a skill `configuracao-de-testes-unitarios` no repositório em <caminho da raiz>.
- Situação do projeto: já tem testes
```

### Projeto que roda em Docker

Use quando a aplicação sobe em contêiner, pelo Docker.

**Prompt:**

```text
Use a skill `configuracao-de-testes-unitarios` para planejar a configuração de testes unitários no repositório em <caminho da raiz>.
- Ambiente: a aplicação roda em Docker
- Serviço da aplicação: <nome do serviço, se souber>
```

### Projeto sem Docker

Use quando a aplicação roda direto na máquina, sem contêiner.

**Prompt:**

```text
Use a skill `configuracao-de-testes-unitarios` para planejar a configuração de testes unitários no repositório em <caminho da raiz>.
- Ambiente: o projeto não usa Docker e roda direto na máquina
```

### Analisar o repositório e planejar os testes unitários

Use quando, além do plano de configuração, você quer saber por onde começar a escrever os testes. Essa análise fica fora do que a skill entrega e vem depois do plano.

**Prompt:**

```text
Use a skill `configuracao-de-testes-unitarios` para analisar o repositório em <caminho da raiz> e montar o plano de configuração dos testes unitários.

Depois de entregar o plano, traga uma análise com:
- Testável sem refatoração: as unidades que já podem ser testadas isoladamente, sem mexer no código, com o caminho de cada uma
- Partes críticas: as que merecem prioridade nos primeiros testes, com o caminho e o motivo de cada uma; considere crítica a unidade com regra de negócio, cálculo ou validação, priorizando as que mais mudaram no histórico do versionamento
```

---

## dicionario-dados-db-scan-codebase-docs

Investiga o código do sistema, os arquivos que criam e alteram o banco e a documentação disponível para gerar e manter dicionários de dados. Além do dicionário, ela mantém o changelog estrutural, que é o histórico das mudanças na estrutura do banco. Ela nasceu de um documento conceitual apoiado na família de normas ISO/IEC de qualidade de dados e metadados (ISO 8000-1, ISO/IEC 25012/25024 e ISO/IEC 11179), guardado em `references/` dentro da própria skill. O alvo pode ser o sistema, um módulo, uma base corporativa ou um data warehouse.

Todo alvo reconhecido precisa de um adaptador registrado. O adaptador é o arquivo que ensina a skill a localizar, investigar e versionar esse alvo: onde fica a fonte estrutural, qual fonte tem precedência quando houver mais de uma, como a versão é identificada e onde buscar no código. Ele fica em `adapters/<família>/<caminho-do-adaptador>.md`, listado em `registro-adaptadores.md`, ambos na raiz da skill. Sem ele registrado, a skill se recusa a gerar o dicionário e aponta a lacuna.

A skill gera três artefatos de saída: `dicionario_tabelas.md` e `dicionario_colunas.md`, com as descrições semânticas, e `CHANGELOG.md`, com o changelog estrutural.

A ordem das seções abaixo é a ordem recomendada de uso. Crie o adaptador do alvo primeiro, em um pedido só dele. Depois, ao criar ou atualizar o dicionário, anexe os materiais complementares que você tiver (manuais, prints de tela, dicionário anterior, planilhas). Eles ajudam a confirmar a semântica de tabelas e colunas. Se ainda não tiver prints mas houver um ambiente de teste disponível, gere-os primeiro com "Gerar prints de tela como insumo complementar".

Não é preciso citar o adaptador do alvo: uma vez criado e registrado, a skill já sabe localizá-lo sozinha. Também não é preciso citar critérios de qualidade ou comandos de verificação internos à skill.

**Pré-requisito da seção:** acesso às fontes que definem a estrutura do banco, que podem ser o código do sistema, os arquivos de instalação e de migração ou o esquema do banco.

### Criar o adaptador

Use este prompt no primeiro contato com um alvo que a skill ainda não reconhece, seja o sistema, um módulo ou uma base de dados corporativa. Ele cria só o adaptador. Gere o dicionário depois, em um pedido separado, com o prompt "Criar o dicionário de dados" a seguir. Informe as convenções que você já souber, para reduzir as perguntas que a skill vai precisar fazer. O que você não souber, ela tenta inferir da codebase antes de perguntar.

A skill pode concluir que um adaptador já registrado cobre o alvo e apenas registrar o alvo nele, em vez de criar um arquivo novo. Isso não é falha do pedido.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o adaptador do alvo abaixo. Investigue a codebase, crie o adaptador completo e registre-o. Não gere o dicionário de dados nem o changelog nesta etapa.

Alvo: <sistema ou módulo>.

O que eu já sei sobre ele:
- pistas que identificam este sistema ou módulo (nome, caminhos, prefixo de tabela, pasta de documentação, ou a própria codebase, se for o sistema inteiro): <se souber, ex.: "prefixo pedidos_, models em app/Models/Pedido.php, migrations em database/migrations/">
- fonte estrutural e convenção de versionamento: <scripts de instalação, migrations, schema ou DDL, se souber, ex.: "migrations em migrations/Version20240115120000.php">
- precedência entre fontes, se houver mais de uma fonte estrutural para a mesma informação: <qual prevalece, se souber, ex.: "migration mais recente prevalece sobre o schema.sql legado">
- codificação, camadas e onde buscar no código: <se souber, ex.: "camadas Entity/Repository/Controller">
- títulos e pasta de destino dos dicionários: <se souber, ex.: "docs/dicionario_dados/pedidos/">
- particularidades ou exceções conhecidas: <se houver, ex.: "módulo tem tabela compartilhada com outro módulo, não duplicar no dicionário">

Confira no código cada item que informei acima e me avise se encontrar divergência.

Pergunte objetivamente só sobre o que não puder ser inferido nem tiver sido informado acima.
```

### Criar o dicionário de dados

**Pré-requisito:** o adaptador do alvo criado e registrado, com o prompt anterior.

Use este prompt na primeira vez que for gerar o dicionário de um sistema ou módulo. Anexar material complementar aumenta o contexto negocial disponível para a skill e tende a melhorar a qualidade do resultado. Pode ser qualquer formato: esquema de banco em outra ferramenta, dicionário anterior, prints de tela, manuais, vídeos ou transcrições. Cite os materiais que tiver e, se houver mais de um, indique qual é o material prioritário. A skill sempre confere as informações com base nas fontes estruturais disponíveis (codebase, esquema de banco ou DDL) antes de publicar qualquer descrição, com ou sem material complementar.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o dicionário de dados e o changelog estrutural do alvo abaixo.

Alvo: <sistema ou módulo>.

Investigue as fontes estruturais disponíveis (codebase, scripts de instalação, migrations, schemas ou DDLs) para identificar a convenção de versionamento e, quando houver codebase, onde ficam as regras de negócio. Aproveite também qualquer documentação já existente. Só publique uma descrição quando as evidências encontradas sustentarem a semântica dela; sem essa sustentação, marque a descrição como não confirmada.

Materiais complementares: <arquivos anexados, esquema em outro formato, dicionário anterior, capturas de tela, manuais, vídeos ou transcrições, se houver>.
Material prioritário: <arquivo ou material ao qual dar mais atenção, opcional>.

Confira as informações dos materiais com base na fonte estrutural disponível (código, esquema de banco ou DDL) antes de publicar qualquer descrição.

Ao final, informe explicitamente: 1) as tabelas ou colunas cuja semântica você não conseguiu confirmar nas fontes disponíveis; 2) o que faltou para confirmá-las; 3) os pontos em que algum material complementar divergiu da fonte estrutural, com a fonte que você adotou.
```

### Atualizar o dicionário

**Pré-requisito:** dicionário e changelog já publicados para esse alvo.

Use quando quiser sincronizá-los com as mudanças estruturais do sistema ou do módulo (novas tabelas, colunas ou regras de negócio), inclusive depois de uma nova versão. Também serve para corrigir uma descrição anterior, mas só quando houver divergência estrutural ou domínio incompleto já confirmado, nunca por ajuste de estilo.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para atualizar o dicionário de dados conforme o estado mais recente das fontes disponíveis.

Alvo: <sistema ou módulo>.

Compare o dicionário de dados e o changelog já existentes com a estrutura e as regras de negócio atuais e altere somente o que realmente mudou desde a última atualização, preservando os demais conteúdos.

Referência da atualização: <versão, commits ou scripts de mudança, se souber>. Se eu não indicar a referência, identifique o escopo da diferença pelas próprias fontes estruturais.

Materiais complementares: <arquivos anexados, esquema em outro formato, dicionário anterior, capturas de tela, manuais, vídeos ou transcrições, se houver>.
Material prioritário: <arquivo ou material ao qual dar mais atenção, opcional>.

Confira as informações dos materiais com base na fonte estrutural disponível (código, esquema de banco ou DDL) antes de publicar qualquer descrição.

Ao final, liste o que foi alterado e o que foi preservado intencionalmente.
```

### Revisar a qualidade do dicionário

**Pré-requisito:** dicionário já publicado para esse alvo.

Use quando quiser avaliar se ele segue os critérios de qualidade e as convenções da própria skill (completude, consistência, terminologia, distinções documentadas), sem alterar arquivos. A revisão também compara a estrutura documentada com a fonte estrutural e aponta as divergências sem corrigi-las; para incorporar mudanças do código, use "Atualizar o dicionário".

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para revisar a qualidade e a consistência do dicionário de dados do alvo abaixo.

Alvo: <sistema ou módulo>.

Classifique cada achado como problema de qualidade documental (descrição incompleta, inconsistente, genérica ou fora das convenções da skill), como lacuna (elemento sem descrição) ou como divergência estrutural (tabela ou coluna documentada de forma diferente da fonte estrutural).
```

### Gerar prints de tela como insumo complementar

**Pré-requisito:** um ambiente de teste do sistema no ar, local ou remoto, uma ferramenta que controle o navegador, como Playwright ou Selenium, que a ferramenta de IA da sua sessão consiga executar, e uma credencial de teste que não seja a de produção. Qualquer ajuste de configuração feito só para habilitar a automação é local e não deve ser comitado.

Os prints gerados aqui podem ser apontados como material complementar em "Criar o dicionário de dados".

**Prompt:**

```text
Gere os prints de tela do alvo abaixo para servirem de insumo complementar ao dicionário de dados (skill `dicionario-dados-db-scan-codebase-docs`).

Alvo: <sistema ou módulo>.

O ambiente de teste já está disponível em <endereço ou instrução para subir o ambiente>. Para autenticar, leia a credencial na <variável de ambiente ou arquivo local não versionado>; se não houver, pare e me peça para configurá-la nesse local, sem recebê-la pela conversa. Nunca use credencial de produção.

Use <ferramenta de automação de navegador disponível, ex.: Playwright ou Selenium> para rodar um script de automação que:

1. Faça login no ambiente de teste.
2. Navegue pelas telas que leem ou gravam as tabelas do alvo, criando os dados de teste (seeds) necessários para preencher cada tela. Se o ambiente for remoto ou compartilhado, confirme comigo antes de criar dados.
3. Capture um print de cada uma dessas telas (listagem, formulário vazio, formulário preenchido, modal, estado intermediário).
4. Salve os PNGs em <pasta de destino>/screenshots/, organizados por subpasta.
5. Exporte os seeds e dados de teste usados no passo 2 (SQL de insert ou passo a passo reprodutível) em <pasta de destino>/seeds/, para reaproveitar em futuras implementações sem recriar a massa de teste do zero.

Ao final, liste as telas que não conseguiu capturar e o motivo de cada uma.
```

---

## manual-creator-scan-codebase

Cria e mantém manuais de uso no destino declarado pelo adaptador, que por padrão é `docs/manuais/<slug_do_manual>.md`, com imagens em `docs/manuais/imagens-<slug_do_manual>/`. Primeiro combina entrevista e inspeção da codebase para preparar o adaptador do sistema; depois conecta tarefas e personas às telas, campos, textos, regras e permissões para redigir o manual em linguagem simples. O pedido de manual inclui criar o adaptador necessário, e também é possível preparar somente o adaptador.

Informe o público e as tarefas que conhece. A skill investiga antes de perguntar pelas lacunas e não presume que um perfil de acesso define sozinho uma persona. O renderizador e a logo permitem verificar a apresentação do Markdown; ter acesso ao código não comprova a versão implantada nem substitui observação de conteúdo dinâmico. Não anexe capturas com dados pessoais ou credenciais.

A varredura funcional também planeja onde os prints ajudam a explicar telas, campos e decisões. Quando faltar uma captura necessária, a skill deixa um aviso padronizado no ponto correspondente, com o caminho no sistema e o contexto de coleta. Você ou o desenvolvedor obtém os prints manualmente depois. Na verificação sem escrita, essas posições são apenas reportadas.

### Preparar o adaptador do manual

Use quando quiser preparar a investigação sem gerar o manual ainda.

```text
Use a skill `manual-creator-scan-codebase` para criar ou atualizar somente o adaptador de <sistema ou módulo> neste repositório.

Público e tarefas: <o que já souber sobre quem usa e o que precisa fazer>.
Versão, idioma e configuração: <se souber>.
Local de leitura e renderizador Markdown: <se souber>.
Logo e materiais complementares: <arquivos locais, se houver>.

Confira no código as convenções informadas, inclusive como rastrear caminhos visíveis, telas, estados e personas para orientar a coleta manual de prints. Entreviste-me sobre as lacunas relevantes e registre o adaptador completo. Não gere o manual nem insira avisos nele nesta etapa.
```

### Criar um manual de uso

```text
Use a skill `manual-creator-scan-codebase` para criar o manual de uso de <sistema ou módulo> neste repositório.

Público: <grupos de usuários e seus objetivos>.
Tarefas no alcance: <tarefas ou funcionalidades>.
Versão e idioma da interface: <se souber>.
Local de leitura e renderizador Markdown: <onde o manual será lido>.
Logo: <caminho do arquivo ou indicação da logo existente no projeto>.
Materiais complementares: <documentos ou capturas locais, se houver>.
Ambiente para conferência: <fonte e alcance autorizados, se houver>.

Prepare primeiro o adaptador e só depois faça a varredura funcional completa do alcance e redija o manual a partir das regras e dos textos comprovados. Articule o texto com as capturas disponíveis; onde faltar um print necessário, insira o aviso padronizado junto à explicação pertinente, com o caminho comprovado no sistema e o contexto para coleta manual. Ao final, apresente as lacunas, os prints pendentes e diferencie a conferência no código da observação na interface.
```

### Atualizar um manual de uso

```text
Use a skill `manual-creator-scan-codebase` para atualizar o manual em <docs/manuais/nome-do-manual.md> conforme a codebase atual.

Mudança a documentar: <funcionalidades, versão ou commits, se souber>.
Público ou configuração que mudou: <se houver>.
Novas capturas ou materiais: <arquivos locais, se houver>.

Revalide o adaptador antes de escrever e altere somente o conteúdo afetado por mudanças comprovadas. Reavalie no alcance as telas, caminhos e posições didáticas dos prints: confira novas capturas antes de substituir os avisos correspondentes e sinalize prints necessários ainda ausentes pelo padrão da skill. Preserve as seções ainda corretas, os nomes de imagens e as âncoras válidas; relate necessidades fora do alcance sem editá-las. Informe limitações do verificador em Markdown legado e pendências funcionais ou visuais.
```

### Verificar um manual sem escrita

```text
Use a skill `manual-creator-scan-codebase` para verificar o manual em <docs/manuais/nome-do-manual.md> contra a codebase atual e as convenções da skill.

Confira cobertura de tarefas e personas, campos, regras, mensagens, imagens e navegação. Confronte as telas encontradas no código com as posições dos prints no manual, os avisos de captura pendente e a fidelidade dos caminhos no sistema. Para cada print necessário ausente, reporte a seção, o ponto de inserção, o aviso sugerido e o contexto para coleta manual. Não altere nenhum arquivo, inclusive manual, imagens, adaptador e registro. Reporte os critérios verificados, as evidências e o que não puder confirmar.
```

---

## gauntlet-loop-forge

A skill `gauntlet-loop-forge` monta um prompt com a técnica de loop de verificação a partir do que você tiver: uma ideia, uma especificação ou um prompt que já existe. Ela só escreve o prompt e para: executar é um pedido separado, em uma janela nova.

Para agregar a técnica, acrescente esta linha ao início ou ao fim de qualquer prompt deste arquivo, antes de enviar:

```text
Use a skill `gauntlet-loop-forge` para acrescentar a técnica de loop ao prompt <acima/abaixo>.
```

Antes de acionar o loop, confirme que a tarefa é complexa ou que um erro nela é difícil de reverter. Em tarefa pequena e reversível, o loop custa mais do que resolve.

Onde o loop compensa:

| Demanda | Quando o loop compensa |
|---|---|
| Correção de bug | A correção muda comportamento em fluxo crítico, mexe em transação ou migra dado, e precisa preservar o que já funciona. |
| Pedido inicial e entregáveis do Speckit | O documento de uma fase é insumo de todas as fases seguintes, e o `/speckit-analyze` só roda depois do `/speckit-tasks`. |
| Revisão técnica e de segurança | O código vai para produção, trata dado pessoal ou já causou incidente. |

**Modelo para executar o prompt com loop:** prefira modelos intermediários e mais baratos. Exemplos em 2026: Luna e Terra (GPT), Haiku e Sonnet (Claude). Eles tendem a gastar menos tokens e, com o loop e os critérios bem definidos no prompt, entregam bom resultado. Modelos de topo, como Opus e Fable (Claude) ou Sol e Astra (GPT), tendem a alongar o loop, porque o mecanismo de execução do próprio modelo já repete e reverifica passos por conta própria, e o gasto de tokens cresce muito.

### Criar o prompt a partir de uma ideia

Use quando o ponto de partida é um objetivo na sua cabeça, sem prompt e sem documento nenhum.

**Prompt:**

```text
Use a skill `gauntlet-loop-forge` para transformar o objetivo abaixo em um prompt com loop de verificação, pronto para colar.

Objetivo: <o que precisa existir no final, em uma ou duas frases>
Onde o prompt vai rodar: <Claude Code, Codex, outro agente, ou chat comum>
Padrão de qualidade que eu já tenho: <se souber, ex.: "a suíte de testes atual precisa continuar passando", "quero no nível do relatório de pedidos que já existe">
Material que serve de fonte da verdade: <se houver: arquivos, issue, especificação, repositório>
O que não pode mudar: <se houver: comportamento, formato, compatibilidade>
O que os agentes podem fazer no ambiente: <ler, rodar teste, editar arquivo, acessar rede, publicar, gastar>
Ações que exigem minha aprovação: <se houver>
```

### Criar o prompt a partir de uma especificação

Use quando já existe um documento, uma issue ou um repositório que manda no resultado.

**Pré-requisito:** o arquivo, a issue ou o repositório acessível ao agente dentro da sessão.

**Prompt:**

```text
Use a skill `gauntlet-loop-forge` para transformar <arquivo, issue ou especificação> em um prompt com loop de verificação, pronto para colar.

Trate <arquivo, issue ou especificação> como fonte da verdade: extraia dali os critérios de aceite, as restrições e o que está fora de escopo antes de me perguntar qualquer coisa. Me avise se encontrar contradição em vez de escolher um lado sozinho.

Me pergunte só o que não estiver no material. Não prescreva arquitetura, divisão de tarefas nem ordem de implementação: isso é decisão do agente líder na hora de executar.
```

### Otimizar um prompt que já existe

Use quando o prompt já tem bloco de loop e você quer saber onde ele falha. A skill troca só o bloco de loop e preserva o seu texto e as restrições que você já escreveu.

**Prompt:**

```text
Use a skill `gauntlet-loop-forge` para diagnosticar e reescrever o bloco de loop do prompt abaixo.

<cole aqui o prompt atual, com o bloco de loop>

Aponte onde ele deixa quem constrói aprovar o próprio trabalho, onde o padrão de qualidade não é conferível, onde a repetição não tem limite finito e onde ele manda usar comando ou flag que o meu ambiente não tem. Me diga o que mudou e por quê.
```

### Executar o prompt criado

Use em uma janela nova, colando o prompt que a skill devolveu. As linhas depois do prompt servem para você conferir logo no começo que os limites e o registro de evidências ficaram claros.

**Pré-requisito:** uma ferramenta de IA que consiga abrir agentes auxiliares em conversa separada. Quem constrói e quem confere são agentes diferentes, e quem confere trabalha em conversa nova, sem ter acompanhado a construção. Sem essa segunda conversa, o mesmo agente faz os dois papéis e acaba aprovando o próprio trabalho. O prompt ainda roda assim, com resultado mais fraco, e o bloco de loop manda o agente avisar você de que a separação não foi real.

**Prompt:**

```text
<cole aqui o prompt criado>

Antes de começar, confirme em uma linha: quantas rodadas de melhoria e conferência você tem por frente de trabalho, quantos agentes vai abrir ao mesmo tempo e onde vai manter o registro de evidências.

Se algum limite for atingido antes da aprovação, pare e me devolva o estado CAPPED com os achados em aberto e a próxima ação recomendada. Atingir o limite nunca é aprovação, e nenhum limite é ampliado sem eu autorizar.
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

---

## recapitulacao-resumo-ata-relato-reuniao

Transforma o conteúdo de uma reunião em dois blocos: a recapitulação, por tema, e a lista de ações, com o responsável de cada uma. Usa só o que está na fonte: nenhuma decisão, prazo, participante ou responsável é inventado, e ação sem responsável claro fica de fora.

Aceita transcrição colada, anotações, gravação legível e a URL de "Assistir no Navegador" do Microsoft Teams. A URL serve só para obter o conteúdo e não aparece no resultado. A resposta é só o registro, sem introdução nem comentário. Se a fonte não estiver acessível, a skill avisa e pede a transcrição em vez de registrar com lacunas.

### Registrar uma reunião a partir da transcrição

**Prompt:**

```text
Use a skill `recapitulacao-resumo-ata-relato-reuniao` para registrar a reunião abaixo.

Data da reunião: <dd/mm/aaaa, se a transcrição não trouxer>

<cole aqui a transcrição ou as anotações>
```

### Registrar uma reunião a partir da gravação no Teams

**Pré-requisito:** a gravação acessível ao agente dentro da sessão.

**Prompt:**

```text
Use a skill `recapitulacao-resumo-ata-relato-reuniao` para registrar a reunião gravada em <URL de "Assistir no Navegador" do Microsoft Teams>.
```

---

## escrita-em-linguagem-simples-pt-br

Reescreve um texto em Linguagem Simples, em português do Brasil, para o público que você informar ou para o cidadão, quando você não informar. Preserva fatos, condições, datas, valores, prazos, responsáveis e trechos entre aspas; não acrescenta interpretação nem informação de fora. Aceita texto colado, arquivo, anexo e URL de página, inclusive várias URLs, e devolve só o texto reescrito.

### Reescrever um texto colado

**Prompt:**

```text
Use a skill `escrita-em-linguagem-simples-pt-br` para reescrever o texto abaixo.

Público-alvo: <se não for o cidadão, ex.: "servidores da área de contratos">

<cole aqui o texto>
```

### Reescrever um arquivo ou uma página

Para várias páginas, liste as URLs na ordem em que quer os textos: a skill reescreve cada uma sob o próprio título.

**Prompt:**

```text
Use a skill `escrita-em-linguagem-simples-pt-br` para reescrever <caminho do arquivo, anexo ou URL da página>.

Público-alvo: <se não for o cidadão>
```

---

## conformidade-de-escrita-normativa

Versão em arquivo único da avaliação de conformidade: as dezessete dimensões e as regras de redação ficam dentro do próprio `SKILL.md`, para ambiente que carrega a skill em um arquivo só, como o Copilot Studio. Qualquer pedido, mesmo com os verbos corrigir ou reescrever, é tratado como análise e devolve só o relatório; o texto ajustado aparece apenas na seção de transcrição dos ajustes, dispositivo por dispositivo.

### Analisar a minuta inteira

**Prompt:**

```text
Use a skill `conformidade-de-escrita-normativa` para analisar a conformidade da redação da minuta abaixo.

<cole aqui a minuta, ou informe o caminho do arquivo>
```

### Analisar só alguns dispositivos

**Prompt:**

```text
Use a skill `conformidade-de-escrita-normativa` para analisar a conformidade da redação dos dispositivos abaixo, sem presumir o restante da minuta.

<cole aqui o texto dos dispositivos, ex.: o texto do art. 3º ao art. 7º>
```
