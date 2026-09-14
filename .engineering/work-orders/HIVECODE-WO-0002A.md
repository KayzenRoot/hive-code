# HIVECODE-WO-0002A — Safe User-Facing Branding Migration

MODE: IMPLEMENT
TASK_CLASS: T1
CONTEXT_RADIUS: C1
ASSURANCE: A0-A1 documentation

## Base
`f3ed1eabc8e45400a6452072a08a51c3abe3d130`

## Objective
Replace inherited current-project Goose identity in low-risk root-facing documentation with canonical Hive Code branding while preserving technical compatibility identifiers and upstream provenance.

## Allowed paths
- `README.md`
- `CONTRIBUTING.md`
- `AGENTS.md`
- `.engineering/CHECKPOINT.md`
- `.engineering/work-orders/HIVECODE-WO-0002A.md`

## Frozen constraints
- Product name is `Hive Code`.
- `@KayzenRoot` remains sole human maintainer/code owner.
- Final visual assets remain `UGAS_PENDING`.
- Do not rename CLI executable, crates, packages, data paths, env vars, protocol IDs or release coordinates.
- Do not remove required Apache 2.0 provenance.
- Do not rewrite Git history.

## Acceptance
- Root README presents Hive Code, not Goose, as current product.
- Contribution/development guidance matches solo-maintainer governance.
- Agent instructions use Hive Code project identity while retaining inherited technical identifiers where required.
- No product source or compatibility contract changes.

## STOP
`READY_FOR_HIVECODE_WO_0002A_AUDIT`