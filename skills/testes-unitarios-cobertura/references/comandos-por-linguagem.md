# Comandos por linguagem

Autoridade sobre: como gerar, em cada linguagem, o relatório que `scripts/verificar_cobertura.py` lê, e qual ferramenta de mutação usar em módulo crítico.

Confirme a versão da ferramenta no manifesto do projeto antes de usar o comando. Se o projeto já registra outro comando no `AGENTS.md`, o do projeto prevalece, desde que gere relatório com linhas e ramos.

## Geração do relatório

| Linguagem | Comando | Relatório | Formato |
|---|---|---|---|
| Python | `pytest --cov=<pacote> --cov-branch --cov-report=xml` | `coverage.xml` | Cobertura |
| PHP | `XDEBUG_MODE=coverage vendor/bin/phpunit --coverage-cobertura coverage.xml` | `coverage.xml` | Cobertura |
| JavaScript e TypeScript com Jest | `npx jest --coverage --coverageReporters=cobertura` | `coverage/cobertura-coverage.xml` | Cobertura |
| JavaScript e TypeScript com Vitest | `npx vitest run --coverage.enabled --coverage.reporter=cobertura` | `coverage/cobertura-coverage.xml` | Cobertura |
| Java e Kotlin com Maven | `mvn verify`, com o `jacoco-maven-plugin` e a meta `report` | `target/site/jacoco/jacoco.xml` | JaCoCo |
| Java e Kotlin com Gradle | `gradle test jacocoTestReport`, com `xml.required = true` | `build/reports/jacoco/test/jacocoTestReport.xml` | JaCoCo |
| C# e .NET | `dotnet test --collect:"XPlat Code Coverage"` | `TestResults/<execução>/coverage.cobertura.xml` | Cobertura |
| Go | `go test -coverprofile=cover.out ./...` e conversão com `gcov2lcov` | `coverage.lcov` | LCOV |

## Particularidades

**PHP.** Cobertura de ramos exige Xdebug com cobertura de caminho ligada, pelo atributo `pathCoverage="true"` no elemento `<coverage>` do `phpunit.xml`. O PCOV mede só linhas: com ele o gate reprova por falta de medição de ramos, e isso é o comportamento esperado. Arquivos em ISO-8859-1, comuns em módulos do SEI, não afetam a medição.

**Go.** A ferramenta padrão mede só instruções, não ramos. Rode o gate com `--minimo-ramos 0` e registre a limitação em decisão de arquitetura. O mínimo de linhas continua em 90%.

**Perl.** O `Devel::Cover` mede instruções, ramos e condições. Para gerar Cobertura XML, use um módulo de relatório Cobertura publicado no CPAN e confirme a disponibilidade no ambiente antes de fixar o comando no `AGENTS.md`.

**Monorrepositório.** Rode o gate uma vez por relatório, ou combine os relatórios na própria ferramenta de cobertura antes do gate. Não some percentuais à mão.

## Teste de mutação em módulo crítico

| Linguagem | Ferramenta |
|---|---|
| Python | `mutmut` |
| PHP | Infection |
| JavaScript e TypeScript | StrykerJS |
| Java e Kotlin | PIT (`pitest`) |
| C# e .NET | Stryker.NET |

Rode a mutação só sobre as unidades alteradas, para o tempo de execução ficar proporcional à mudança. Mutante sobrevivente em regra de autorização ou em cálculo é defeito de teste e bloqueia a entrega.
