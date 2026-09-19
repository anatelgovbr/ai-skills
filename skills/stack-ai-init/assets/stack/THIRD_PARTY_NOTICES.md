# Avisos de terceiros

A stack distribuída por `stack-ai-init` combina skills mantidas no repositório `ai-skills` e cópias de materiais de terceiros. Este arquivo registra origem, revisão, licença e condições de distribuição; a documentação funcional em [`docs/stack-ai/stack-de-ia.md`](./docs/stack-ai/stack-de-ia.md) serve para descoberta e uso.

A licença do repositório de destino não substitui as licenças dos materiais de terceiros. Quando a origem fornece um arquivo de licença ou de avisos próprio, ele é mantido no caminho indicado e tem precedência sobre qualquer resumo nesta página.

## Skills vendorizadas

| Skill | Origem | Revisão | Licença | Registro |
|---|---|---|---|---|
| `speckit-<fase>` (10 fases) | [github/spec-kit](https://github.com/github/spec-kit/tree/v1.0.3) | `v1.0.3` | [MIT](https://raw.githubusercontent.com/github/spec-kit/v1.0.3/LICENSE) | `.agents/skills/speckit-*/SKILL.md` |
| `skill-creator` | [Anthropic Skills](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Sem versionamento na origem | [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) | [`.agents/skills/skill-creator/LICENSE.txt`](./.agents/skills/skill-creator/LICENSE.txt) |
| `caveman` | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman/tree/v1.9.0) | `v1.9.0` | [MIT](https://raw.githubusercontent.com/JuliusBrussee/caveman/v1.9.0/LICENSE) | `.agents/skills/caveman/SKILL.md` |
| `grill-me` | [mattpocock/skills](https://github.com/mattpocock/skills/tree/v1.2.3/skills/productivity) | `v1.2.3` | [MIT](https://raw.githubusercontent.com/mattpocock/skills/v1.2.3/LICENSE) | `.agents/skills/grill-me/SKILL.md` |
| `grilling` | [mattpocock/skills](https://github.com/mattpocock/skills/tree/v1.2.3/skills/productivity) | `v1.2.3` | [MIT](https://raw.githubusercontent.com/mattpocock/skills/v1.2.3/LICENSE) | `.agents/skills/grilling/SKILL.md` |
| `writing-for-agents` | [mattpocock/skills](https://github.com/mattpocock/skills/tree/v1.2.3/skills/productivity/writing-for-agents) | `v1.2.3` | [MIT](https://raw.githubusercontent.com/mattpocock/skills/v1.2.3/LICENSE) | `.agents/skills/writing-for-agents/SKILL.md` |
| `owasp-playbook` | [OWASP/secure-agent-playbook](https://github.com/OWASP/secure-agent-playbook/tree/v0.2.7) | `v0.2.7`, commit `79fea6b9115b55687818f8c4073844ee9ba907a6` | [CC-BY-4.0](./.agents/skills/owasp-playbook/upstream/LICENSE.md); dados e componentes conforme [avisos upstream](./.agents/skills/owasp-playbook/upstream/THIRD_PARTY_NOTICES.md) | `.agents/skills/owasp-playbook/upstream/` |

### Avisos da licença MIT

#### `speckit-<fase>` (10 fases)

Copyright GitHub, Inc.

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#### `caveman`

Copyright (c) 2026 Julius Brussee

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#### `grill-me`, `grilling` e `writing-for-agents`

Copyright (c) 2026 Matt Pocock

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Skills mantidas pelo projeto `ai-skills`

`dicionario-dados-db-scan-codebase-docs` e `gauntlet-loop-forge` são mantidas pela Anatel no repositório `ai-skills`. Elas não são materiais vendorizados de terceiros; sua origem e seus arquivos distribuídos pela carga pertencem ao projeto que mantém esta skill. A licença registrada para ambas é GPL-3.0.

## Avisos incorporados pelo upstream

`owasp-playbook` inclui uma cópia literal parcial do projeto [OWASP Secure Agent Playbook](https://github.com/OWASP/secure-agent-playbook). Preserve [`upstream/LICENSE.md`](./.agents/skills/owasp-playbook/upstream/LICENSE.md) e [`upstream/THIRD_PARTY_NOTICES.md`](./.agents/skills/owasp-playbook/upstream/THIRD_PARTY_NOTICES.md) integralmente; esses arquivos registram as atribuições e as licenças do playbook, dos dados e dos demais componentes incorporados.

## Skills documentais fornecidas pelo host

`stack-ai-init` não distribui `docx`, `pdf`, `pptx`, `xlsx` ou outra skill documental fornecida pelo host. Se alguma dessas skills aparecer no destino por injeção do ambiente, ela fica fora desta carga e deste inventário; siga o `LICENSE.txt` disponibilizado pelo host.
