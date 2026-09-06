---
name: gauntlet-loop-forge
description: Create or optimize a bounded, evidence-driven Gauntlet Loop execution prompt from any goal, idea, plan, specification, or existing prompt. Interview the user in layers until the mission, quality bar, acceptance criteria, verification evidence, constraints, permissions, human gates, and one user-friendly maximum-effort choice are resolved; then derive the finite technical safety envelope and return one paste-ready prompt while preserving lead-agent autonomy and independent builder/critic review. Route automatically to domain-specific verification. When the mission includes software, code, systems, APIs, infrastructure, data/ML engineering, debugging, refactoring, migration, or technical implementation, activate the bundled software-engineering profile with TDD, regression/contract/integration/E2E testing, non-functional gates, and bounded executor/verifier loops. PASS requires evidence; exhausted limits are CAPPED, never PASS.
---

# Gauntlet Loop Forge

Create or optimize a **paste-ready Gauntlet Loop execution prompt**. Do not execute the underlying mission unless the user separately asks you to run it.

Preserve these invariants:

- give the lead agent the destination and hard constraints, not a premature implementation recipe;
- use a real, inspectable quality bar rather than vague excellence language;
- let the lead decompose the mission into the smallest independently judgeable workstreams;
- never let a builder/executor approve its own work;
- have fresh-context critics/verifiers inspect the actual artifact and direct evidence, not builder summaries;
- prefer deterministic evidence where it can decide correctness; use blind comparison for genuinely comparative or subjective dimensions;
- stop early on evidence-backed `PASS`;
- make every iterative path finite: reaching a declared limit yields `CAPPED`, never `PASS`;
- require explicit human approval before increasing any safety limit.

Read `references/method-core.md` when canonical Gauntlet fidelity is uncertain.

## 1. Extract before asking

Accept an inline idea, goal, existing prompt, PRD, issue, plan, specification, requirements document, repo context, or other source material.

Extract every usable fact first. Treat an explicitly designated source of truth as authoritative unless the user says otherwise. Do not ask again for information already present.

If the environment cannot provide separate contexts/subagents, state that independence is degraded and write a portable approximation. Never call same-context self-review an independent critic.

## 2. Classify the mission and load only relevant specialization

Classify the mission after the first extraction pass. It may be single-domain or mixed-domain.

Always use the general core. Then load only the needed domain guidance:

- for quality-bar patterns across common domains, read `references/domain-bars.md`;
- **if any material part of the mission is software/engineering**, read both `references/software-engineering.md` and `references/software-testing.md` before finalizing acceptance criteria, delegation contracts, or verification gates;
- for any mission with uncertain or subjective judging, read `references/verification-protocol.md`;
- for every mission, resolve the finite safety envelope using `references/bounded-execution.md`.

Treat software as activated when the requested artifact or work includes code, repositories, services, APIs, CLIs, libraries, infrastructure/configuration, databases/migrations, build systems, technical automation, security fixes, performance engineering, data pipelines, or ML system implementation/evaluation.

For mixed missions, compose compatible verification layers rather than forcing one domain's bar onto the whole artifact.

Read `references/intake-routing.md` for detailed routing and interview logic.

## 3. Interview in layers until the prompt is actually buildable and judgeable

Do **not** emit the final Gauntlet prompt while a material requirement below remains unresolved, unless the user explicitly delegates that decision to you.

Ask missing items in compact batches. After every answer, recompute the gap list and ask only what remains material.

Resolve, at minimum:

1. **Mission** — concrete outcome and intended user/system-visible result.
2. **Artifact(s)** — what real outputs will exist and be inspected.
3. **Starting state / source of truth** — greenfield, existing artifact, rewrite, repair, optimization, evaluation, migration, etc.
4. **Scope boundaries** — in scope, out of scope, preserved behavior/content, dependencies.
5. **Target harness/runtime** — Claude Code/SDK, Codex, OpenAI Agents SDK, another agentic runtime, plain chat, or unknown.
6. **Acceptance criteria / definition of done** — observable conditions for completion.
7. **Quality bar** — concrete exemplar, benchmark, test suite, rubric, gold output, reference implementation, threshold, or hybrid bar the critic can actually inspect.
8. **Verification plan / hard gates** — objective checks that must pass, plus comparative judging only where useful.
9. **Quality dimensions / non-functional requirements** — domain-relevant properties such as correctness, clarity, robustness, security, latency, accessibility, maintainability, groundedness, fidelity, or compliance.
10. **Hard constraints versus preferences** — language, format, stack, compatibility, word count, platform, policy/legal boundaries, style constraints, etc.
11. **Tools, data, access, and permissions** — what the agents may read, run, edit, fetch, test, deploy, spend, or call.
12. **Human gates / irreversible actions** — anything requiring explicit approval.
13. **Maximum effort** — ask one plain-language question about the maximum number of improve-and-check rounds that each important part of the work may use. The user chooses a number, selects a concise effort option, or delegates the choice. Never ask the user to size internal variables such as turns, invocations, delegation depth, concurrency, or global fan-out.
14. **Observability** — evidence ledger/progress artifact and evidence types the user wants retained.

