# Hive Code Engineering Source Hierarchy

This directory is the canonical Source Pack for Hive Code.

## Authority order
1. `CHECKPOINT.md`
2. `DECISIONS-LEDGER.md` / approved ADRs
3. `SCOPE.md`
4. `DEFINITION-OF-DONE.md`
5. `ARCHITECTURE.md`
6. `REQUIREMENTS.md`
7. remaining canonical sources
8. code, tests and Git evidence override unsupported prose claims

## Operating model
Hive Code adopts GEF V1 as its prompt/review engineering model. This repository is an `EXISTING_PROJECT/BROWNFIELD` adoption because the Goose codebase was imported before GEF governance was installed.

Flow: ANALYZE -> SOURCE CHECK -> NEXT NECESSARY INCREMENT -> WORK ORDER -> CONTEXT LOCK -> PREFLIGHT -> EXECUTOR -> TESTS/EVIDENCE -> PR -> AUDIT -> APPROVED / CORRECTION REQUIRED / BLOCKED -> CHECKPOINT DELTA -> MERGE -> NEXT.

No source may claim implementation that is not evidenced by code/tests/Git.