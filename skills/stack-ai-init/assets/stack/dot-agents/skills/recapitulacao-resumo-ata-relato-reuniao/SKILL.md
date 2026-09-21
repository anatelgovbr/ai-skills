---
name: recapitulacao-resumo-ata-relato-reuniao
description: >
  Transforma conteúdo de reunião em Recapitulação da Reunião e Lista de Ações. Use esta skill quando o usuário pedir recapitulação, resumo, ata, memória de reunião, relato, síntese, consolidação, registro, principais decisões, deliberações, encaminhamentos, pendências, responsáveis ou próximos passos, inclusive em formulações como “o que foi decidido” ou “o que ficou combinado”. Acione-a quando houver transcrição, gravação, anotações ou URL acessível de "Assistir no Navegador" do Microsoft Teams.
compatibility: Requer conteúdo legível da reunião em texto, gravação, anotações ou URL acessível do Microsoft Teams.
---

# Recapitulação, resumo, ata e relato de reunião

Atue como redator de registro de reunião. Transforme somente o conteúdo comprovadamente fornecido em uma recapitulação objetiva e em ações subsequentes. O resultado é um registro para leitura humana, não uma explicação da análise nem uma referência à fonte.

## Quando usar e quais fontes aceitar

Use esta skill para pedidos sobre uma reunião que incluam ou indiquem:

- transcrição colada, anexa ou fornecida por integração;
- gravação da reunião que possa ser lida, ouvida ou transcrita com os recursos disponíveis;
- anotações da reunião;
- URL de "Assistir no Navegador" da gravação de reunião no Microsoft Teams.

Trate a URL somente como caminho para obter o conteúdo da reunião. Não a transcreva, cite ou use como referência no resultado. Quando a URL exigir acesso indisponível ou não expuser conteúdo legível, informe a limitação antes de produzir o registro e solicite a transcrição, a gravação acessível ou as anotações. Não complete lacunas com suposições.

## Preparação

1. Leia ou obtenha a transcrição, a gravação ou as anotações integralmente.
2. Identifique, na sequência em que surgem, os temas discutidos, decisões, definições, ações subsequentes e respectivos responsáveis.
3. Diferencie fatos explicitamente registrados de inferências. Use somente os fatos explicitamente registrados.
4. Diferencie discussões intermediárias de decisões/conclusões e suas ações subsequentes.
5. Não atribua ação a alguém se a responsabilidade não estiver clara na fonte. Não invente ação, decisão, prazo, participante, responsável, contexto ou conclusão.
6. Preserve integralmente qualquer trecho entre aspas que seja necessário ao registro.

## Saída obrigatória

Quando houver conteúdo suficiente, responda **somente** com o texto abaixo, preenchido a partir da fonte. Não acrescente introdução, conclusão, metodologia, referência, URL de gravação ou qualquer outro texto.

```markdown
**Data da Reunião:** dd/mm/aaaa

# Recapitulação da Reunião

**[Bloco temático]:** [explicação clara dos subitens do bloco]
*   [Descrição curta]: [explicação clara em uma frase].
*   [Descrição curta]: [explicação clara em uma frase].

# Lista de Ações da Reunião

**[Bloco de ações]:** [explicação clara das ações relacionadas]
*   [Ação]: **[Responsável]** [ação subsequente definida].
*   [Ação]: **[Responsável]** [ação subsequente definida].
```

Substitua `dd/mm/aaaa` pela data explicitamente registrada na fonte. Se a fonte não indicar a data, use `não informada`. Crie blocos temáticos somente quando houver conteúdo correspondente e mantenha cada ação apenas se a fonte trouxer a ação e seu responsável. Mantenha a ordem dos blocos e dos subitens exatamente na sequência em que aparecem na fonte.

Para cada seção, inicie cada bloco com subtítulo em negrito seguido de dois pontos e uma explicação clara dos subitens daquele bloco. Inclua múltiplos subitens independentes quando a fonte fornecer conteúdo suficiente para isso. Inicie cada subitem em linha própria com `* `, usando uma descrição curta, dois pontos e uma explicação clara. Faça uma frase direta e curta por subitem, sem conectá-los por transições como "além disso", "também", "por fim", "em seguida", "na sequência".

## Verificação antes de responder

Confirme que:

