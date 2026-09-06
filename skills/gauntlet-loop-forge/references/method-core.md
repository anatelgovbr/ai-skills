# Gauntlet Loop Method Core

Use this reference to preserve the method while adapting it to different domains and bounded execution.

## Canonical invariants

1. Give the lead agent the **goal**, not a prematurely dictated implementation.
2. Give it a **real bar** the agent can inspect or measure.
3. Let the lead split the mission into the smallest parts that can be improved and judged independently.
4. Separate **builder/executor** from **critic/verifier**; use fresh context for the critic where the harness supports it.
5. The critic inspects the **real artifact**, not the builder's summary.
6. When the artifact loses against the bar, identify the **largest meaningful remaining gap** and iterate.
7. Use a live progress/evidence artifact for long work.
8. Run an optional integration/smoothing review when separately optimized pieces may conflict.

## Bounded adaptation

The original method rejects an arbitrary round count as a **definition of done**. That does not require infinite execution.

This Skill separates two questions:

- **Did quality pass?** Determined only by evidence and the quality bar.
- **May the system continue spending effort?** Determined by a finite safety envelope.

Therefore:

- stop early on `PASS`;
- if a hard limit is exhausted first, stop as `CAPPED`;
- never report a cap as quality success;
- only explicit human approval may establish a new continuation budget.

This preserves the method's quality logic while preventing uncontrolled execution.

## Source lineage

Primary method:
- Matt Shumer, “How to Run a Gauntlet Loop”, Something Big Is Happening, 2026: https://somethingbig.ai/gauntlet-loop
- Official prompt generator: https://somethingbig.ai/gauntlet-loop/generator

Community implementations studied:
- RoboNuggets / Jay E: https://github.com/robonuggets/gauntlet-loop
- Nicholas Spisak: https://github.com/NicholasSpisak/gauntlet-loop

The Skill intentionally synthesizes the method rather than copying either community Skill verbatim.
