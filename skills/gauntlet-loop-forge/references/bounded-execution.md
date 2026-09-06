# Bounded Execution Protocol

## Contents

- Principle
- Required safety envelope
- Budget inheritance
- Workstream cycle
- Stagnation brake
- Integration
- User-friendly effort choice and budget derivation
- Runtime mapping
- Terminal semantics


## Principle

**Quality determines `PASS`; resource limits determine `CAPPED`.**

A maximum is a safety ceiling, never a target or definition of done. There is no minimum number of cycles.

## Required safety envelope

The final **execution prompt** must contain finite values for:

- `MAX_WORKSTREAM_CYCLES` — executor→verifier cycles per workstream;
- `MAX_EXECUTOR_INVOCATIONS_PER_WORKSTREAM` — includes retries hidden inside a cycle;
- `MAX_VERIFIER_INVOCATIONS_PER_WORKSTREAM` — includes fresh critics, second opinions, and rechecks;
- `MAX_INTEGRATION_CYCLES` — integrate→final-verifier cycles;
- `MAX_AGENT_TURNS` or equivalent per spawned agent when enforceable;
- `MAX_DELEGATION_DEPTH` — child-agent nesting depth;
- `MAX_CONCURRENT_AGENTS` — simultaneous workers/reviewers;
- one global fan-out/iteration ceiling such as `MAX_TOTAL_AGENT_SPAWNS` or `MAX_TOTAL_CYCLES`;
- at least one additional global boundary when practical: wall-clock, token/compute, or cost budget;
- `AUTO_EXTEND = false`.

Only explicit human approval may enlarge an envelope or authorize a continuation run.

Do not ask the user to provide this implementation-level list. Obtain one maximum-effort choice in plain language, then derive the envelope as described below.

## Budget inheritance

Every child/workstream inherits the strictest applicable remaining limit among:

1. its local cap;
2. its parent/orchestrator remaining allowance;
3. the global remaining allowance.

A child may not spawn another child if the resulting depth exceeds `MAX_DELEGATION_DEPTH`.

Count all retry-like activity: revisions, self-fix attempts, reruns, fresh critics, adversarial second opinions, tool-runner iterations, replans, test-fix retries, integration retries, and nested agent work.

There is no unlimited “internal retry” channel hidden inside a nominal single cycle.

## Workstream cycle

One cycle is:

1. executor changes or produces the artifact;
2. executor records direct evidence;
3. fresh verifier inspects current artifact + criteria + evidence;
4. verifier returns status, blocking findings, largest gap, and next acceptance check.

Stop immediately on `PASS`.

## Stagnation brake

If the dominant failure repeats for two consecutive failed cycles without measurable improvement:

- stop repeating the same strategy;
- replan, split the workstream, strengthen the evidence, or reconsider the bar/requirement;
- replanning consumes budget;
- if progress cannot be re-established, return `ESCALATE` or `CAPPED` rather than burning the remaining budget mechanically.

## Integration

Local `PASS` is not global `PASS`.

After local convergence:

- assemble the actual artifacts;
- verify cross-workstream interfaces/consistency;
- run global gates;
- use a fresh final verifier;
- repeat only while budget remains and never above `MAX_INTEGRATION_CYCLES`;
- stop early on global `PASS`.

## User-friendly effort choice and budget derivation

### Ask only for a maximum number of improve-and-check rounds

Once the task, risk, and verification needs are clear, obtain one answer in ordinary language:

> For each important part of this work, what is the maximum number of improve-and-check rounds the agents may use? They can finish earlier when the evidence proves success.

Recommend one of these task-informed choices without exposing internal limit names:

| Plain-language choice | Recommended for | Maximum rounds (`N`) |
|---|---|---:|
| Up to 3 rounds | Focused, low-risk work with cheap checks | 3 |
| Up to 5 rounds | A typical task with meaningful verification | 5 |
| Up to 8 rounds | Complex or high-risk work with costly or multi-step verification | 8 |
| You decide from the task | The user delegates effort sizing | Derive 3, 5, or 8 |

Accept any positive whole number when the user provides one. If they delegate, select `N` from the table using task size, failure cost, verification cost, and known runtime restrictions; record the selection as `DERIVED`.

This is a safety budget, not a target. Do not select a larger `N` merely because the user asks for higher quality; strengthen the bar and evidence instead. A user may give a smaller or larger finite number, but resolve whether it is practical before finalizing the prompt.

### Derive the internal envelope

