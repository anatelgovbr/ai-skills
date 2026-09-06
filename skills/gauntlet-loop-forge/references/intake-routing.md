# Intake and Mission Routing

## Contents

- Layer 0 — Extract supplied context
- Layer 1 — Mission and artifact
- Layer 2 — Scope and success
- Layer 3 — Verification and domain specialization
- Layer 4 — Action safety
- Layer 5 — Bounded execution
- Interview behavior


## Purpose

Interrogate only what is missing, in layers, so a vague idea becomes a concrete Gauntlet input without forcing the user to design the implementation.

## Layer 0 — Extract supplied context

Before asking anything:

- read the user's idea, prompt, plan, PRD/spec, issue, file, repo context, or linked source;
- extract explicit requirements, checklists, metrics, SLAs, constraints, forbidden actions, human gates, references, and existing quality criteria;
- mark each datum as `USER`, `SOURCE`, or later `DERIVED`;
- identify contradictions instead of silently choosing one.

## Layer 1 — Mission and artifact

Resolve:

- desired outcome;
- target audience/user/system;
- artifact(s) that should exist at the end;
- starting state;
- source of truth;
- harness/runtime.

If these are unclear, ask them before detailed verification questions.

## Layer 2 — Scope and success

Resolve:

- in scope / out of scope;
- preserved behavior/content;
- acceptance criteria;
- quality dimensions;
- hard constraints vs preferences;
- candidate quality bars.

Acceptance criteria should describe observable outcomes rather than implementation steps.

## Layer 3 — Verification and domain specialization

Classify the mission and load only relevant references.

### Software / engineering

Trigger if any material deliverable involves code, runtime behavior, technical configuration, infrastructure, APIs, databases, data pipelines, ML implementation, builds, migrations, debugging, refactoring, performance, or security engineering.

Load:
- `software-engineering.md`
- `software-testing.md`

### Research / analysis

Prioritize source quality, coverage, reproducibility, citation/grounding requirements, methodological checks, and calculation verification.

### Writing / editorial

Prioritize factuality, audience comprehension, structure, clarity, evidence, length/format constraints, and concrete comparison pieces when useful.

### Design / visual / UX

Prioritize inspectable references, matched states/viewports, interaction behavior, accessibility/usability, and reproducible captures.

### Data / ML evaluation

Prioritize frozen datasets/splits, metrics, baselines, robustness, seed/repetition control, leakage checks, resource limits, and real-world failure modes. If the work also includes implementation, activate software specialization too.

### Documents / business / operations / other

Use explicit deliverable checklists, factuality/completeness, consistency, process/state evidence, compliance constraints, and a concrete exemplar/rubric when useful.

For multi-domain missions, combine criteria rather than choosing one exclusive label.

## Layer 4 — Action safety

Resolve:

- tools and data access;
- write/deploy/publish permissions;
- secrets/credentials handling;
- irreversible actions;
- spending/external side effects;
- required human approvals.

Fail closed when authorization is ambiguous.

## Layer 5 — Bounded execution

Resolve a finite safety envelope internally. Read `bounded-execution.md`.

Do not accept “keep going forever”, “unlimited”, or an omitted cap in the final prompt.

Do not present the user with a list of internal variables or ask them to choose agent turns, executor/verifier invocations, integration cycles, delegation depth, concurrency, fan-out, tokens, or cost limits individually.

Instead, after the mission and risk are understood, ask at most one compact, plain-language maximum-effort question when the user has not already supplied an applicable limit:

> For each important part of this work, what is the maximum number of improve-and-check rounds the agents may use before they stop and report what remains? This is only a safety limit: they stop sooner as soon as the result is proven good enough.

Offer a task-informed recommendation and concise choices such as:

- **Up to 3 rounds** — a focused, low-risk task;
- **Up to 5 rounds** — a typical task with meaningful checks;
- **Up to 8 rounds** — a complex or high-risk task that needs more chances to address verified findings;
- **You decide from the task** — derive a conservative finite value.

Accept a whole number of rounds or a clearly equivalent plain-language answer. If the user delegates the choice, select 3, 5, or 8 from the task's size, risk, verification cost, and available runtime budget. A stronger quality bar does not by itself justify a larger number: it improves the decision rule, whereas the maximum only buys more attempts.

Then derive all technical caps using the mapping in `bounded-execution.md`. Label those values `DERIVED` in the prompt's safety-envelope section, but explain the selected number of rounds in user-facing language.

## Interview behavior

- Ask compact groups of related questions rather than one-at-a-time interrogation. The maximum-effort choice is one compact question, not a technical-budget questionnaire.
- Recompute gaps after each answer.
- Do not ask again for resolved information.
- Avoid asking implementation questions that the lead agent should decide.
- When ambiguity is low-risk and the user delegated judgment, derive instead of blocking.
- When ambiguity changes the definition of success, permissions, or safety, resolve it before finalizing.
