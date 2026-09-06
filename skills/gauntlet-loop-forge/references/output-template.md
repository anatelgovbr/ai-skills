# Final Prompt Assembly Skeleton

Use this as a compact assembly aid, not text that must be copied verbatim.

## Core skeleton

1. **Mission** — Build/produce/achieve `[MISSION]` using `[SOURCE OF TRUTH]`.
2. **Constraints** — Preserve `[HARD CONSTRAINTS]`; do not do `[OUT OF SCOPE / FORBIDDEN ACTIONS]`.
3. **Bar** — The quality bar is `[BAR]`; obtain/inspect the real bar or measurement before judging.
4. **Acceptance** — Success requires `[ACCEPTANCE CRITERIA]` and `[HARD GATES]`.
5. **Lead autonomy** — The lead chooses architecture/approach and splits the mission into the smallest independently judgeable workstreams.
6. **Role split** — Each material workstream gets an executor and a separate fresh verifier; the verifier sees the real current artifact/evidence, not the executor's self-assessment.
7. **Cycle** — Executor revises → produces direct evidence → verifier decides against assigned criteria/bar → on failure returns the largest remaining gap and next acceptance check.
8. **Bounded safety** — Apply the exact `[SAFETY ENVELOPE]`; stop early on `PASS`; hitting a ceiling is `CAPPED`; never auto-extend.
9. **Integration** — Assemble locally passing pieces, inspect interfaces/consistency, run global gates, and use a fresh final verifier within the integration budget.
10. **Human gates** — Require explicit approval for `[HUMAN-GATED ACTIONS]`.
11. **Ledger** — Maintain `[OBSERVABILITY ARTIFACT]` with evidence, remaining budget, findings, and status.
12. **Terminal semantics** — Use `PASS`, `FAIL`, `INCONCLUSIVE`, `ESCALATE`, `BLOCKED`, `CAPPED`, and `STOPPED` honestly.

## Conditional software clauses

Include only when software specialization is active and relevant:

- “For behavior-changing work, use a bounded TDD micro-loop: define the next behavior, prove a focused test fails for the expected reason when feasible, implement the smallest coherent change to make it pass, refactor while green, then run the broader relevant regression/integration gates.”
- “A verifier must confirm tests meaningfully represent acceptance behavior, were not weakened to obtain green, and that the actual current code/runtime passes the relevant functional, contract, reliability, security, performance, migration, or compatibility gates.”
- “For bug fixes, prefer a pre-fix regression test; for refactors/legacy work, establish characterization tests before risky structural change; use task-appropriate alternatives when strict red-first TDD is not meaningful.”

Do not paste every test type into the final prompt. Select the risk-relevant gates from the software references.
