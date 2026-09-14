# Hive Code Development Guide

Hive Code is a **solo-maintainer project** built by `@KayzenRoot` with AI-assisted engineering.

External implementation contributions, co-maintainer roles, shared code ownership and unsolicited pull requests are not accepted by default. The repository may remain publicly readable, but its development model is intentionally closed and governed.

## Development authority

- Sole human maintainer: `@KayzenRoot`
- Code owner: `@KayzenRoot`
- AI assistance: permitted under maintainer direction
- Engineering governance: operational GEF V1
- Canonical engineering state: `.engineering/`

Historical Goose authors remain visible in imported Git history as upstream provenance. That history does not represent the current Hive Code development team.

## Work model

Every governed increment should follow:

`ANALYZE → SOURCE CHECK → WORK ORDER → CONTEXT LOCK → SOURCE_MATCH → BOUNDED EXECUTION → TESTS/EVIDENCE → PR → HEDS DELTA AUDIT → CHECKPOINT → MERGE`

A change should not begin without a bounded Work Order when it affects product behavior, architecture, packaging, release infrastructure, security, persistence, protocols or compatibility surfaces.

## Current compatibility state

Hive Code is being transformed from an imported Goose baseline. Many technical identifiers still intentionally use inherited `goose` names.

Do not perform global renames. In particular, do not rename without a dedicated compatibility Work Order:

- the inherited CLI executable
- Rust crates and workspace dependency keys
- persistent paths such as `.config/goose` or `.local/share/goose`
- environment variables
- protocol identifiers
- package coordinates
- updater/release identifiers

User-facing branding can migrate independently when it does not alter these contracts.

## Local development setup

The inherited workspace currently uses Rust, Electron/Node and Hermit tooling.

Activate Hermit:

```bash
source bin/activate-hermit
```

Build Rust workspace:

```bash
cargo build
```

Run formatting and linting:

```bash
cargo fmt
cargo clippy --all-targets -- -D warnings
```

Run tests:

```bash
cargo test
```

Run desktop development UI:

```bash
just run-ui
```

During the compatibility period, the inherited CLI remains available under its current executable name:

```bash
./target/debug/goose --help
```

This does **not** mean Goose is the current product brand. It is a temporary technical compatibility surface tracked by Hive Code's branding migration plan.

## Engineering rules

- Keep changes within the active Work Order patch map.
- Do not silently widen scope.
- Prefer deterministic tooling before LLM exploration.
- Preserve exact-head evidence for governed approval.
- Do not convert UNKNOWN into PASS/ALLOW.
- Do not merge with unresolved HIGH or CRITICAL findings.
- Preserve applicable Apache 2.0 attribution and historical provenance.
- Do not rewrite imported history merely to remove upstream authors.
- Do not replace final visual assets until the UGAS branding increment is authorized.

## AI-generated work

AI-generated changes are reviewed as engineering output, not trusted because of their source. They must satisfy the same architecture, testing, security, evidence and review requirements as any other change.

## Upstream provenance

Hive Code is derived from the imported Goose codebase. The original project and historical sources may still appear in changelogs, licenses, compatibility code and imported history. Such references should remain when they are legally, historically or technically necessary.

For current Hive Code project governance, see:

- `GOVERNANCE.md`
- `.engineering/SOLO-MAINTAINER-POLICY.md`
- `.engineering/BRANDING-IDENTITY.md`
- `.engineering/BRANDING-INVENTORY.md`
- `.engineering/gef/`