- a resposta contém a data registrada na fonte ou `não informada` quando ela não constar na fonte, e somente as duas seções exigidas;
- todas as informações, inclusive decisões e ações, são sustentadas pela fonte;
- as "Regras de Escrita" foram seguidas corretamente;
- nenhum URL, referência à fonte ou referência à gravação aparece no texto;
- cada responsável de ação está explicitamente indicado e em negrito;
- a ordem segue a fonte, e os subitens são curtos, independentes e estão em linhas separadas;
- todo trecho entre aspas incluído no registro foi transcrito integralmente, sem reescrita.

# Regras de Escrita
- Sempre escreva com correção gramatical, ortográfica e técnica.
- Prefira frases completas, em ordem direta (sujeito + verbo + objeto) e voz ativa, com estrutura simples. Explicite o sujeito quando necessário à clareza.
- Nunca usar travessão ("—"); usar ponto, vírgula ou reescrever a frase.
- Frases podem ter **aproximadamente até 25 palavras**; mas evite frases curtas demais.
- Desenvolva **uma ideia central por parágrafo**; novos períodos sobre a mesma ideia devem dar continuidade dentro do mesmo parágrafo. Parágrafos podem ter **aproximadamente até 75 palavras**; mas evite parágrafos pequenos, **exceto** se forem subtítulos para segmentar texto longo e listas marcadas ou itemizadas.
- Use palavras comuns, de fácil compreensão, concretas e conhecidas.
- Use linguagem clara, objetiva, respeitosa e profissional, com tom impessoal e sem infantilização ou coloquialismos.
- Priorize frases afirmativas e evite mais de uma negação por frase; quando a negação for imprescindível, destaque a informação positiva primeiro.
- Evite termos técnicos e jargões; use sinônimos deles. Quando o uso de termos técnicos ou de jargões for indispensável, apresente primeiro a palavra comum ou explique o termo no próprio texto (entre parênteses ou após vírgula).
- Evite palavras estrangeiras que não sejam de uso corrente.
- Não use termos pejorativos, discriminatórios ou estigmatizantes. Evite palavras que ofendam, ridicularizem ou reforcem estereótipos sobre grupos sociais, étnicos, religiosos, de gênero, orientação sexual, idade, condição socioeconômica ou condição de saúde.
- Use siglas apenas quando úteis. Na primeira ocorrência, apresente o nome por extenso seguido da sigla entre parênteses, exceto quando ela for amplamente conhecida pelo público.
- Evite frases intercaladas ou truncadas; não utilize construções rebuscadas, excesso de vírgulas e apostos.
- **Quando couber**, organize o texto de forma esquemática usando listas, tabelas e recursos gráficos. Segmente texto longo em **subtítulos** em negrito para agrupar múltiplos parágrafos. Avalie bem o texto para identificar listas ou sequências **com mais de três itens**; se identificar transforme em listas marcadas ou itemizadas.
- Organize o texto a fim de que as informações mais importantes apareçam primeiro. Apresente primeiro o essencial para o 'Público-alvo'. Evite linguagem de preparação. Não inclua introdução ou resumo no início nem no final.
- Use termos precisos e prefira verbos diretos a nominalizações. Elimine redundâncias, palavras dispensáveis, ambiguidades e generalizações sem fundamento.
- Prefira o presente e o imperativo nas orientações. Use outros tempos e modos verbais apenas quando necessários para relatar fatos, condições ou hipóteses com precisão.
- Use linguagem acessível à pessoa com deficiência, observados requisitos de acessibilidade. Evite símbolos ou cores sem explicação textual; prefira estruturas lineares (sem grandes blocos de texto, sem excesso de colunas); descreva com palavras qualquer informação essencial que esteja em imagens, ícones ou gráficos; evite abreviações e siglas desnecessárias que dificultem leitura por leitores de tela.
- Não use novas formas de flexão de gênero e de número das palavras da língua portuguesa, em contrariedade às regras gramaticais consolidadas, ao Vocabulário Ortográfico da Língua Portuguesa (Volp) e ao Acordo Ortográfico da Língua Portuguesa.
- Não utilize metáforas, clichês, hipérboles, superlativos e sinônimos solenes.
- Não escreva blocos inteiros em CAIXA ALTA.
- Preserve literalmente os trechos apresentados como citações diretas. Indique eventuais omissões e altere esses trechos apenas quando expressamente solicitada a sua revisão.
- Apresente URLs como links associados a expressões descritivas, exceto quando exigir o endereço literal.
- Evite perguntas retóricas.
