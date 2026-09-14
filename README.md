<div align="center">

# Hive Code

**AI-native software construction, governed by evidence.**

A desktop, CLI and API foundation for building software with AI agents, tools, context and engineering controls working together.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

</div>

## What is Hive Code?

Hive Code is an AI-native coding and software-construction platform being developed by `@KayzenRoot` with AI-assisted engineering.

The project starts from the imported Goose codebase and is being progressively transformed into an independent Hive product through governed, preservation-first Work Orders. The objective is not a cosmetic fork. Hive Code will evolve its own product identity, engineering workflow, integrations and capabilities while preserving required upstream attribution and compatibility where necessary.

### Current foundation

The inherited platform already provides a strong technical base:

- native desktop application
- terminal/CLI workflows
- embeddable API surfaces
- Rust-based core
- multi-provider LLM support
- ACP/MCP integrations
- agent/tool execution infrastructure

Hive Code layers its own governed construction model on top of that baseline, including the operational **GEF V1** workflow, exact-head evidence, bounded execution, HEDS Delta review and project-specific engineering controls.

## Project status

Hive Code is currently in **brownfield transformation**.

The repository is usable as an engineering baseline, but branding, packaging, release infrastructure and internal technical identifiers are being migrated in controlled phases.

### Branding status

| Surface | Status |
| --- | --- |
| Product name | **Hive Code** |
| Repository identity | **Hive Code** |
| Governance | **Hive Code** |
| User-facing documentation | Migration in progress |
| Desktop display name | Planned validation phase |
| CLI executable | Compatibility name `goose` retained temporarily |
| Rust crates / internal package IDs | Compatibility migration pending |
| Final logo / icons / splash | **UGAS_PENDING** |

The final visual identity will be produced with UGAS after it is installed. Until then, Hive Code intentionally uses text-first branding instead of promoting inherited Goose artwork as its permanent identity.

## Governance

Hive Code uses a **solo-maintainer model**.

- Sole human maintainer and code owner: `@KayzenRoot`
- External implementation contributors: not accepted by default
- AI assistance: allowed under maintainer direction
- Engineering model: operational GEF V1
- Canonical engineering sources: `.engineering/`

See [GOVERNANCE.md](GOVERNANCE.md) and [.engineering/SOLO-MAINTAINER-POLICY.md](.engineering/SOLO-MAINTAINER-POLICY.md).

## Development compatibility note

During the migration period, many inherited technical identifiers still use `goose`. This is intentional.

For example, the current CLI binary and several Rust crates still use Goose-derived names. These identifiers are compatibility surfaces and will only be migrated after dependency, installer, updater, protocol and persistent-data impacts are validated. A blind repository-wide rename is explicitly forbidden by Hive Code governance.

## Engineering workflow

Hive Code development follows the governed flow:

`ANALYZE → SOURCE CHECK → WORK ORDER → CONTEXT LOCK → SOURCE_MATCH → BOUNDED EXECUTION → TESTS/EVIDENCE → PR → HEDS DELTA AUDIT → CHECKPOINT → MERGE`

Important engineering documents live in `.engineering/`, including:

- brand identity and migration inventory
- architecture and scope
- security and test plans
- Definition of Done
- Decisions Ledger
- Work Orders
- GEF V1 contracts

## Upstream provenance

Hive Code is derived from the open-source **Goose** project originally imported from `aaif-goose/goose`.

The imported source history, applicable copyright notices and Apache License 2.0 obligations are preserved. References to Goose, AAIF, Block and upstream authors in historical or legally relevant material describe provenance only and do not represent the current Hive Code maintainer team or product branding.

Hive Code is not presented as an AAIF, Block or Goose-maintainer product or endorsement.

## License

The inherited codebase is distributed under the [Apache License 2.0](LICENSE), subject to applicable attribution and notice requirements.

---

**Hive Code**

Built as a governed evolution of an agentic development foundation, with one goal: make AI-assisted software construction faster, more reliable, auditable and increasingly autonomous.
