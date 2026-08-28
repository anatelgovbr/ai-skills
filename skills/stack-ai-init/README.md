# stack-ai-init

A skill `stack-ai-init` prepara um repositório para trabalhar com agentes de IA. Ela leva para a raiz do repositório de destino a estrutura mínima da stack: os arquivos que os agentes leem, as skills que eles usam e as integrações das ferramentas suportadas.

Ela é simples de propósito. Não lê o código do destino, não tenta entender o projeto, não preenche o `AGENTS.md` e não adapta nenhum arquivo ao caso: copia os artefatos da stack para o lugar certo. Descrever o sistema dentro da stack é trabalho da skill `stack-ai-creator`, em um pedido separado, depois que a estrutura já existe.

## O que chega no repositório

| Onde | Conteúdo |
|---|---|
| Raiz | `AGENTS.md`, `CLAUDE.md`, `README.md` e as linhas da stack no `.gitignore` |
| `.agents/skills/` | a `skill-creator`, as 9 fases do SpecKit e 10 skills de apoio |
| `.agents/references/` | a regra de manutenção das fases do SpecKit |
| `.specify/` | o SpecKit em si: scripts, templates, workflows e a constituição do projeto |
| `.claude/`, `.github/`, `.opencode/`, `.vscode/` | as integrações de Claude Code, GitHub Copilot, OpenCode e VS Code |

O inventário completo está em [`references/payload.md`](references/payload.md).

## O que ela garante

- **Mostra o plano antes de escrever.** A skill primeiro simula a instalação e apresenta o que pretende criar, o que vai preservar e o que vai mesclar. Só escreve depois do seu aval.
- **Não passa por cima do que já existe.** Arquivo que já está no destino é mantido como está e aparece no relatório final. `AGENTS.md`, `CLAUDE.md` e `README.md` pertencem ao projeto de destino: esses três a skill nunca substitui, mesmo quando você autoriza a substituição dos demais.
- **Soma, em vez de trocar,** nos dois arquivos que são do destino: no `.gitignore` acrescenta só as linhas que faltam, e no `.vscode/settings.json` só as chaves que faltam. Valor que você já definiu continua como está.
- **Deixa os symlinks e as permissões prontos.** O symlink `.claude/skills`, que faz o Claude Code enxergar as skills de `.agents/skills`, é recriado, e os scripts do SpecKit chegam com permissão de execução. Onde o sistema não aceita symlink, entra uma cópia de verdade, e o relatório avisa.
- **Pode ser rodada quantas vezes você quiser.** Instalar de novo no mesmo repositório não muda nada: a skill confere, avisa que está tudo no lugar e não escreve.
- **Confere o que escreveu.** Cada arquivo copiado é comparado com o original logo depois da cópia. Em uma instalação antiga, a skill refaz essa conferência e diz o que ficou diferente e o que está faltando, sem escrever nada.
- **Diz o que sobrou para você.** No fim, aponta o que ficou pendente e os dois passos manuais: preencher o `AGENTS.md` com o contexto do projeto e instalar uma das ferramentas suportadas, se você ainda não usa nenhuma.

## Prompts de exemplo

Todo trecho entre `<` e `>` é um parâmetro: substitua pela informação real antes de enviar.

Peça só o que você quer fazer. O que está na seção acima a skill já garante sozinha, e não precisa entrar no prompt.

Informe sempre o caminho da raiz do repositório de destino: a skill nunca assume que é o repositório em que você está trabalhando.

### Instalar a stack em um repositório novo

```text
Use a skill `stack-ai-init` para instalar a stack de IA no repositório em <caminho da raiz>.
```

### Conferir uma instalação antiga

Use quando a stack já foi instalada há algum tempo e você quer saber se ela continua igual à versão distribuída hoje. A resposta é um relatório do que está diferente e do que está faltando.

```text
Use a skill `stack-ai-init` para verificar a instalação da stack no repositório em <caminho da raiz>.
```

### Atualizar arquivos da stack que ficaram para trás

Use depois de uma conferência, quando você já sabe o que divergiu. A autorização é obrigatória: sem ela, a skill preserva o que encontrar.

```text
Use a skill `stack-ai-init` no repositório em <caminho da raiz> para atualizar os arquivos
da stack que estão desatualizados.

Autorizo substituir os arquivos da stack que divergirem da versão distribuída hoje.
```

## Manutenção

Esta seção é para quem mantém a skill, não para quem a usa.

Os arquivos que a skill entrega são uma cópia dos artefatos da raiz deste repositório e envelhecem sempre que a raiz muda. O procedimento para conferir e atualizar essa cópia e o motivo de cada exclusão estão em [`references/payload.md`](references/payload.md).
