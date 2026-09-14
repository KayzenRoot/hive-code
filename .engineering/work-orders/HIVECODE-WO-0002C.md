# HIVECODE-WO-0002C — Whole-System Stabilization

MODE: CORRECT / VERIFY
TASK_CLASS: T3
CONTEXT_RADIUS: C4
ASSURANCE: A0-A4
STATUS: CORRECTION_REQUIRED

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

## Corrections applied so far
- `HC-AUD-001` PARTIAL FIX: recipe security scanning now flags stdio extensions and retry shell surfaces, with regression tests.
- `HC-AUD-002` FAIL-CLOSED MITIGATION: delegation is refused when the parent session requires approval, instead of silently weakening the child to autonomous mode.
- `HC-AUD-003` PARTIAL FAIL-CLOSED MITIGATION: generic tool-confirmation IDs are tombstoned for the lifetime of the router so delayed approvals cannot be routed to a later invocation reusing the same provider-controlled ID.
- `HC-AUD-005` FIX CANDIDATE: OAuth refresh failure preserves durable stored credentials while the current session may fall back to browser authorization. A duplicate temporary declaration introduced during patch application was removed before this validation checkpoint.
- `HC-AUD-006` FIX CANDIDATE: ACP load-session reload includes messages before pending-confirmation/state-machine-resume evaluation.
- `HC-AUD-009` FIX CANDIDATE: thinking-only provider output is treated as unproductive and enters the bounded empty-turn retry path; Hive-generated fallback text is not replayed to the model.
- `HC-AUD-011` FIX CANDIDATE: a provider-less restored agent cannot enter the LRU cache; saved-provider restore errors remain retryable on later loads.
- Wave 0 CI added: Rust format/check/clippy/tests, Desktop typecheck/unit/lint and Rust dependency audit.

## Evidence state
- Initial CI proved checkout/toolchain setup, Desktop dependency installation and Desktop typecheck are operational.
- A formatting failure introduced by the first patch was detected by the new gate and the applicator was changed to run `cargo fmt --all` before commit.
- Long Rust workspace jobs have also experienced external workflow cancellation; those cancellations are not classified as source failures.
- A bot-authored correction checkpoint produced GitHub `action_required` without jobs; this maintainer-authored checkpoint exists to trigger normal exact-head CI validation.
- `HC-AUD-004` duplicate-side-effect protection remains unresolved: current state-machine execution still dispatches a tool before its durable response is applied. The correction requires a persisted invocation identity / execution-lease design rather than an unsafe boolean marker.
- Final status remains `CORRECTION_REQUIRED` until every known HIGH/CRITICAL item is resolved or explicitly proven inapplicable.

## STOP conditions
- `BLOCKED_EVIDENCE` if automated validation cannot be established.
- `CORRECTION_REQUIRED` while any known HIGH/CRITICAL defect remains unresolved.
- `READY_FOR_PRODUCTION_AUDIT` only after all required waves complete and exact-head evidence passes.
