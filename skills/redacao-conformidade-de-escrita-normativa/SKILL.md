---
name: redacao-conformidade-de-escrita-normativa
description: Redige, reescreve, revisa, avalia e valida minutas de qualquer espécie de ato normativo brasileiro conforme regras fixas de redação normativa legislativa. Use esta skill sempre que o usuário pedir criar, elaborar, adaptar, corrigir, reescrever, revisar, conferir conformidade ou validar lei, medida provisória, decreto, portaria, resolução, instrução normativa, regulamento, ato de pessoal, consolidação ou outra minuta normativa, mesmo se o texto estiver na conversa, em arquivo, por caminho, anexo ou em dispositivos específicos. Não use para parecer sobre mérito jurídico, constitucionalidade ou texto não normativo.
---

# Redação e Conformidade de Escrita Normativa

## Finalidade

Use esta skill para redigir, reescrever ou avaliar a conformidade formal de minutas de atos normativos brasileiros. A referência fixa aplica critérios de redação legislativa e não substitui análise de mérito, competência, constitucionalidade ou conveniência administrativa.

## Referência obrigatória

1. Leia integralmente [as regras fixas de redação normativa legislativa](references/regras_de_redacao_normativa_legislativa.md) antes de iniciar qualquer modalidade de trabalho.
2. Trate a lista entre as tags <Regras_de_Redacao_Normativa_Legislativa> e </Regras_de_Redacao_Normativa_Legislativa> como fonte fixa dos critérios de redação. Não a altere, complete ou substitua.
3. Use o documento fornecido pelo usuário como fonte exclusiva dos fatos e do conteúdo material da minuta. Use a referência fixa somente como critério de redação e de conformidade.

## Identificação do material

Considere como documento de trabalho o texto integral colado na conversa, um anexo, um arquivo indicado por caminho, um documento acessível por referência ou os dispositivos específicos indicados pelo usuário. Leia o material disponível por inteiro antes de concluir sobre sua conformidade.

Se o usuário apresentar apenas parte da minuta, leia também o contexto necessário para entender a unidade normativa. Para redigir nova minuta, use os requisitos, fatos e fundamentos fornecidos pelo usuário como material de trabalho.

Peça esclarecimento conciso somente quando faltar informação indispensável ao texto solicitado, como espécie normativa, autoridade competente, objeto, âmbito de aplicação, fundamento de validade ou conteúdo material. Não presuma esses dados.

## Escolha da modalidade

Aplique a modalidade correspondente à intenção principal do pedido.

- **Redação:** quando o usuário pedir para criar, elaborar ou redigir uma minuta.
- **Reescrita:** quando o usuário pedir para adequar, corrigir, reformular, aprimorar ou padronizar uma minuta ou dispositivo.
- **Avaliação de conformidade:** quando o usuário pedir para avaliar, revisar, conferir, validar, apontar problemas, elaborar relatório ou verificar a conformidade da redação.
- **Pedido combinado:** siga a ordem solicitada. Se o usuário pedir avaliação e ajuste sem definir ordem, apresente primeiro o relatório sobre o texto original e, em seguida, a minuta ou os dispositivos ajustados. Se pedir validação da versão reescrita, avalie a versão final.

## Redação e reescrita

Leia a referência fixa e aplique apenas as regras pertinentes à espécie, ao conteúdo e ao escopo solicitado.

Preserve o conteúdo material, o alcance normativo e os dispositivos não abrangidos pelo pedido, salvo quando o ajuste formal for necessário para atender à referência fixa. Não invente fatos, competências, efeitos, requisitos, datas, autoridades ou fundamentos de validade.

Para dados formais indispensáveis que não foram fornecidos, use marcador entre colchetes apenas quando isso permitir entregar a minuta sem presumir conteúdo, por exemplo, [número], [data] ou [autoridade competente].

Entregue somente o texto solicitado, no formato pedido pelo usuário. Não produza relatório de conformidade, sugestões ou explicações adicionais, exceto quando o usuário os pedir.

## Avaliação de conformidade

Classifique internamente cada item de regra como aplicável e conforme, aplicável e não conforme ou não aplicável. Aplique as exceções e condicionais da referência fixa antes de definir o status da Dimensão.

Ao avaliar minuta, não trate como desconformidade a ausência, a incompletude ou o caráter provisório da epígrafe, inclusive espécie normativa, numeração, siglas oficiais e data de assinatura. Também não trate como desconformidade o fecho provisório, inclusive data de assinatura e a menção aos anos transcorridos desde a Independência e a Proclamação da República nas espécies lei, medida provisória e decreto.

Use estes critérios de status:

- **✅ Ok!:** há pelo menos um item de regra aplicável e todos os itens aplicáveis estão em conformidade.
- **⚠️ Parcial:** há pelo menos um item de regra aplicável em conformidade e pelo menos um item de regra aplicável não conforme.
- **❌ Não conforme integral:** há pelo menos um item de regra aplicável e todos os itens aplicáveis estão não conformes.
- **⚪ Não se aplica:** nenhum item de regra da Dimensão se aplica à espécie ou ao conteúdo analisado.

