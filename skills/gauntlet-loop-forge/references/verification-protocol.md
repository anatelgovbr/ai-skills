# Evidence-First Verification Protocol

## Evidence packet

A verifier evaluates the actual current artifact/version. Give it only the context required to judge fairly:

- mission and assigned acceptance criteria;
- applicable quality bar/reference;
- hard constraints;
- artifact/version locator or actual artifact;
- direct measurements, test results, rendered output, traces, source evidence, calculations, or other task-appropriate proof;
- comparison conditions.

Do not provide the executor's self-assessment, effort narrative, excuses, or hidden reasoning.

## Evaluation order

Prefer this order:

1. verify evidence corresponds to the current artifact;
2. evaluate mandatory deterministic/hard gates;
3. inspect domain-specific failure modes and side effects;
4. evaluate non-functional/quality dimensions;
5. use rubric/reference/pairwise judging only for dimensions not already settled objectively;
6. return the verdict and next acceptance check.

One failed mandatory hard gate prevents `PASS`.

## Failure contract

On failure, return:

- `VERDICT`;
- criterion-by-criterion evidence or missing evidence;
- blocking deficiencies;
- single highest-impact remaining gap;
- objective acceptance check for the next revision;
- non-blocking residual risks if material.

The verifier may diagnose failure but should not become the implementation owner.

## Pairwise / LLM-as-judge protocol

Use pairwise comparison only when it adds signal.

When possible:

1. mask candidate identity/provenance;
2. present candidate and reference under equivalent conditions;
3. judge A vs B;
4. swap positions and judge again;
5. accept the content-level verdict only if it is consistent across orders;
6. if the winner flips, return `INCONCLUSIVE` and use stronger evidence or another fresh judge.

A tie is acceptable only when the configured bar allows non-inferiority.

## Freshness

Prefer a fresh verifier for materially revised candidates when the harness supports separate contexts. At minimum, a verifier must not inherit the executor's self-justification.

Multiple verifiers are not automatically independent merely because there are several. Diversity of context, model/protocol, or evidence is more useful than duplicated rubber-stamping.

## Whole-artifact verification

After local workstreams converge, evaluate the integrated whole for cross-boundary defects, inconsistencies, regressions, and global acceptance criteria. Local passes do not imply global pass.
