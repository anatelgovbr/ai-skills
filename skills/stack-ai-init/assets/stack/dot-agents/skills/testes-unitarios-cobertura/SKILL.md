---
name: testes-unitarios-cobertura
description: >
  Impõe teste unitário de caixa branca e cobertura mínima de 90% de linhas e de ramos como condição de entrega de qualquer código novo ou alterado. Use sempre que o pedido criar, alterar, corrigir ou refatorar código de produção, e quando o pedido for configurar testes, cobertura, Codecov ou o gate de cobertura em integração contínua. Também use para conferir se uma entrega cumpre o gate. Não se aplica a mudança exclusivamente em documentação, que segue a skill documentacao-obrigatoria.
compatibility: Requer Python 3.9 ou superior para o script de gate e a ferramenta de teste e cobertura da linguagem do projeto.
---

# Testes unitários e cobertura obrigatória

Uma skill é compromisso de competência. Nesta, o compromisso é: nenhum código de produção é entregue sem teste unitário que o exercite por dentro e sem relatório de cobertura que prove isso.

Teste unitário, aqui, é análise de caixa branca. O caso de teste nasce da estrutura do código: cada decisão, cada ramo, cada limite e cada caminho de exceção. Teste que só confirma o caminho feliz não cumpre esta skill.

## Gates não negociáveis

| Gate | Mínimo | Como se prova |
|---|---|---|
| Cobertura de linhas, projeto inteiro | 90% | `scripts/verificar_cobertura.py` sobre o relatório gerado |
| Cobertura de ramos, projeto inteiro | 90% | o mesmo comando; relatório sem medição de ramos reprova |
| Cobertura do código novo ou alterado | 90% | status `patch` do Codecov, ou relatório do GitLab no merge request |
| Não regressão | cobertura total não cai | `--linha-base` com o JSON da execução anterior, ou status `project` do Codecov |
| Suíte inteira | 0 falha, 0 teste pulado sem justificativa | saída do executor de testes |

Os mínimos valem para projeto novo e para todo código novo em projeto antigo. Projeto legado abaixo de 90% segue o regime de "Código legado", abaixo. Nenhum mínimo é reduzido por decisão do agente.

## Fluxo obrigatório

1. **Localize a infraestrutura de teste do projeto.** Leia o `AGENTS.md`, o manifesto de dependências e a configuração de CI. Se o projeto não tiver executor de teste nem ferramenta de cobertura, pare: a primeira entrega é montar essa infraestrutura, em mudança própria, com o comando registrado no `AGENTS.md`. Não escreva código de produção antes disso.
2. **Vermelho.** Escreva primeiro o teste que descreve o comportamento pedido ou reproduz o defeito. Rode e guarde a saída da falha. Teste que passa antes da implementação não prova nada: reescreva.
3. **Verde.** Implemente o mínimo para o teste passar. Rode a suíte inteira, não só o teste novo.
4. **Caixa branca.** Leia o código que você escreveu ou alterou e complete os casos pela lista de "O que testar". Rode com cobertura de ramos ligada.
5. **Refatore** com a suíte verde, rodando de novo a cada passo.
6. **Gate.** Gere o relatório e rode:

```bash
python3 <caminho-desta-skill>/scripts/verificar_cobertura.py --relatorio <arquivo> --minimo-linhas 90 --minimo-ramos 90
```

Código de saída `0` aprova, `1` reprova e `2` indica relatório ausente ou inválido. Reprovado, volte ao passo 4. O comando de cada linguagem para gerar o relatório está em `references/comandos-por-linguagem.md`.

## O que testar

Para cada unidade nova ou alterada:

- cada ramo de cada `if`, `switch`, operador ternário e curto-circuito lógico, nos dois sentidos;
- cada laço com zero, uma e várias iterações;
- valores de fronteira: mínimo, máximo, logo abaixo e logo acima de cada limite, vazio, nulo e tamanho máximo;
- cada exceção lançada ou tratada, com asserção sobre o tipo e a mensagem ou o código de erro;
- entrada inválida e maliciosa nos pontos que recebem dado externo, cruzando com os tópicos S04 a S11 de `.agents/security/guia-seguranca.md` quando a stack estiver instalada;
- regra de autorização: o usuário permitido passa e o não permitido é barrado, com teste para cada perfil;
- todo defeito corrigido ganha um teste de regressão com o identificador do defeito no nome ou na descrição.

Módulo crítico, que trata autenticação, autorização, dado pessoal, cálculo financeiro, prazo legal ou decisão administrativa, exige também teste de mutação com pontuação mínima de 70% nas unidades alteradas. As ferramentas por linguagem estão em `references/comandos-por-linguagem.md`.

## Proibições

Cada item abaixo reprova a entrega, mesmo com o gate numérico aprovado:

- reduzir mínimo de cobertura em configuração, pipeline ou `codecov.yml`;
- acrescentar exclusão de cobertura, como `pragma: no cover`, `@codeCoverageIgnore`, `istanbul ignore` ou lista `omit`, sem registro de decisão de arquitetura que a justifique;
- apagar, comentar, pular ou marcar como esperado-falhar um teste existente para a suíte passar;
- teste sem asserção, ou com asserção que não pode falhar;
- simular (mock) a própria unidade sob teste; simule só a fronteira externa, como rede, relógio, banco e sistema de arquivos;
- declarar a entrega concluída sem a saída do gate na resposta.

## Código legado

Projeto que hoje está abaixo de 90% não vira exceção permanente. O regime é:

1. Meça a cobertura atual e grave o resultado com `--json` como linha de base versionada.
2. A partir daí, todo código novo ou alterado cumpre 90% de linhas e de ramos, e a cobertura total não pode cair (`--linha-base`).
3. Toda alteração em arquivo legado sem teste começa por um teste de caracterização, que registra o comportamento atual antes da mudança.
4. O plano de recuperação até 90% no projeto inteiro entra como decisão de arquitetura, com prazo e responsável.

## Integração contínua e Codecov

O gate precisa rodar no pipeline, não só na sessão do agente. Os modelos estão em `assets/`:

| Arquivo | Uso |
|---|---|
| `assets/ci/github-actions.yml` | GitHub Actions com testes, gate e envio ao Codecov |
| `assets/ci/gitlab-ci.yml` | GitLab CI com testes, gate e relatório de cobertura no merge request |
| `assets/codecov.yml` | metas de 90% para o projeto e para o código novo, sem tolerância |

Repositório público pode usar o Codecov em nuvem. Código que não pode sair da rede do órgão usa o relatório nativo do GitLab ou uma instância própria do Codecov: o gate é o script, e o Codecov é a camada de visibilidade. O `merge` só fica liberado com o job de cobertura aprovado, configurado como verificação obrigatória na proteção do ramo principal.

## Evidência na resposta final

A resposta que entrega código traz, nesta ordem:

1. a saída do teste falhando no passo 2;
2. o comando e a saída da suíte inteira passando;
3. o comando e a saída de `verificar_cobertura.py`, com linhas, ramos e `APROVADO`;
4. a lista dos casos de caixa branca cobertos por unidade alterada.

Sem esses quatro itens, a entrega é reportada como pendente, com o motivo.

## Handoff

### Recebe de
- Qualquer skill que altere codigo de producao: espera a lista de arquivos alterados e o objetivo da mudanca.

### Entrega para
- Revisao de codigo (`code-reviewer` ou equivalente): lista de arquivos testados, saida do gate (linhas, ramos, resultado), e testes adicionados com contagem.
