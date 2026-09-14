# HIVECODE-WO-0001C — Correct GEF V1 Operational Adoption

Status: `READY_FOR_AUDIT`
Type: `CORRECTION`
Task class: `T2`
Context radius: `C2`
Assurance: `A2 + A4 review`

## Objective
Replace the incorrect `gef-bootstrap` interpretation from WO-0001 with the operational GEF V1 model already used by HIVE and Hive Crypto Trader, adapted to Hive Code.

## Context
- Repository: `KayzenRoot/hive-code`
- Base branch: `main`
- Authorized base SHA: `60a4e476b95aff80918f110630e422701f360897`
- Correction branch: `hivecode/wo-0001c-operational-gef`
- Project mode: `EXISTING_PROJECT/BROWNFIELD`

## Scope
- Install `.engineering/gef/` operational contracts.
- Correct `.engineering/GEF-ADOPTION.md`.
- Record corrected decisions.
- Add project-specific machine-readable current/baseline/profile/test-impact state.
- Preserve Source Pack from WO-0001 where compatible.

## Out of scope
- Product code changes.
- Goose-to-Hive Code rebranding.
- Dependency upgrades.
- CI/CD implementation beyond documenting the future governed requirement.
- Product architecture replacement.

## Reference sources
- `KayzenRoot/hive/.engineering/gef/`
- `KayzenRoot/hive-crypto-trader/docs/gef/`

## Acceptance criteria
1. Operational GEF V1 pipeline is present locally.
2. Task classes T0-T3, Context Radius C0-C4 and A0-A4 assurance are defined.
3. SOURCE_MATCH, exact-head evidence, HEDS Delta, Shadow Assurance and STOP states are defined.
4. Project-specific overrides do not import HCT trading rules or HIVE infrastructure assumptions blindly.
5. No product-code file changes.
6. Historical incorrect adoption is explicitly superseded, not silently hidden.

## STOP CONDITION
`READY_FOR_HIVECODE_WO_0001C_AUDIT`
