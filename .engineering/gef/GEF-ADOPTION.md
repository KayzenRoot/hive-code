# GEF V1 Operational Adoption — HIVE CODE

Status: `GOVERNED_CANDIDATE`
Mode: `EXISTING_PROJECT/BROWNFIELD`
GEF version: `1.0`

## Reference implementations
Hive Code adopts the operational GEF V1 pattern already used by `KayzenRoot/hive` and `KayzenRoot/hive-crypto-trader`, not the separately evolving `gef-bootstrap` project.

## Adopted core
- Source Drift Sentinel
- Task classes `T0-T3`
- Context Radius `C0-C4`
- UPIR/Task Manifest
- Decision Freeze Capsule
- Context Slice
- Patch Recipe
- explicit budgets
- `SOURCE_MATCH`
- bounded execution
- A0/A1/A2 local assurance
- A3 hosted gates
- A4/HEDS Delta semantic assurance
- exact-head evidence
- delta-first review
- Shadow Assurance
- STOP-state fail-closed behavior

## Hive Code adaptation
Project-specific rules live in `GEF-POLICY.md` and canonical `.engineering/` sources. Rules specific to HIVE infrastructure or HCT trading/live credentials are not imported unless independently applicable to Hive Code.

## Adoption constraints
- GEF is an optimization/governance layer, not canonical product truth.
- Current Goose-derived code remains authoritative implementation evidence until changed under a Work Order.
- Adoption itself does not authorize rebranding or product-code mutation.
- Proof reuse remains shadow-only until promoted by measured evidence.

## Correction note
The earlier `.engineering/GEF-ADOPTION.md` referenced `gef-bootstrap`; this correction supersedes that interpretation. The operational source is this `.engineering/gef/` contract set.
