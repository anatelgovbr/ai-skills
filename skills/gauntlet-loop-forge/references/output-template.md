# Final Prompt Assembly Skeleton

A compact assembly aid, not text to copy verbatim.

## Core skeleton

1. **Mission:** build, produce, or achieve `[MISSION]` using `[SOURCE OF TRUTH]`.
2. **Constraints:** preserve `[HARD CONSTRAINTS]` and stay inside scope. `[FORBIDDEN ACTIONS]` are off limits.
3. **Bar:** the quality bar is `[BAR]`. Obtain and inspect the real bar or measurement before judging.
4. **Acceptance:** success requires `[ACCEPTANCE CRITERIA]` and `[HARD GATES]`.
5. **Lead autonomy:** the lead chooses architecture and approach and splits the mission into the smallest independently judgeable workstreams.
6. **Role split:** each material workstream gets an executor and a separate fresh verifier. The verifier sees the real current artifact and its evidence, never the executor's self-assessment.
7. **Cycle:** the executor revises, produces direct evidence, and a fresh verifier decides against the assigned criteria and bar. On failure it returns the blocking findings, the largest remaining gap, and the next acceptance check, and the next cycle starts from those.
8. **Bounded safety:** apply the exact `[SAFETY ENVELOPE]`. Stop early on `PASS`, treat any exhausted ceiling as `CAPPED`, never auto-extend.
9. **Integration:** assemble the locally passing pieces, inspect interfaces and consistency, run the global gates, and use a fresh final verifier within the integration budget.
10. **Human gates:** require explicit approval for `[HUMAN-GATED ACTIONS]`.
11. **Ledger:** maintain `[OBSERVABILITY ARTIFACT]` with evidence, remaining budget, findings, and status.
12. **Statuses:** use `PASS`, `FAIL`, `INCONCLUSIVE`, `ESCALATE`, `BLOCKED`, `CAPPED`, and `STOPPED` honestly, and never convert a non-`PASS` state into `PASS` because the run ended.

The safety envelope carries the derived integers themselves, with the formulas and the internal limit names left behind in the forge.

## Conditional software clauses

Include only when the software profile is active and the clause is relevant:

- "For behavior-changing work, use a bounded TDD micro-loop: define the next behavior, prove a focused test fails for the expected reason when feasible, implement the smallest coherent change to make it pass, refactor while green, then run the broader relevant regression and integration gates."
- "A verifier must confirm that the tests meaningfully represent the acceptance behavior, that they were not weakened to obtain green, and that the actual current code and runtime pass the relevant functional, contract, reliability, security, performance, migration, and compatibility gates."
- "For bug fixes, prefer a pre-fix regression test. For refactors and legacy work, establish characterization tests before risky structural change. Use task-appropriate alternatives when strict red-first TDD is not meaningful."

Select the risk-relevant gates from the software references, and carry only those into the final prompt.
