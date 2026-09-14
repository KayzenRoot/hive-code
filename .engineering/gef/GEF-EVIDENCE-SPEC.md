# GEF V1 Machine Evidence Specification — HIVE CODE

Status: `GOVERNED_CANDIDATE`

## Principle
Evidence is exact-head, machine-auditable and scoped to the authorized increment. Executor prose is never sufficient by itself.

## Minimum receipt fields
- repository
- workOrder
- branch/pr
- baseSha
- headSha
- taskClass
- contextRadius
- assuranceLevel
- changedPaths
- tests with command/result/exit code
- evidence/proof identifiers and validity fingerprints
- required hosted gates and receipts
- unresolved blockers/findings
- requested/applied model when exposed
- final STOP/verdict

## Assurance ladder
`A0 -> A1 -> A2 -> A3 -> A4`.

## Proof states
- `FRESH`
- `CARRY_FORWARD`
- `INVALIDATED`
- `UNKNOWN`
- `BLOCKED_EVIDENCE`

`CARRY_FORWARD` requires compatible dependency fingerprints. UNKNOWN cannot be converted to PASS.

## Exact-head invariant
A receipt produced for another source head is historical. Any source change after evidence production invalidates exact-head status for the new head unless the affected proof is independently and explicitly shown reusable under the current validity rules.

## Storage
Prefer GitHub checks, workflow artifacts, PR comments or equivalent external receipts for run IDs and hosted results. Keep source-controlled evidence only when it describes stable policy/schema rather than ephemeral run state.
