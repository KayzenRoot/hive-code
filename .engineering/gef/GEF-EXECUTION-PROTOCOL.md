# GEF V1 Execution Protocol — HIVE CODE

Status: `GOVERNED_CANDIDATE`

## Pipeline
`REQUEST -> Source Drift Sentinel -> Task Class -> Context Radius -> UPIR/Task Manifest -> Decision Freeze Capsule -> Context Slice -> Patch Recipe -> Budgets -> SOURCE_MATCH -> bounded executor -> A0/A1/A2 -> one final publication -> A3 hosted gates + HEDS Delta -> exact-head verdict`

## Source Drift Sentinel
Before implementation, bind repository identity, authorized base/head, branch/PR, checkpoint identity, Work Order identity and material contracts. Drift causes `SOURCE_CONFLICT` or pack regeneration.

## Required Execution Pack
Every implementation/correction pack states:
1. project/repository/work order/branch/PR/base/head
2. task class, context radius, assurance level
3. `ACCEPTED_AND_FROZEN`
4. `OPEN_GOAL` or `ONLY_OPEN_FINDING`
5. resolved `ROOT_CAUSE / ENGINEERING_DECISION`
6. `PATCH_MAP` with allowed files/symbols
7. `PRESCRIBED_ALGORITHM` and postconditions
8. `FORBIDDEN_SHORTCUTS`
9. required positive/negative/regression/eval tests
10. search/files-opened/patch/retry/token-output budgets
11. A0-A2 local assurance
12. one-shot publication target
13. compact machine output
14. exact STOP condition

## SOURCE_MATCH
Mutation begins only when authorized base/head, branch, checkpoint, Work Order and relevant frozen sources still match; target paths/symbols exist or creation is explicitly authorized; no newer decision invalidates the recipe.

## Correction Pack defaults
Prefer `T1|T2`, `C0|C1`, 1–3 source files and 1–3 test files when compatible, small bounded search, causal retries only, and one final publication after local candidate completion.

## STOP states
- `COMPLETE_CANDIDATE`
- `SOURCE_CONFLICT`
- `SCOPE_EXPANSION_REQUIRED`
- `BLOCKED_EVIDENCE`
- `NEEDS_ARCHITECTURE`

A STOP state is not permission to explore or widen scope silently.

## Machine output
Prefer compact structured output containing changed files, tests/evals, exit codes, evidence digests/paths, remaining blockers, requested/applied model where exposed, budget overruns and final STOP state.
