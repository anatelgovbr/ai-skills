# ADR-001: O Claude Code encontra as skills por plugin local

- Status: aceita
- Data: 2026-09-02
- Proprietário: Mantenedores da stack de IA (ai-skills)
- Participantes afetados: equipes dos repositórios que recebem a stack de IA e quem usa o Claude Code neles
- Escopo: como o Claude Code encontra as skills de `.agents/skills/` nos repositórios que recebem a stack de IA
- Substitui: nenhuma
- Substituída por: nenhuma

## Contexto

A stack de IA guarda as skills em `.agents/skills/`, um lugar só para todas as ferramentas. O GitHub Copilot e o OpenCode apontam para essa pasta por configuração: a chave `chat.agentSkillsLocations` do `.vscode/settings.json` e a chave `skills.paths` do `.opencode/opencode.json`. O Claude Code lê skills de `.claude/skills/` e de plugins, e não de `.agents/skills/`.

A stack precisa de um caminho para o Claude Code chegar em `.agents/skills/` sem manter duas cópias das skills. Na época da decisão, a maior parte das pessoas que usam os repositórios da stack, e não só a equipe que mantém a stack, trabalhava no Windows. Para que a transição fosse suave, o caminho escolhido precisava funcionar no Windows sem nenhuma intervenção manual de quem clona o repositório.

## Critérios da decisão

- Funcionar no Windows sem intervenção manual, como ligar o Modo de Desenvolvedor ou mudar a configuração do Git, porque é o sistema da maior parte de quem usa os repositórios da stack.
- Funcionar também no Linux e no macOS, inclusive em pasta sincronizada por OneDrive, Dropbox, Google Drive ou iCloud e em repositório recebido como `.zip`.
- Funcionar para quem clona o repositório, sem comando de instalação.
- Manter uma cópia só de cada skill, lida sem etapa de atualização.
- Carregar cada skill uma vez só no contexto do agente.
- Valer só dentro do repositório.

## Alternativas consideradas e tradeoffs

### Symlink `.claude/skills -> ../.agents/skills`

Não duplica arquivos e é simples de criar no Linux. No Windows, o Git só materializa o symlink com `core.symlinks=true` e o Modo de Desenvolvedor ligado, o que não é o padrão da maioria das instalações. Sem isso, o checkout deixa no lugar um arquivo de texto de 17 bytes com o caminho, e o Claude Code descarta a pasta. Pastas sincronizadas e extratores de `.zip` também transformam o link em arquivo comum, inclusive no macOS. Rejeitada por enquanto: no Windows, que é o sistema da maior parte de quem usa os repositórios, ela exigiria intervenção manual em cada máquina.

### Cópia das skills em `.claude/skills/`

Funciona em qualquer sistema, mas mantém duas cópias de cada skill. A primeira edição feita de um lado só faz as cópias divergirem, e a stack perde a fonte única. Rejeitada por não manter uma cópia só de cada skill.

### Plugin local

O arquivo `.claude-plugin/marketplace.json` declara um plugin com a origem em `./.agents`, e o Claude Code varre `.agents/skills/` a partir dele. O arquivo `.claude/settings.json` registra o marketplace do próprio repositório e liga o plugin para quem clonar. São dois arquivos JSON versionados, lidos pelo próprio Claude Code, que não dependem de recurso do sistema de arquivos. Adotada.

## Decisão e justificativa

Nos repositórios que recebem a stack de IA, o Claude Code encontra as skills de `.agents/skills/` por um plugin local chamado `stack-ai`, declarado em `.claude-plugin/marketplace.json` e ligado em `.claude/settings.json`. A stack não usa symlink nem cópia das skills. O plugin local é a única alternativa que atende a todos os critérios.

A escolha vale para o perfil atual de quem usa os repositórios da stack. Trocar o plugin pelo symlink fica para uma avaliação futura, feita por demanda.

A origem do plugin aponta para `./.agents`, e não para a raiz do repositório. Com a raiz, um `claude plugin install` copiaria o repositório inteiro para o cache de quem instalou: numa medição em repositório com código de sistema, foram mais de 190 MB, contra 1 MB com `./.agents`.

O plugin se chama sempre `stack-ai`, e o marketplace tem um nome único em cada repositório. O Claude Code guarda na máquina um caminho só para cada nome de marketplace, e dois repositórios com o mesmo nome disputariam a mesma entrada, com um deles carregando as skills do outro sem aviso.

## Consequências

### Favoráveis

- Funciona em qualquer sistema operacional e em pasta sincronizada, porque depende só de arquivos JSON.
- Quem clona o repositório não roda comando nenhum. Basta abrir o Claude Code na pasta.
- Skill nova ou editada vale na hora, porque o plugin lê `.agents/skills/` diretamente.
- O plugin vale só dentro do repositório. Uma sessão aberta em outra pasta não enxerga as skills dele.
- A skill continua sendo chamada por `/nome-da-skill`, e `/stack-ai:nome-da-skill` também funciona.

### Desfavoráveis

- As skills aparecem só a partir da segunda sessão: a primeira registra o marketplace na máquina, e a segunda carrega as skills.
- Symlink e plugin não podem conviver. Com os dois ligados, cada skill entra duas vezes no contexto, e numa stack de 40 skills isso soma perto de 3.800 tokens a mais em toda mensagem. Um repositório que ainda tem o symlink precisa removê-lo do disco e do índice do Git.
- O `.claude/settings.json` precisa ser versionado. Se ele cair numa regra do `.gitignore`, o time fica sem a configuração.
- Renomear o marketplace de uma instalação existente quebra a ligação `stack-ai@<marketplace>` e deixa uma entrada órfã no registro da máquina.

## Verificação

Comportamento medido com o Claude Code 2.1.257, num repositório real e numa máquina sem nenhum marketplace registrado: sem comando de instalação, as skills apareceram na segunda sessão, uma skill editada valeu na hora e uma sessão aberta em outra pasta não enxergou as skills do repositório. Depois de qualquer edição no manifesto do plugin, o comando `claude plugin validate <raiz do repositório>` confirma o formato.

## Gatilhos de revisão

- A maior parte de quem usa os repositórios da stack deixar de trabalhar no Windows, ou o Windows passar a aceitar symlink sem configuração manual. Nesse caso, avaliar se o symlink substitui o plugin.
- O Claude Code passar a ler `.agents/skills/` sem plugin, ou mudar o funcionamento do marketplace local.
- A stack de IA mudar o local das skills.

A revisão acontece por demanda, quando um desses gatilhos for observado ou quando alguém pedir.

## Referências

- Os arquivos `.claude-plugin/marketplace.json` e `.claude/settings.json` que a skill `stack-ai-init` instala na raiz do repositório.
- A skill `stack-ai-init`, do repositório ai-skills, que distribui a stack de IA.
