# GEF V1 Local Policy — HIVE CODE

Status: `GOVERNED_CANDIDATE`

## Authority
GEF is an optimization/governance layer. Hive Code canonical source priority remains:

`CHECKPOINT > DECISIONS/ADRs > SCOPE > DEFINITION OF DONE > ARCHITECTURE > REQUIREMENTS > remaining canonical sources > chat prose`.

When GEF conflicts with a newer or higher-authority Hive Code source, record `SOURCE_CONFLICT`, preserve canonical truth and stop for reconciliation.

## Global rules
- Think once, compile once, execute narrowly, prove incrementally, review only what changed.
- Deterministic tools before LLM calls when practical.
- Start with the smallest safe context radius and expand only for a concrete dependency or source conflict.
- Executor claims are staged until validated by evidence.
- Exact-head proof is mandatory for governed approval.
- `UNKNOWN` never becomes ALLOW, PASS, HIT, zero, exact usage or exact cost.
- Git remains canonical source-code history.
- No GEF cache, summary, receipt or derived artifact replaces canonical source.
- Existing Goose-derived architecture is preserved until a governed Work Order authorizes change.

## Task classes
- `T0`: mechanical change, no architectural exploration.
- `T1`: bounded patch with prescribed recipe and minimal search.
- `T2`: semantic correction within frozen architecture.
- `T3`: architecture work with explicitly governed broad analysis.

## Context radius
- `C0`: target symbol/function + direct test.
- `C1`: target symbols + direct dependencies + tests.
- `C2`: module + interfaces.
- `C3`: related architecture + cross-module contracts.
- `C4`: broad project architecture.

## Assurance
- `A0`: syntax/static/basic local checks.
- `A1`: focused local tests.
- `A2`: impacted local tests/evals.
- `A3`: hosted CI/security/platform/release gates.
- `A4`: HEDS independent semantic assurance.

## Budgets
Every Execution Pack or Correction Pack declares search budget, files-opened budget, patch files/LOC budget, retry budget and output discipline. Budgets are guardrails, not permission to truncate correctness. Material overrun triggers a STOP state.

## Hive Code overrides
1. No executor may widen the active Work Order or checkpoint authorization ceiling.
2. Rebranding, inherited-code removal, dependency migration and architectural replacement require explicit Work Orders.
3. Apache-2.0 provenance/license obligations from the Goose baseline must remain auditable.
4. Upstream Goose workflow absence is not permission to invent or weaken CI; Hive Code CI is governed separately.
5. Product code is not modified by process-adoption increments unless explicitly scoped.

## Forbidden shortcuts
- `UNKNOWN -> ALLOW`
- fabricated test/gate/proof/reviewer/receipt data
- old-head evidence represented as exact-head proof
- silent scope expansion
- full-repository search by default
- asking the executor to rediscover frozen architecture
- repeated identical retry without causal change
- evidence-only source commit after exact-head receipts
- merge before required review/gates
- deleting governance to simplify GEF
- treating optimization targets as measured gains
- proof carry-forward without validity-input checks
