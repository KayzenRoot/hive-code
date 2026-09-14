# Hive Code Agent Instructions

Hive Code is an AI-native software-construction platform derived from an imported Goose technical baseline. The current product identity is **Hive Code**. Inherited `goose` identifiers remain where they are technical compatibility surfaces.

## Authority

- Sole human maintainer/code owner: `@KayzenRoot`.
- Canonical project governance: `.engineering/`.
- Operational engineering model: `.engineering/gef/`.
- External implementation contributors are not accepted by default.
- AI agents operate under maintainer direction and do not become independent contributors or maintainers.

## Governed workflow

Use the active Work Order and current checkpoint as the source of authorized scope.

`ANALYZE → SOURCE CHECK → WORK ORDER → CONTEXT LOCK → SOURCE_MATCH → BOUNDED EXECUTION → TESTS/EVIDENCE → PR → HEDS DELTA AUDIT → CHECKPOINT → MERGE`

Before mutation:

- confirm repository, branch, base/head and active Work Order;
- read accepted/frozen decisions and current checkpoint;
- stay inside the authorized patch map;
- stop on source conflict, scope-expansion need, blocked evidence or architecture uncertainty;
- do not silently broaden context or scope.

## Branding migration rule

Do not perform a global `goose -> hive` rename.

Current product-facing copy should use **Hive Code** unless a Goose reference is required for provenance, historical accuracy or compatibility.

The following inherited identifiers are compatibility-sensitive and require dedicated Work Orders before renaming:

- CLI executable `goose`
- Rust crates under `crates/goose*`
- workspace dependency keys
- persistent user data/config paths
- `GOOSE_*` environment variables
- protocol/integration identifiers
- package coordinates and updater/release identities
- `ui/goose-acp`

Final logo/icon/splash/favicons and related visual assets are `UGAS_PENDING`.

## Upstream provenance

Preserve applicable Apache 2.0 license/copyright/notice obligations and factual historical references. Imported Goose authorship is upstream provenance, not current Hive Code team membership.

## Setup

```bash
source bin/activate-hermit
cargo build
```

## Commands

### Build
```bash
cargo build
cargo build --release
just release-binary
```

### Test
```bash
cargo test
cargo test -p goose
cargo test --package goose --test mcp_integration_test
just record-mcp-tests
```

### Lint / format
```bash
cargo fmt
cargo clippy --all-targets -- -D warnings
```

### UI
```bash
just run-ui
cd ui/desktop && pnpm run typecheck
cd ui/desktop && pnpm test
```

## Structure

```text
crates/       Rust workspace members
ui/desktop/   Electron desktop app
ui/text/      deprecated inherited ACP TUI
.engineering/ Hive Code canonical governance and GEF contracts
```

## Development rules

- Prefer tests in the established test locations.
- Use `anyhow::Result` where consistent with the inherited architecture.
- Provider implementations follow the established Provider trait/contracts.
- MCP extensions live under the inherited MCP architecture until separately migrated.
- Desktop UI should use ACP SDK or local types as already governed by the codebase.
- Prefer self-documenting code and comments that explain why, not what.
- Do not add defensive optionality solely to silence the compiler.
- Keep `Cargo.lock` consistent with dependency changes.
- Never overwrite a live executable in place; use unlink/atomic replacement where required by platform behavior.

## Evidence rules

- Executor claims are staged until tests/evidence validate them.
- Old-head evidence is historical, not exact-head proof.
- UNKNOWN never becomes PASS/ALLOW/HIT by assumption.
- HIGH or CRITICAL unresolved findings block advancement.
- Proof carry-forward requires compatible Evidence Validity Fingerprints.

## Important entry points

These names remain inherited compatibility identifiers for now:

- CLI: `crates/goose-cli/src/main.rs`
- UI: `ui/desktop/src/main.ts`
- Agent: `crates/goose/src/agents/agent.rs`

Do not rename them solely for branding without an explicit technical migration Work Order.
