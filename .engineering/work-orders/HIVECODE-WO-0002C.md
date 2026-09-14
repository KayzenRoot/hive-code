# HIVECODE-WO-0002C — Whole-System Stabilization

MODE: CORRECT / VERIFY
TASK_CLASS: T3
CONTEXT_RADIUS: C4
ASSURANCE: A0-A4

## Project
Hive Code — `KayzenRoot/hive-code`

## Authorized base
`ce3bd218b3fd7f74e3bc304136a9e34b24305ccf`

## Objective
Stabilize the inherited Goose codebase before further branding or feature work. Correct every defect that can be safely fixed and verified from this repository, with priority on security boundaries, side-effect safety, sessions, OAuth, providers, protocols, build reliability, UI correctness and CI.

## Frozen decisions
- Branding/package migration is paused while stabilization is active.
- No blind refactors or global rename work.
- No HIGH/CRITICAL defect may be knowingly carried into a production-ready verdict.
- A claim of production readiness requires automated build/test evidence and exact-head audit.
- Historical upstream provenance remains intact.

## Waves
1. Wave 0 — repository/build gates and reproducible validation.
2. Wave 1 — security and side-effect correctness.
3. Wave 2 — sessions, cancellation, state machine and OAuth reliability.
4. Wave 3 — providers, MCP/ACP and model capability correctness.
5. Wave 4 — UI, performance, portability and remaining medium/low defects.
6. Wave 5 — full regression audit and production-readiness decision.

## Initial critical/high targets
- Recipe executable-surface trust/consent boundary.
- Subagent approval-policy inheritance and routing.
- Tool invocation identity and duplicate-side-effect prevention.
- OAuth refresh credential preservation.
- ACP load-session pending-confirmation correctness.
- Cancelled-turn session integrity.
- Unproductive thinking-only turn handling.
- Provider restore cache poisoning.
- MCP protocol downgrade/compatibility behavior.
- Streaming inactivity handling.
- Tool-result ordering / provider formatting integrity.
- Mandatory CI and exact-head evidence.

## STOP conditions
- `BLOCKED_EVIDENCE` if automated validation cannot be established.
- `CORRECTION_REQUIRED` while any known HIGH/CRITICAL defect remains unresolved.
- `READY_FOR_PRODUCTION_AUDIT` only after all required waves complete and exact-head evidence passes.
