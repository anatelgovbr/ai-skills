# Software Test Strategy for Gauntlet Work

## Contents

- TDD micro-loop
- Test-layer selection
- Test doubles and fidelity
- Regression and characterization
- Contract testing
- Property/invariant and parameterized tests
- Mutation testing
- Security verification
- Reliability and fault tolerance
- Performance and scalability
- Database and migration testing
- Static and build gates
- Test quality and flakiness
- Evidence hierarchy
- Sources


Use this reference to choose **the smallest test portfolio that gives strong evidence for the specific risk**, not to maximize test count.

## 1. TDD micro-loop

For behavior-changing work, prefer:

`test list → RED → GREEN → REFACTOR → broader regression evidence`

Before the first code change, identify the next behavior/example. A good red test fails for the expected behavioral reason. A good green test passes because the desired behavior exists, not because assertions were weakened or dependencies were over-mocked.

Keep internal TDD retries bounded by the executor's invocation/turn budget.

## 2. Test-layer selection

Use a portfolio rather than relying on a single test type.

### Small/unit/component tests

Use for fast, specific feedback on logic and edge cases. Prefer many fast tests where they provide real confidence.

### Integration tests

Use to prove components/dependencies collaborate correctly, especially where isolated tests could pass while wiring/contracts fail.

### End-to-end / critical user journey tests

Use a smaller number for high-value workflows and system fidelity. Avoid making E2E the entire suite when cheaper focused tests can isolate the same failure.

Do not mechanically enforce a fixed numeric unit/integration/E2E ratio. Balance the suite using tradeoffs in speed, maintainability, utilization/cost, reliability/flakiness, and fidelity to production conditions.

## 3. Test doubles and fidelity

Prefer the highest-fidelity dependency that remains practical and deterministic:

1. real implementation when safe/practical;
2. a maintained fake when real use is impractical;
3. mocks/stubs when needed for isolation or hard-to-trigger cases.

Do not mock away the production behavior the test is supposed to prove.

## 4. Regression and characterization

For a bug, write a regression test that reproduces it before the fix whenever feasible.

For legacy/refactoring work, establish characterization tests around behavior that must remain stable. Create seams/observability where needed to make risky code testable before changing it.

## 5. Contract testing

For service/API/event integrations, use contract tests when they provide faster, more focused evidence than broad E2E tests. Verify both consumer expectations and provider conformance as appropriate to the architecture.

Do not confuse static schema validation with behavioral consumer/provider contract evidence.

## 6. Property/invariant and parameterized tests

Use when behavior can be expressed as invariants across broad input spaces, boundary values, or combinatorial cases. They are especially useful for parsers, serialization, algorithms, financial/math rules, transformations, state machines, and data processing.

Record seeds/examples needed to reproduce a discovered failure.

## 7. Mutation testing

For high-risk changed logic where tooling exists, mutation testing can test the **tests**: intentionally modified production behavior should be caught by the suite.

Use mutation score as supporting evidence, not a universal threshold. Investigate important surviving mutants rather than gaming the number.

## 8. Security verification

For security-relevant systems, derive tests from actual threats and requirements. Where applicable use recognized verification requirements such as OWASP ASVS as a source for technical security controls.

Potential evidence includes:

- authn/authz boundary tests;
- injection/untrusted-input cases;
- secret/PII handling;
- dependency/SAST findings;
- session/crypto/configuration controls;
- least privilege;
- abuse/rate-limit/error-path behavior.

A clean generic unit suite is not a substitute for security verification.

## 9. Reliability and fault tolerance

Test relevant failure modes:

- timeout;
- retry and duplicate delivery;
- idempotency;
- partial dependency failure;
- stale state/concurrency/races;
- restart/recovery;
- rollback;
- queue/event reprocessing;
- degraded mode;
- data consistency after failure.

Use fault injection or controlled dependency failures when appropriate.

## 10. Performance and scalability

When performance matters, define a baseline/threshold before optimization and measure under reproducible conditions.

Possible gates:

- latency percentiles;
- throughput;
- memory/CPU/resource use;
- load/scalability behavior;
- soak stability;
- regression tolerance against a frozen baseline.

Do not accept a microbenchmark that does not represent the performance requirement it claims to prove.

## 11. Database and migration testing

As applicable verify:

- forward migration;
- backward/compatibility window;
- idempotency/retry behavior;
- data invariants;
- rollback/restore plan;
- large-data/runtime characteristics;
- deployment ordering with mixed application versions.

Destructive production actions remain human-gated.

## 12. Static and build gates

Use project-appropriate build, compiler/type, lint, formatting-policy, static-analysis, generated-schema, and dependency checks as objective evidence. Do not let style-only tooling overrule a user-defined functional requirement unless it is a mandatory project gate.

## 13. Test quality and flakiness

A verifier should reject tests that are:

- non-deterministic without controlled/reproducible conditions;
- assertion-free or trivially true;
- coupled to irrelevant implementation details;
- so heavily mocked that they cannot catch the target defect;
- weakened, skipped, or deleted merely to make the suite green;
- duplicative without adding risk coverage.

Record and isolate known flaky tests rather than silently rerunning until green. Retry budgets remain finite and visible.

## 14. Evidence hierarchy for software

Prefer, roughly:

1. failing pre-change acceptance/regression evidence when feasible;
2. focused passing post-change test;
3. relevant broader regression/integration suite;
4. runtime/contract evidence;
5. non-functional/security/reliability evidence;
6. code review/static inspection;
7. subjective comparison only for dimensions not objectively decidable.

## 15. Sources informing this profile

- Martin Fowler, Test-Driven Development (Red–Green–Refactor and maintaining a test list): https://martinfowler.com/bliki/TestDrivenDevelopment.html
- Google Testing Blog, testing pyramid and SMURF tradeoffs: https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html and https://testing.googleblog.com/2024/10/
- Google Testing Blog, test fidelity and test doubles: https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html
- Pact documentation, consumer/provider contract testing: https://docs.pact.io/
- Hypothesis documentation, property-based testing: https://hypothesis.readthedocs.io/
- PIT/Stryker documentation, mutation testing: https://pitest.org/ and https://stryker-mutator.io/docs/
- OWASP ASVS, technical security verification requirements: https://owasp.org/www-project-application-security-verification-standard/
