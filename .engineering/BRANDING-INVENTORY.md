# Hive Code — Branding Inventory and Migration Matrix

Status: `READY_FOR_REVIEW`
Work Order: `HIVECODE-WO-0002`
Base: `4c715ce0ebe8636b18294d521450bdda829449a2`

## Objective

Map inherited Goose identity before mutation, classify every branding surface by migration risk, and define the safe order for rebranding Hive Code without breaking compatibility or violating provenance obligations.

## Evidence sampled

Repository search confirms Goose branding in:

- `README.md` and root project documentation
- `GOVERNANCE.md`, `CONTRIBUTING.md`, `AGENTS.md`, release/build documentation
- `documentation/**` guides, tutorials, architecture pages, static content and icon components
- `ui/desktop/package.json` (`name: goose-app`, `productName: Goose`, `description: Goose App`)
- desktop/UI icon components such as `ui/desktop/src/components/icons/Goose.tsx`
- documentation icon components such as `documentation/src/components/icons/goose.tsx`
- `ui/goose-acp/**` package/bin naming
- Rust crates and paths under `crates/goose*`
- shell scripts and persistent paths such as `~/.local/share/goose`
- Docker labels and upstream source/vendor metadata
- release/update links pointing to `aaif-goose/goose`
- changelogs and package coordinates that encode upstream history

## Classification

### A — REBRAND NOW / LOW RISK
User-facing identity that can change without renaming executable or persistence contracts:

- README product title and descriptive copy
- current-project governance copy
- current-project maintainer wording
- non-historical documentation headings and descriptions
- desktop `productName` and human-readable description, after package/build review
- Docker human-readable title/description/vendor/source metadata when publishing Hive Code images
- current-project repository links
- About/product-name surfaces

### B — REBRAND WITH BUILD/RELEASE VALIDATION / MEDIUM RISK

- installer/display names
- updater repository coordinates
- package metadata
- Linux desktop templates
- release scripts
- Docker image coordinates
- documentation site metadata
- bundle/display names
- generated artifacts and installer filenames

These require A0-A3 validation because packaging/updater code may depend on names.

### C — COMPATIBILITY MIGRATION / HIGH RISK

Do not mass-replace:

- CLI executable `goose`
- Rust crate names `goose`, `goose-*`
- workspace dependency keys
- module/type identifiers containing Goose
- persistent directories such as `~/.config/goose` and `~/.local/share/goose`
- environment variable names
- protocol/integration identifiers
- `ui/goose-acp`
- package coordinates consumed by external tools

Target state may use Hive Code identifiers, but migration requires aliases, compatibility reads, deprecation windows or explicit breakage approval.

### D — PRESERVE AS PROVENANCE / DO NOT REWRITE AS CURRENT BRAND

- `LICENSE`
- applicable copyright and attribution notices
- applicable `NOTICE` content if present/required
- imported commit authorship
- historical changelog links and release references when they describe upstream releases
- factual references needed to document origin or compatibility

## Visual assets

Status: `UGAS_PENDING`

The following are intentionally deferred until UGAS is installed:

- final logo
- application icon sets
- favicons
- splash art
- installer artwork
- README/social hero graphics
- documentation logo variants

Temporary rule: prefer text-first Hive Code identity. Do not promote inherited Goose icons as permanent Hive Code assets.

## Recommended migration sequence

1. Freeze brand identity and provenance rules.
2. Replace current-project governance/README/community identity.
3. Replace safe user-facing product strings and repository URLs.
4. Validate desktop/package/distribution metadata.
5. Establish Hive Code release/update coordinates.
6. Introduce CLI/data-path compatibility strategy.
7. Rename internal packages/crates only when dependency graph and external API impact are proven.
8. Generate and integrate final UGAS visual assets.
9. Run final repository-wide Goose-reference audit and classify remaining occurrences as provenance, compatibility debt or defect.

## Non-goals for this inventory increment

- no blind `goose -> hive` global replacement
- no crate rename
- no CLI rename
- no data migration
- no icon/logo generation
- no removal of required upstream attribution
- no history rewrite

## Acceptance

The inventory is complete enough to authorize bounded branding Work Orders only when every changed surface is assigned a risk class and the next change does not mix low-risk visual/text branding with high-risk compatibility renames.