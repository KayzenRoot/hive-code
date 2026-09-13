# Architecture

## Baseline state
Hive Code currently inherits the Goose application architecture. This document does not yet redefine that architecture; it governs how divergence is approved.

## Architecture rules
1. Audit before replacement.
2. Preserve working subsystem boundaries until evidence justifies change.
3. Prefer incremental adapters and seams over big-bang rewrites.
4. New Hive Code modules must have explicit ownership, contracts and failure boundaries.
5. Cross-cutting changes require regression evidence for affected CLI, desktop, API and shared/core surfaces where applicable.
6. No architecture claim becomes canonical without code/Git evidence.

## Brownfield normalization stages
`B0 DISCOVER -> B1 MAP -> B2 ALIAS -> B3 BASELINE -> B4 SHADOW -> B5 PROMOTE -> B6 NORMALIZE`.

Hive Code is currently at `B3 BASELINE` for repository import and `B0/B1` for subsystem-level architectural classification.

## Next architecture deliverable
A subsystem map classifying inherited Goose areas as `KEEP`, `MODIFY`, `REPLACE`, `REMOVE` or `UNKNOWN`, with evidence and dependency boundaries.