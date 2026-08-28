# Diretrizes de Desenvolvimento com IA

## Contexto do Projeto

## Dependências Técnicas do Projeto

## Escopo e Limites de Escrita

## Hierarquia de Autoridade

1. Instruções explícitas do desenvolvedor na conversa atual.
2. Este arquivo (`AGENTS.md`).

Em caso de conflito, parar e solicitar decisão ao desenvolvedor.

## Guardrails Universais

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
