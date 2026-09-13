# HIVECODE-WO-0001 — Install GEF V1 Governance Baseline

## OBJECTIVE
Install Hive Code's canonical Source Pack and the currently approved GEF V1 construction/governance model without modifying product behavior.

## CONTEXT
Hive Code imported the Goose codebase before GEF governance existed in this repository. Treat as brownfield.

## SCOPE
- Create canonical engineering Source Pack.
- Record GEF V1 adoption.
- Record baseline, source hierarchy, decisions, DoD and Context Lock.
- Establish backlog and next legal increment.

## OUT OF SCOPE
- Product code changes.
- Rebranding.
- Dependency upgrades.
- CI/CD implementation.
- Cleanup or dead-code removal.

## FILES/SOURCES TO READ
- `.engineering/*` created by this Work Order.
- `README.md`, `AGENTS.md`, root build manifests from imported baseline.
- `KayzenRoot/gef-bootstrap` approved M00-M07 canonical contracts.

## REQUIREMENTS
R-GOV-001..006, R-ENG-001..004, R-HC-001..003.

## ARCHITECTURE RULES
Preservation-first brownfield adoption. No inherited subsystem rewrite in this increment.

## CONSTRAINTS
No force-push. No destructive history rewrite. No unverified implementation claims.

## ACCEPTANCE CRITERIA
1. Required Source Pack files exist on the WO branch.
2. Brownfield mode and GEF adoption are explicit.
3. Base SHA and source fingerprints are recorded.
4. No product code changes are included.
5. PR can be audited against exact changed-file list.
6. Next work is limited to baseline/subsystem audit after approval.

## TESTS
- Git changed-file audit.
- Verify files are documentation/governance only.
- Validate canonical hierarchy consistency.
- Validate Context Lock base SHA against repository baseline.

## DELIVERABLES
Source Pack, adoption record, Context Lock, Decisions Ledger, DoD, Backlog, Checkpoint and PR evidence.

## REVIEW FORMAT
Verdict: `APPROVED`, `CORRECTION REQUIRED`, or `BLOCKED`, with findings by severity and exact evidence.

## STOP CONDITION
`READY_FOR_HIVECODE_WO_0001_AUDIT`.