Translate the maximum-effort answer into every finite technical limit required by the runtime and prompt. Use the deterministic derivation in `references/bounded-execution.md`, mark derived values `DERIVED`, and distinguish them from user requirements. The user-facing explanation should say how many improve-and-check rounds the choice allows, not make the user validate an internal budget form.

If the user delegates missing decisions, derive them conservatively, label them `DERIVED`, and distinguish assumptions from user requirements.

Do not ask the user to prescribe architecture, file layout, exact decomposition, or implementation sequence unless those are genuine constraints. Preserve lead-agent autonomy.

## 4. Resolve the quality bar

A bar must be sufficiently:

- **concrete** — named or operationally defined;
- **inspectable** — the verifier can read, run, render, measure, or otherwise examine it;
- **comparable** — candidate and bar share explicit evaluation dimensions;
- **reproducible** — material comparison conditions are stable or documented;
- **challenging** — it prevents easy rubber-stamping.

Prefer a **hybrid bar** when one mechanism cannot settle all dimensions: deterministic gates for objective properties plus an exemplar/rubric for subjective ones.

Reject vague phrases such as “world-class”, “production-ready”, “perfect”, “clean”, or “enterprise-grade” until converted into observable criteria.

If the user has no usable bar, propose 2–3 concrete candidates or a measurable equivalent. If finding the right bar itself requires domain investigation, make bar discovery the lead agent's first bounded task.

## 5. Build roles and evidence flow

The final prompt must define roles without unnecessary vendor lock-in:

- **Lead/orchestrator** — interprets the mission, chooses decomposition, manages dependencies and finite budget, tracks evidence, and integrates the whole. It may not grade implementation work it authored.
- **Executor/builder per workstream** — creates or revises one bounded piece and produces direct evidence. It may self-check but cannot declare final `PASS`.
- **Fresh verifier/critic** — receives the goal, assigned criteria, actual artifact, relevant constraints, and direct evidence; it does not receive the executor's self-assessment or rationale. It decides against the bar.
- **Integrator/smoother** — reconciles interfaces, consistency, regressions, and cross-workstream effects after local convergence.
- **Fresh final verifier** — evaluates the integrated whole against global acceptance criteria and gates.

Parallelize only genuinely independent workstreams and never beyond the configured concurrency cap.

For software missions, the executor/verifier contract is further constrained by the TDD and test-evidence rules in `references/software-engineering.md` and `references/software-testing.md`.

## 6. Use evidence-first verification

A verifier inspects the **actual current artifact/version** and direct evidence. Builder claims are not evidence.

When a round fails, require at least:

- explicit verdict/status;
- criterion-by-criterion evidence or missing evidence;
- every blocking finding;
- the single highest-impact remaining gap;
- an objective acceptance check for the next revision;
- residual non-blocking risks when useful.

For pairwise/LLM judging, mask provenance when feasible and reverse A/B order. If the winner flips, return `INCONCLUSIVE` and prefer stronger evidence or a fresh judge.

Read `references/verification-protocol.md` for the detailed contract.

## 7. Make the loop bounded without confusing caps with quality

Define one local Gauntlet cycle as:

`executor revision → direct evidence → fresh verifier → verdict + largest gap`

Rules:

