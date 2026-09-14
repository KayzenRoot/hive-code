# GEF V1 HEDS Delta Review Protocol — HIVE CODE

Status: `GOVERNED_CANDIDATE`
Review mode: `HEDS_DELTA`

## Pipeline
`ANALYZE DELTA -> SOURCE CHECK -> INVALIDATED PROOFS -> SEMANTIC REVIEW -> GATE RECEIPTS -> EXACT-HEAD VERDICT`

## First candidate
The first candidate of an increment may receive the broad review necessary to establish its semantic baseline, architecture boundary, evidence model and mandatory gate set.

## Subsequent candidates
Review delta-first:
1. lock exact base/head;
2. compare last reviewed head with current exact head;
3. identify changed files/symbols and material toolchain/policy changes;
4. carry forward only proofs whose complete dependency fingerprints remain compatible;
5. invalidate affected proofs;
6. inspect semantic delta and newly invalidated areas;
7. combine with current exact-head receipts;
8. issue governed verdict.

Accepted findings are not reopened without a new invalidating delta.

## Evidence Validity Fingerprint
May include source/blob or symbol hashes, tests/evals, schema/contracts, toolchain/lockfiles, workflow/config/policy, OS/platform, canonical checkpoint/authorization identity and provider/runtime identity when material. Matching test names alone are insufficient.

## Exact-head rule
- HEDS may begin while CI runs.
- Final approval waits for mandatory exact-head A3 gates.
- Old-head evidence is historical only.
- Gate receipts should live outside source HEAD when possible.
- Do not create evidence-only source commits merely to store run IDs.

## Verdicts
- `APPROVED`
- `CORRECTION REQUIRED`
- `BLOCKED`

For HIGH_ASSURANCE work, approval requires unresolved CRITICAL=0 and HIGH=0 plus every required exact-head receipt.

## Shadow Assurance
Starts `ON`. Carry-forward/recommended impacted tests are informational until separately promoted by measured evidence. Required hosted gates are not skipped merely because GEF predicts proof reuse.
