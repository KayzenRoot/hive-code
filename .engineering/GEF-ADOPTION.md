# GEF V1 Adoption Record

Status: `CORRECTED_TO_OPERATIONAL_GEF_V1`
Mode: `EXISTING_PROJECT/BROWNFIELD`
Canonical operational contract: `.engineering/gef/`

## Correction
The first adoption pass incorrectly treated the separately evolving `KayzenRoot/gef-bootstrap` project as the GEF implementation source. That interpretation is superseded.

Hive Code adopts the **operational GEF V1 model already used by `KayzenRoot/hive` and `KayzenRoot/hive-crypto-trader`**.

## Operational GEF V1 core
- Source Drift Sentinel
- Task classes `T0-T3`
- Context Radius `C0-C4`
- UPIR/Task Manifest
- Decision Freeze Capsule
- Context Slice
- Patch Recipe
- explicit budgets
- `SOURCE_MATCH`
- bounded executor
- A0/A1/A2 local assurance
- A3 hosted gates
- A4/HEDS Delta semantic assurance
- exact-head evidence
- delta-first review
- Shadow Assurance
- fail-closed STOP states

## Relationship with GEF Bootstrap
`KayzenRoot/gef-bootstrap` is a separate future bootstrap/productization effort. It may later generate or evolve GEF installations, but it is **not** the operational contract source for Hive Code today.

## Project adaptation
Hive Code keeps its own canonical Source Pack and project-specific overrides. Rules unique to HIVE infrastructure or HCT trading/live-operation constraints are not copied unless they independently apply here.
