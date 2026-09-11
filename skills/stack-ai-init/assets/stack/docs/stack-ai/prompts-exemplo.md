# Prompts de exemplo

## Sumário

- [Introdução](#introdução)
- [Como escrever um bom prompt](#como-escrever-um-bom-prompt)
- [Fluxo SpecKit para funcionalidade nova](#fluxo-speckit-para-funcionalidade-nova)
  - [Fluxo padrão](#fluxo-padrão)
  - [Fluxo alternativo, com passos opcionais](#fluxo-alternativo-com-passos-opcionais)
- [Dicionário de dados](#dicionário-de-dados)
  - [Criar o adaptador](#criar-o-adaptador)
  - [Criar o dicionário de dados](#criar-o-dicionário-de-dados)
  - [Atualizar o dicionário](#atualizar-o-dicionário)
  - [Revisar a qualidade do dicionário](#revisar-a-qualidade-do-dicionário)
- [Modos auxiliares](#modos-auxiliares)
  - [Stress-test de um plano utilizando o grill-me](#stress-test-de-um-plano-utilizando-o-grill-me)
  - [Comprimir a resposta utilizando o caveman](#comprimir-a-resposta-utilizando-o-caveman)
  - [Solução mínima utilizando o ponytail](#solução-mínima-utilizando-o-ponytail)
  - [Revisar over-engineering utilizando o ponytail-review e o ponytail-audit](#revisar-over-engineering-utilizando-o-ponytail-review-e-o-ponytail-audit)
  - [Rastrear as simplificações utilizando o ponytail-debt](#rastrear-as-simplificações-utilizando-o-ponytail-debt)
  - [Consultar comandos e impacto utilizando o ponytail-help e o ponytail-gain](#consultar-comandos-e-impacto-utilizando-o-ponytail-help-e-o-ponytail-gain)

---

## Introdução

Este arquivo reúne prompts prontos para as skills que a stack instala. Eles são templates para adaptar ao seu caso e enviar, não ilustrações.

O projeto pode ter um segundo arquivo de prompts, com templates específicos do sistema dele. Os dois se complementam: aqui estão os prompts que valem em qualquer projeto.

---

## Como escrever um bom prompt

O `AGENTS.md` é carregado em toda sessão e concentra as orientações do projeto. Os prompts abaixo não repetem o que já está lá. Repita uma orientação do `AGENTS.md` dentro de um prompt só quando quiser reforçar um ponto muito crítico, para reduzir o risco de o agente errar justo nesse ponto.

**Parâmetros.** Todo trecho entre `<` e `>` é um parâmetro: substitua pela informação real antes de enviar. Campo marcado como `<se souber>` ou `<opcional>` que você não tiver como preencher: apague a linha inteira. Nunca deixe o texto entre `<` e `>` dentro do prompt enviado, e não escreva "não sei" no lugar do campo. Se você não sabe, a linha não deveria estar lá.

**Adapte à vontade.** Nenhum prompt precisa ser enviado igual ao template. Linha que não se aplica ao seu caso, apague; mande só o que você realmente tem. Quanto mais informação e validação você der junto do prompt, mais assertivo o agente tende a ser, mas isso não é obrigatório: um prompt mais enxuto também funciona.

**Nunca cole segredo.** Antes de colar mensagem de erro, print de tela ou qualquer evidência bruta, remova, se forem de ambiente de produção:

- senha ou qualquer outra credencial
- dado pessoal (CPF, nome completo, e-mail, endereço)
- segredo (token, chave de API, string de conexão)

Troque cada um desses valores por um texto genérico, mantendo claro o que está errado. Em ambiente de teste ou desenvolvimento, pode colar sem trocar nada.

**Regra de negócio não documentada.** Se a regra não estiver escrita em lugar nenhum do repositório, escreva a regra no próprio prompt.

**A sessão continua.** Todo prompt daqui é o ponto de partida da sessão, não uma interação única. Depois do resultado, continue na mesma janela para ajustar, aprofundar ou corrigir. Se quiser guardar o conteúdo da sessão (achados, relatório, decisão), peça ao agente para salvar em um `.md` dentro de `specs/`, que é local e não versionada.

---

## Fluxo SpecKit para funcionalidade nova

Use o fluxo SpecKit sempre que a demanda criar algo que ainda não existe. Para uma mudança pontual em algo que já existe, converse direto com o agente.

Quanto mais detalhado o pedido em `/speckit-specify`, melhor a especificação gerada. Descreva contexto, comportamento esperado e critério de aceite em linguagem de negócio; deixe stack técnica, classe e padrão de implementação para o `/speckit-plan`, que é a fase certa para essa decisão.

O exemplo abaixo usa como demanda "adicionar um filtro de período (data inicial e data final) em uma listagem"; troque pelo objetivo real antes de enviar.

### Fluxo padrão

Especificar, planejar, decompor em tarefas e implementar, nessa ordem.

**1. Especificar:**

```text
/speckit-specify

Quero <descreva a funcionalidade nova em uma frase, ex.: "adicionar um filtro de período (data inicial e data final) na listagem"> em <sistema, módulo ou área>.

Contexto:
- quem usa: <perfil, papel ou permissão>
- comportamento esperado: <resultado esperado, ex.: "a listagem mostra somente os registros criados dentro do período informado">
- fora de escopo: <o que essa funcionalidade não faz>

Critério de aceite inicial:
1. Sucesso: <entrada concreta e resultado esperado>
2. Validação: <condição limite e comportamento esperado>

Fatos verificados:
- regra de negócio confirmada: <se houver>
- tela ou fluxo semelhante que serve de referência: <se houver, ex.: "o filtro de período da tela X já faz isso, usar de referência">

Hipóteses não confirmadas: trate como pista, confirme no código e me avise se refutar.
- impacto suposto: <se souber, ex.: "não deve exigir permissão nova, é só um filtro a mais na tela existente">

Justifique sua resposta.
```

**2. Planejar:**

```text
/speckit-plan

Reaproveite tela, componente ou padrão semelhante já existente antes de propor algo novo.

No plano, declare explicitamente os impactos em <as dimensões sensíveis do seu projeto, ex.: "estrutura de banco, permissões e scripts de instalação">. Se algum desses impactos existir, marque-o como ponto de parada para minha decisão antes da implementação.

Justifique sua resposta.
```

**3. Decompor em tarefas:** a decomposição usa a spec e o plano já aprovados nas fases anteriores; não precisa de argumento adicional.

```text
/speckit-tasks
```

**4. Implementar:** executa as tarefas geradas; não precisa de argumento adicional.

```text
/speckit-implement
```

### Fluxo alternativo, com passos opcionais

Mesmo fluxo, com três passos opcionais inseridos: clarificar dúvidas antes de planejar, gerar um checklist de requisitos sensíveis antes de decompor, e analisar consistência antes de implementar.

**1. Especificar:** igual ao fluxo padrão.

**2. Clarificar:** use quando a spec tiver ambiguidade. A skill faz até 5 perguntas objetivas e grava as respostas na própria spec. Não precisa de argumento adicional.

```text
/speckit-clarify
```

**3. Planejar:** igual ao fluxo padrão.

**4. Gerar checklist:** use quando o domínio for sensível e você quiser validar a qualidade dos requisitos antes de decompor em tarefas.

```text
/speckit-checklist

Gere um checklist para validar os requisitos de <dimensão sensível, ex.: permissão e auditoria> de <funcionalidade> antes de implementar.

Justifique sua resposta.
```

**5. Decompor em tarefas:** igual ao fluxo padrão.

**6. Analisar:** checa a consistência entre spec, plano e tarefas antes de implementar. Não precisa de argumento adicional.

```text
/speckit-analyze
```

**7. Implementar:** igual ao fluxo padrão.

---

## Dicionário de dados

A skill `dicionario-dados-db-scan-codebase-docs` investiga a codebase, os scripts de banco e qualquer documentação disponível para gerar e manter dicionários de dados. O alvo pode ser o sistema inteiro, um módulo, uma base corporativa ou um DW.

Todo alvo reconhecido precisa de um **adaptador** registrado. Adaptador é o arquivo que ensina a skill a localizar, investigar e versionar aquele alvo: onde fica a fonte estrutural, qual fonte tem precedência quando houver mais de uma, como a versão é identificada e onde buscar no código. Sem adaptador registrado, a skill recusa gerar o dicionário e aponta a lacuna.

A skill gera três artefatos: `dicionario_tabelas.md` e `dicionario_colunas.md`, com as descrições semânticas, e `CHANGELOG.md`, com o changelog estrutural.

### Criar o adaptador

Use no primeiro contato com um alvo que a skill ainda não reconhece. Este prompt cria só o adaptador. Gere o dicionário depois, em um pedido separado. Informe as convenções que você já souber, para reduzir as perguntas que a skill vai precisar fazer. O que você não souber, ela tenta inferir da codebase antes de perguntar.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o adaptador de <sistema ou módulo>. Investigue a codebase, crie o adaptador completo e registre-o. Não gere o dicionário de dados nem o changelog nesta etapa.

O que eu já sei sobre ele:
- pistas que identificam este alvo (nome, caminhos, prefixo de tabela, pasta de documentação, ou o próprio repositório, se for o sistema inteiro): <se souber, ex.: "prefixo pedidos_, models em app/Models/Pedido.php, migrations em database/migrations/">
- fonte estrutural e convenção de versionamento: <scripts de instalação, migrations, schema ou DDL, se souber>
- precedência entre fontes, se houver mais de uma fonte estrutural para a mesma informação: <qual prevalece, se souber, ex.: "migration mais recente prevalece sobre o schema.sql legado">
- codificação, camadas e onde buscar no código: <se souber, ex.: "camadas Entity/Repository/Controller">
- títulos e pasta de destino dos dicionários: <se souber, ex.: "docs/dicionario_dados/abc/">
- particularidades ou exceções conhecidas: <se houver>

Trate os itens acima como pista, não como conclusão: confirme cada um contra a codebase e me avise se algum divergir.

Pergunte objetivamente só sobre o que não puder ser inferido nem foi informado acima. Justifique sua resposta.
```

### Criar o dicionário de dados

Use na primeira vez que for gerar o dicionário de um alvo que já tenha adaptador. Anexar material complementar aumenta o contexto disponível e tende a melhorar o resultado: pode ser esquema de banco em outra ferramenta, dicionário anterior, prints de tela, manuais, vídeos ou transcrições. A skill sempre confirma tudo contra as fontes estruturais antes de publicar qualquer descrição.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o dicionário de dados e o changelog estrutural de <sistema ou módulo>.

Investigue as fontes estruturais disponíveis (codebase, scripts de instalação, migrations, schemas ou DDLs) para identificar a convenção de versionamento e, quando houver codebase, onde ficam as regras de negócio. Aproveite também qualquer documentação já existente. Não publique como fato uma descrição cuja semântica não esteja suficientemente sustentada pelas evidências encontradas.

Considere como material complementar <se houver: arquivos anexados, esquema em outro formato, dicionário anterior, prints, manuais, vídeos, transcrições>. Dê atenção especial a <o material mais relevante, se houver mais de um>, mas confirme tudo contra a fonte estrutural disponível antes de publicar qualquer descrição.

Ao final, informe explicitamente: as tabelas ou colunas cuja semântica você não conseguiu confirmar, o que faltou para confirmá-las, e onde algum material complementar divergiu da fonte estrutural e qual fonte você adotou. Justifique sua resposta.
```

### Atualizar o dicionário

Use quando o dicionário já existir e você quiser sincronizá-lo com mudanças estruturais (novas tabelas, colunas ou regras de negócio) ou após uma nova versão. Também serve para corrigir uma descrição anterior, mas só diante de divergência estrutural confirmada ou domínio incompleto confirmado, nunca por ajuste de estilo.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para atualizar o dicionário de dados de <sistema ou módulo> para o estado mais recente da <codebase ou base>.

Compare o dicionário de dados e o changelog já existentes com a estrutura e as regras de negócio atuais e altere somente o que realmente mudou desde a última atualização, preservando sem alteração o restante.

Se você souber a versão-alvo, os commits ou as migrations específicas da mudança, indique-os. Caso contrário, identifique o escopo da diferença pela própria codebase.

Considere como material complementar <se houver: arquivos anexados, esquema em outro formato, dicionário anterior, prints, manuais, vídeos, transcrições>. Confirme tudo contra a fonte estrutural disponível antes de publicar qualquer descrição.

Ao final, liste o que foi alterado e o que foi preservado intencionalmente. Justifique sua resposta.
```

### Revisar a qualidade do dicionário

Use quando quiser avaliar se um dicionário já existente segue os critérios de qualidade e as convenções da própria skill (completude, consistência, terminologia, distinções documentadas), sem alterar nenhum arquivo e independente de a codebase ter mudado.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para revisar a qualidade e a consistência do dicionário de dados de <sistema ou módulo>, sem alterar nenhum arquivo.

Classifique cada achado como problema de qualidade documental (descrição incompleta, inconsistente, genérica ou fora das convenções da skill) ou como lacuna (elemento sem descrição). Liste claramente qualquer lacuna que impeça considerar a documentação completa. Justifique sua resposta.
```

---

## Modos auxiliares

Esta seção é diferente das anteriores. As skills aqui não resolvem uma demanda: elas mudam o jeito de o agente trabalhar em cima de qualquer prompt. O `caveman` muda como o agente escreve, o `ponytail` muda o que o agente constrói, e o `grill-me` muda como o agente te entrevista.

Todas são opcionais e nenhuma liga sozinha. O agente nunca aciona esses modos por conta própria: eles só entram se você invocar.

Nenhum desses modos afrouxa o `AGENTS.md`. Se a instrução do modo colidir com uma regra do `AGENTS.md`, vale o `AGENTS.md`.

Envie o comando sozinho, em uma mensagem separada, antes do prompt real. O `caveman` e o `ponytail` continuam ativos nas respostas seguintes até você desligar ou até a sessão acabar. As outras skills desta seção valem só para a resposta que elas geram.

### Stress-test de um plano utilizando o grill-me

Use antes de aprovar um plano, tipicamente entre `/speckit-specify` e `/speckit-plan`. Comece em uma janela nova.

A entrevista é uma pergunta por vez, cada uma com a resposta que o agente recomenda. Quando a pergunta puder ser respondida lendo o código, o agente lê o código em vez de perguntar. Nada é gravado em arquivo: se quiser guardar o que ficou decidido, peça no fim da entrevista.

Não peça a entrevista nem peça uma pergunta por vez, porque a skill já faz as duas coisas. Diga só três coisas: o que vai ser interrogado, a decisão que ainda está em aberto e o que mais te preocupa.

Responder "tanto faz" ou concordar com tudo esvazia a entrevista: são as suas objeções que fazem o agente mudar de direção.

**Prompt:**

```text
/grill-me

<o plano, a spec ou a decisão a ser interrogada, ex.: "o plano gerado pelo /speckit-plan para o filtro de período da listagem de pedidos">

Ainda em aberto: <a decisão que você não tomou, ex.: "se o filtro entra na página de pesquisa que já existe ou em uma página nova">

Me preocupa: <o que mais te preocupa, ex.: "impacto em permissão, impacto no processo de release e o que acontece com os registros já existentes">
```

### Comprimir a resposta utilizando o caveman

Use quando a sessão vai gerar texto longo, como a revisão de um diretório inteiro, e você quer o conteúdo sem a prosa em volta.

O `caveman` corta artigo, hedging e frase de cortesia. Ele não corta conteúdo técnico: termo técnico, trecho de código, nome de classe ou de API e mensagem de erro saem literais, iguais ao modo normal. Código, mensagem de commit e descrição de PR também continuam em texto normal.

São três níveis. O `lite` mantém frase completa e tira só o excesso. O `full` é o padrão e usa frase fragmentada. O `ultra` abrevia palavra de prosa (BD, config, req) e nunca abrevia nome de função, símbolo de código ou string de erro.

Na sequência, na mesma janela, envie o prompt real. Para voltar ao normal, envie `stop caveman`.

**Prompt:**

```text
/caveman full
```

### Solução mínima utilizando o ponytail

Use em ajuste pontual, ou quando as respostas anteriores vieram com abstração demais: interface com uma implementação só, camada com um único chamador, configuração que ninguém muda.

O `ponytail` percorre uma escada e para no primeiro degrau que resolve: a coisa precisa existir, já existe algo no código para reusar, dá para usar recurso nativo, cabe em uma linha, e só então código novo.

Na sequência, envie o prompt real e acrescente a ele a linha do segundo bloco abaixo, para o modo não tentar simplificar os controles obrigatórios do seu projeto.

Para voltar ao normal, envie `stop ponytail`.

**Ligar o modo:**

```text
/ponytail
```

**Linha para acrescentar ao prompt real:**

```text
Fora de escopo simplificar: <liste aqui os controles obrigatórios do seu AGENTS.md, ex.: "validação de permissão, controle transacional e registro de auditoria">. Esses controles são guardrail do AGENTS.md, não código extra.
```

### Revisar over-engineering utilizando o ponytail-review e o ponytail-audit

Use quando quiser saber o que dá para cortar do código, sem entrar no mérito de correção ou segurança.

Esta revisão olha só complexidade desnecessária. Ela não avalia correção, segurança, permissão, transação nem modelagem de banco, e por isso nunca substitui uma revisão técnica de verdade. Use as duas coisas: a revisão técnica responde se está correto, esta revisão responde se está inchado.

**Revisar o diff da branch:**

```text
/ponytail-review

Revise as mudanças da branch atual em <diretório ou arquivo>, comparadas com <branch base>.

Trate como fora de escopo, e não como achado: <as dimensões que pertencem à revisão técnica do seu projeto, ex.: "permissão, transação, auditoria e validação de entrada">.

Não altere nenhum arquivo. Cite arquivo e linha em cada achado.
```

**Revisar um diretório inteiro:**

```text
/ponytail-audit

Varra <diretório> inteiro e liste o que dá para cortar, do maior corte para o menor.

Trate como fora de escopo, e não como achado: <as dimensões que pertencem à revisão técnica do seu projeto>.

Não altere nenhum arquivo. Cite arquivo e linha em cada achado.
```

### Rastrear as simplificações utilizando o ponytail-debt

O `ponytail` marca cada simplificação deliberada com um comentário `// ponytail: <teto>, <gatilho de upgrade>`. Esse marcador registra o limite conhecido da simplificação e a condição para revisitá-la.

Atenção: somente a skill `ponytail-debt` enxerga o marcador `ponytail:`. Ferramentas de revisão e relatórios de pendência costumam procurar `TODO:`. Se a simplificação precisa aparecer nesses relatórios, marque também com `TODO:` na mesma linha do código.

**Prompt:**

```text
/ponytail-debt

Colete os comentários `ponytail:` de <diretório> em um ledger.

Para cada marcador, informe arquivo, linha, o que foi simplificado, o teto declarado e o gatilho de upgrade. Sinalize separadamente os marcadores que estiverem sem gatilho de upgrade.

Não altere nenhum arquivo.
```

### Consultar comandos e impacto utilizando o ponytail-help e o ponytail-gain

Envie `/ponytail-help` para ver o cartão de referência com todos os modos, níveis e comandos da família `ponytail`.

Envie `/ponytail-gain` para ver o scoreboard de benchmark da skill. Os números são medianas publicadas pelos autores do `ponytail`, medidas por eles em outras tarefas: não são uma medição do seu projeto.
