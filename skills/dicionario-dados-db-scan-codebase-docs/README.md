# dicionario-dados-db-scan-codebase-docs

Skill de agente que cria, atualiza e verifica a documentação estrutural e semântica de um banco de dados: `dicionario_tabelas.md`, `dicionario_colunas.md` e `CHANGELOG.md`. Toda descrição publicada segue uma fórmula obrigatória e só nasce de evidência rastreável na codebase (scripts de banco, ORM, regras de negócio, integrações, telas), nunca de suposição. Ela não conhece nenhum sistema de antemão; aprende o alvo através de um adaptador, que pode já existir no projeto ou ser criado sob autorização sua.

## Como ela é acionada

É uma skill de modelo, não um comando digitado. Basta descrever o que você quer em linguagem natural, no seu agente:

- "Cria o dicionário de dados do módulo de cobrança."
- "Atualiza o dicionário de dados para a versão 4.2 do schema."
- "Verifica se o dicionário de dados da tabela pedidos está batendo com o banco."

O agente interpreta alvo (sistema/módulo), intenção (criar, atualizar ou verificar) e artefatos envolvidos a partir do pedido e da inspeção da codebase, sem exigir nomes técnicos internos.

## Primeiro uso num projeto: o adaptador

A skill não presume linguagem, caminho, convenção de nome ou destino de arquivo de nenhum sistema. Essa informação fica em um adaptador, registrado em `registro-adaptadores.md`. Este repositório entrega a skill sem nenhum adaptador cadastrado.

Ao pedir algo para um alvo ainda não registrado, o agente:

1. Investiga a codebase e relata o que já consegue reconhecer e o que permanece indeterminado (caminho da fonte estrutural, convenção de identificadores, destino dos arquivos etc.).
2. Pergunta se você autoriza criar e registrar um adaptador para esse alvo.
3. Só cria o adaptador com sua autorização explícita; sem ela, um pedido de verificação segue usando o que for possível estabelecer sem convenções presumidas, e um pedido de criação ou atualização é encerrado sem escrever nada.

Criar o adaptador é opcional e por decisão sua a cada alvo novo, não um passo automático. Um projeto com vários sistemas acumula um adaptador por sistema conforme forem sendo usados.

## O que ela produz

| Artefato | Quando |
|---|---|
| `dicionario_tabelas.md` | Uma linha por tabela: identificador físico e descrição. |
| `dicionario_colunas.md` | Índice de tabelas e, por tabela, uma linha por coluna com sua descrição. |
| `CHANGELOG.md` | Só fatos de estrutura por versão (tabela/coluna/chave/índice/restrição adicionada, alterada ou excluída); nunca significado de negócio. |
| Relatório de atualização | Gerado quando uma atualização produz delta em tabela, coluna ou outra propriedade física; mostra escopo, resumo numérico e evidências. |
| Relatório de varredura | Só na resposta ao agente, nunca gravado em arquivo; mostra evidências, conflitos, lacunas e o resultado dos critérios A1 a A10. |

Se algum dado necessário para completar uma descrição não puder ser confirmado na codebase (ou em material complementar que você anexar), o objeto fica registrado como lacuna no relatório em vez de publicado com suposição.

## Verificação automatizada (opcional)

Nenhuma dependência é necessária para o agente usar a skill. Só o verificador automatizado opcional, `scripts/verificar_dicionario.py`, precisa de Python 3, sem bibliotecas externas. Ele valida a forma e a consistência dos artefatos já escritos. Use a partir da raiz desta pasta:

```bash
# forma de dicionario_tabelas.md
python3 scripts/verificar_dicionario.py formato caminho/dicionario_tabelas.md --padrao-versao '<regex do título>'

# forma de dicionario_colunas.md, com ordem das colunas
python3 scripts/verificar_dicionario.py formato caminho/dicionario_colunas.md --checar-ordem --padrao-pk '<padrão>' --padrao-versao '<regex do título>'

# tabelas e colunas descrevem o mesmo conjunto
python3 scripts/verificar_dicionario.py tabelas-colunas --tabelas caminho/dicionario_tabelas.md --colunas caminho/dicionario_colunas.md

# CHANGELOG.md
python3 scripts/verificar_dicionario.py changelog caminho/ --padrao-versao '<regex>' --ordem-versoes '<mais-recente,...,mais-antiga>'

# diferença estrutural entre duas versões de dicionario_colunas.md
python3 scripts/verificar_dicionario.py diff --antigo snapshot-anterior/dicionario_colunas.md --novo caminho/dicionario_colunas.md --json
```

Saída: `0` sem achado, `1` com achado, `2` entrada inválida. `--padrao-pk`, `--padrao-versao` e `--ordem-versoes` só se aplicam quando o adaptador do alvo declarar esses valores.

Para rodar a suíte de testes do próprio script (só necessário depois de alterar `verificar_dicionario.py`):

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
```

## Estrutura da skill

```text
SKILL.md                          ponto de entrada: fluxo, gates e fontes de regra
registro-adaptadores.md           mapa de alvo → adaptador (vazio até você criar um)
references/
  contrato-de-adaptador.md        seleção de adaptador e tratamento de alvo sem adaptador
  criacao-adaptador.md            contrato para criar um adaptador novo
  formato-dicionario-de-dados.md  forma exata dos artefatos
  principios-qualidade-dados.md   conteúdo, redação e critérios A1 a A10
  templates-descricao.md          fórmulas obrigatórias de descrição
  processo-analise-semantica.md   evidência, confiança, conflito e lacuna
  insumos-complementares.md       uso de material fornecido por você
  conceitos-e-instrucoes-tecnicas_descricao_tabelas_colunas.md
                                   fundamentação e exemplos completos
scripts/
  verificar_dicionario.py         verificador de forma e consistência
  test_verificar_dicionario.py    testes do verificador
adapters/                         criado quando o primeiro adaptador for registrado
```