Let `N` be the user's selected maximum rounds, and let `W` be the finite maximum number of independent material workstreams the lead may create. Derive `W` from the mission before writing the prompt: normally `1` for focused work, `2` for a multi-part task, and `3` for a complex mission. If the task needs more than the selected cap permits, phase the mission or obtain approval; do not leave `W` unbounded.

Calculate every expression using the selected `N` and `W`, then put only the resulting integers or booleans in the execution prompt. The formulas below are for the forge, not literals for the generated prompt. Label all values other than the user-selected `N` as `DERIVED`:

| Internal limit | Exact derivation | Purpose |
|---|---|---|
| `MAX_WORKSTREAMS` | `W` | Bounds the lead's decomposition before any work begins. |
| `MAX_WORKSTREAM_CYCLES` | `N` | Limits executor → evidence → fresh-verifier rounds per workstream. |
| `MAX_EXECUTOR_INVOCATIONS_PER_WORKSTREAM` | `N` | Prevents hidden executor retries. |
| `MAX_VERIFIER_INVOCATIONS_PER_WORKSTREAM` | `N + ceil(N / 3)` | Allows a bounded fresh second opinion or recheck without granting an extra executor revision. |
| `MAX_INTEGRATION_CYCLES` | `ceil(N / 2)` | Limits integrate → final-verifier rounds. |
| `MAX_EXECUTOR_TURNS_PER_INVOCATION` | `max(6, 2 * N)` | Bounds one executor invocation when the runtime supports role-specific turn limits. |
| `MAX_VERIFIER_TURNS_PER_INVOCATION` | `max(4, N)` | Bounds one verifier invocation when supported. |
| `MAX_ORCHESTRATOR_TURNS` | `max(10, 3 * N)` | Covers decomposition, budget tracking, integration, and terminal reporting. |
| `MAX_AGENT_TURNS` | `max(10, 3 * N)` | Use only when the runtime has one shared per-agent turn control instead of role-specific controls. |
| `MAX_DELEGATION_DEPTH` | `1` | Keeps the lead's direct executor/verifier delegation bounded; use `2` only with explicit task-specific justification. |
| `MAX_CONCURRENT_AGENTS` | `min(2 * W, 2 + ceil(N / 2))` | Allows independent work without unbounded parallelism. |
| `MAX_TOTAL_CYCLES` | `(W * N) + ceil(N / 2)` | Globally limits all local and integration cycles. |
| `MAX_TOTAL_AGENT_SPAWNS` | `W * (2 * N + ceil(N / 3)) + 2 * ceil(N / 2) + 1` | Covers every allowed executor/verifier invocation, integration/final verification, and the lead. |
| `MAX_WALL_CLOCK_MINUTES` | `max(30, 15 * N)` when a time limit is practical | Adds a global wall-clock boundary. |
| `AUTO_EXTEND` | `false` | Requires explicit human approval for any continuation. |

For example, a typical two-workstream task where the user chooses **up to 5 rounds** produces `N = 5`, `W = 2`, `MAX_WORKSTREAM_CYCLES = 5`, `MAX_VERIFIER_INVOCATIONS_PER_WORKSTREAM = 7`, `MAX_INTEGRATION_CYCLES = 3`, `MAX_TOTAL_CYCLES = 13`, and `MAX_TOTAL_AGENT_SPAWNS = 31`. The user only chose “up to 5 rounds”; the other values are engineering controls derived for the prompt.

Use real token, compute, or monetary ceilings only when the runtime exposes them and the user has authorized the applicable spending. Never invent a vendor limit or price. When wall-clock enforcement is unavailable, retain the semantic deadline in the prompt and require the orchestrator to stop at it.

## Runtime mapping

Use real runtime controls when present, but keep semantic caps in the generated prompt.

Examples:

- OpenAI Agents SDK exposes `max_turns`/`maxTurns`; exhaustion is an exception/termination condition, not a quality pass.
- Claude/Anthropic runtimes may expose turn, budget, depth, concurrency, or tool-iteration controls depending on product/version.
- For CLIs/runtimes without a verified native turn cap, enforce limits in the orchestrator/wrapper and via process/time/budget controls available in the environment.

Never invent a flag.

## Terminal semantics

- `PASS`: required evidence proves the bar.
- `FAIL`: current version fails and another permitted attempt remains.
- `CAPPED`: any hard safety ceiling was reached before `PASS`.
- `BLOCKED`: required access, dependency, environment, data, or approval is unavailable.
- `INCONCLUSIVE`: evidence/judging cannot support a stable verdict.
- `ESCALATE`: requirements/bar/strategy need reframing.
- `STOPPED`: human intentionally stopped the run.