1. stop immediately when assigned criteria and gates earn evidence-backed `PASS`;
2. never exceed the declared local or global caps;
3. count hidden retries, self-fix loops, extra reviewers, replans, tool-runner loops, and nested agents against explicit budgets;
4. disallow recursive fan-out beyond `MAX_DELEGATION_DEPTH`;
5. if progress stagnates, replan/split/escalate rather than repeating the same attempt until the cap;
6. if any hard ceiling is reached before `PASS`, return `CAPPED` with unresolved findings and the recommended next action;
7. never auto-extend a cap; only explicit human approval can authorize a continuation envelope.

Do **not** add a minimum number of rounds. A single excellent, independently verified cycle may be sufficient. A maximum is a safety boundary, not a quality target.

Read `references/bounded-execution.md` for budget inheritance, the maximum-effort-to-envelope derivation, and terminal semantics.

## 8. Require honest terminal states

Use at least:

- `PASS` — all mandatory acceptance criteria/gates are evidenced, no blocking/critical finding remains, and any required comparative bar is satisfied;
- `FAIL` — current version fails but another permitted cycle remains;
- `INCONCLUSIVE` — evidence or judge consistency is insufficient;
- `ESCALATE` — requirements, bar, decomposition, or strategy need reframing;
- `BLOCKED` — missing access, permission, dependency, environment, data, or human gate;
- `CAPPED` — a finite cycle/turn/spawn/time/token/cost boundary was reached before success;
- `STOPPED` — human intentionally stopped the run.

Never convert a non-`PASS` terminal state into `PASS` merely because the run ended.

## 9. Require a lightweight evidence ledger

Have the lead maintain a progress/evidence artifact appropriate to the harness, such as `workbench.md`, containing enough to audit:

- workstream and owner;
- artifact/version locator;
- assigned acceptance criteria/bar;
- direct gate/evidence results;
- current cycle and remaining budget;
- verifier verdict and largest gap;
- change attempted and observed delta;
- open findings/residual risks;
- human gates;
- integration/final-verifier status.

Keep observability useful but not bureaucratic.

## 10. Adapt to the harness honestly

Map semantic limits to runtime controls only when those controls actually exist in the user's environment. Do not invent flags or feature names.

Retain prompt-level workstream/global caps even when the runtime exposes a `max_turns`, cost, timeout, depth, or concurrency limit, because runtime exhaustion and quality status are different concepts.

For a plain chat without real subagents/fresh contexts, explicitly describe the result as a degraded simulation and preserve visible role separation as far as possible.

## 11. Compose the final Gauntlet prompt

Keep the final execution prompt as short as possible without losing enforceability. It should communicate, in a natural operational order:

1. mission and source of truth;
2. hard constraints and exclusions;
3. quality bar and acceptance criteria;
4. verification/hard gates;
5. lead autonomy over approach and decomposition;
6. executor + fresh verifier separation;
7. exact finite safety envelope;
8. evidence/failed-round contract;
9. integration + fresh final verification;
10. human gates/forbidden actions;
11. evidence ledger;
12. exact `PASS` versus `CAPPED` semantics.

For software missions, also include only the software/TDD/test clauses that are relevant to the task. Do not paste an entire testing encyclopedia into every prompt.

Read `references/output-template.md` when a reliable assembly skeleton is useful.

## 12. Optimize an existing prompt

When the user provides an existing Gauntlet prompt, diagnose it against the same invariants and rewrite only what materially improves fidelity, verification, boundedness, or domain fit.

Preserve useful user constraints. Remove duplicated methodology prose, arbitrary minimum-round requirements, unbounded retry paths, self-approval, vague bars, unsupported runtime commands, and irrelevant domain-specific checks.

## 13. Final self-gate before returning the prompt

Verify that:

- every material intake field is resolved or explicitly delegated;
- the mission says what outcome matters without unnecessary route prescription;
- the domain was classified correctly and only relevant specializations were loaded;
- every acceptance criterion has a credible evidence path;
- the quality bar is real/operational and not hand-wavy;
- executor and verifier are independent in role/context as far as the harness allows;
- verifiers inspect current artifacts/evidence rather than summaries;
- subjective pairwise judging is used only where it adds information;
- all iterative/spawn paths have finite explicit ceilings;
- a cap means `CAPPED`, never success, and only a human can extend it;
- integrated output receives an independent whole-artifact verification;
- **for software missions:** the appropriate TDD/regression/test strategy and engineering gates are present, with test scope proportional to risk;
- the generated prompt remains compact and executable.

Only then return the paste-ready Gauntlet Loop prompt.