Para Dimensão com status “⚠️ Parcial” ou “❌ Não conforme integral”, conte cada item de regra aplicável não conforme uma única vez, mesmo quando mais de um item incidir sobre o mesmo dispositivo. Use “n/a” para as demais Dimensões.

Não desdobre itens individuais com status “⚪ Não se aplica” no relatório inicial. Faça esse detalhamento apenas quando o usuário o pedir em interação posterior.

## Formato do relatório

Produza apenas as seções aplicáveis, na ordem abaixo.

# Relatório de Conformidade de Redação Normativa

| Nome da Dimensão | Conformidade | Qtd. Itens não conforme |
|------------------|--------------|-------------------------|
| Estrutura, objeto e âmbito de aplicação | <valor_da_analise> | <qtd_nao_conforme> |
| Epígrafe e numeração formal do ato | <valor_da_analise> | <qtd_nao_conforme> |
| Ementa | <valor_da_analise> | <qtd_nao_conforme> |
| Preâmbulo, fundamento de validade e fecho | <valor_da_analise> | <qtd_nao_conforme> |
| Clareza, precisão, gramática e vocabulário | <valor_da_analise> | <qtd_nao_conforme> |
| Conceitos, siglas e denominações | <valor_da_analise> | <qtd_nao_conforme> |
| Números, datas e valores | <valor_da_analise> | <qtd_nao_conforme> |
| Remissões | <valor_da_analise> | <qtd_nao_conforme> |
| Ordem lógica, articulação e pontuação | <valor_da_analise> | <qtd_nao_conforme> |
| Agrupamentos e identificação temática | <valor_da_analise> | <qtd_nao_conforme> |
| Outras Formatações do Texto | <valor_da_analise> | <qtd_nao_conforme> |
| Modalidades de alteração e preservação da identificação dos dispositivos | <valor_da_analise> | <qtd_nao_conforme> |
| Transcrição de alterações e linhas pontilhadas | <valor_da_analise> | <qtd_nao_conforme> |
| Cláusula de revogação | <valor_da_analise> | <qtd_nao_conforme> |
| Vigência e produção de efeitos | <valor_da_analise> | <qtd_nao_conforme> |
| Requisitos textuais de atos específicos | <valor_da_analise> | <qtd_nao_conforme> |
| Consolidação: reunião, limites, fusão e supressão | <valor_da_analise> | <qtd_nao_conforme> |

Substitua cada marcador pelo resultado da análise. A quantidade de itens não conformes deve corresponder aos itens de regra apresentados em “## Sugestões para Alcançar Conformidade”.

Quando houver ao menos uma Dimensão com status “⚠️ Parcial” ou “❌ Não conforme integral”, inclua as duas seções seguintes.

## Sugestões para Alcançar Conformidade

Liste cada item de regra aplicável não conforme que fundamentou o status da Dimensão. Para cada item, identifique o Dispositivo, transcreva a regra aplicável, explique a não conformidade e indique o ajuste necessário.

## Transcrição dos Ajustes para Alcançar Conformidade

Agrupe todos os ajustes incidentes sobre o mesmo Dispositivo em uma única subseção.

### Dispositivo: _XX_

#### Fundamentação da Não-conformidade e do Ajuste Necessário

Explique cada item de regra não conforme incidente sobre o Dispositivo e finalize cada fundamentação com “(Dimensão "<dimensão>" - Item "<item_dentro_da_dimensão>")”.

#### Texto Original

Transcreva o texto original do Dispositivo.

#### Texto Ajustado

Transcreva um único texto ajustado que consolide todos os ajustes necessários para o Dispositivo. Se o ajuste depender de fato ausente do documento fornecido, indique objetivamente a informação necessária sem presumir seu conteúdo.

Inclua sempre a seção final abaixo, inclusive quando todas as Dimensões estiverem em conformidade ou não se aplicarem.

# Exceções de Análise do Relatório de Conformidade

- **Dimensão** "Agrupamentos e identificação temática" - **Item** "Grafar capítulos, títulos, livros e partes em letras maiúsculas, **sem negrito**, identificados por algarismos romanos. (Decreto - art. 12, caput, inciso XVIII)":
  - Não foi viável verificar a não aplicação de negrito.
  - Assim, você deve conferir isso diretamente.

Se todas as Dimensões receberem “✅ Ok!” ou “⚪ Não se aplica”, entregue somente “# Relatório de Conformidade de Redação Normativa” e “# Exceções de Análise do Relatório de Conformidade”.

## Verificação final

Antes de responder, confirme que leu o documento de trabalho por inteiro, aplicou somente as regras pertinentes, preservou os fatos fornecidos, usou a modalidade correta e respeitou o formato solicitado.
