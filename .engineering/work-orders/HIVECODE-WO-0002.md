# HIVECODE-WO-0002 — Branding Inventory and Identity Freeze

MODE: ANALYZE / GOVERN
TASK_CLASS: T2
CONTEXT_RADIUS: C2
ASSURANCE: A0-A1 documentation/governance

## Project
Hive Code — `KayzenRoot/hive-code`

## Authorized base
`4c715ce0ebe8636b18294d521450bdda829449a2`

## Objective
Establish Hive Code's canonical brand identity, inventory inherited Goose branding surfaces, classify migration risk, preserve legal/provenance obligations, and define the safe migration order before product-code branding changes.

## Accepted and frozen
- Official product name: `Hive Code`.
- Sole human maintainer: `@KayzenRoot`.
- Goose is upstream technical provenance, not current product identity.
- Final visual assets will be created/integrated later through UGAS.
- No history rewrite.
- No removal of legally applicable Apache 2.0 attribution.

## Open goal
Produce an auditable branding migration map that separates low-risk user-facing rebranding from package/CLI/data-path compatibility migration.

## Patch map
Allowed:
- `.engineering/BRANDING-IDENTITY.md`
- `.engineering/BRANDING-INVENTORY.md`
- `.engineering/DECISIONS-LEDGER.md`
- `.engineering/CHECKPOINT.md`
- `.engineering/BACKLOG.md`
- `.engineering/work-orders/HIVECODE-WO-0002.md`

Forbidden:
- product source code
- package/crate renames
- CLI rename
- persistent data path migration
- binary/image asset replacement
- LICENSE deletion/rewrite that removes upstream obligations

## Evidence
- repository code search for `goose`
- repository code search for `aaif-goose`
- desktop `productName` discovery
- package/bundle identifier discovery
- Apache 2.0 redistribution/trademark requirements review

## STOP
`READY_FOR_HIVECODE_WO_0002_AUDIT`