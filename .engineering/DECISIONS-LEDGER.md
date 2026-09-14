# Decisions Ledger

## HC-D-0001 — Hive Code adopts GEF V1
Status: APPROVED — CORRECTED SOURCE

Hive Code uses the operational GEF V1 model already deployed in `KayzenRoot/hive` and `KayzenRoot/hive-crypto-trader` as its default prompt/review engineering and governed-construction model. `KayzenRoot/gef-bootstrap` is not the current operational source.

## HC-D-0002 — Brownfield adoption
Status: APPROVED

Hive Code is treated as `EXISTING_PROJECT/BROWNFIELD` because the Goose baseline predates GEF installation. Adoption is preservation-first, incremental and non-destructive.

## HC-D-0003 — Imported Goose baseline is evidence, not product identity
Status: APPROVED

The Goose codebase is the technical baseline. Hive Code branding, architecture divergence and feature replacement require separate governed increments.

## HC-D-0004 — Upstream workflows are not copied blindly
Status: APPROVED

The Goose `.github/workflows` set was excluded during repository bootstrap due token permission constraints. Hive Code will define CI/CD intentionally under its own requirements instead of treating missing upstream workflows as an implementation defect.

## HC-D-0005 — No broad cleanup during process adoption
Status: APPROVED

GEF adoption may not be combined with broad inherited-code cleanup. Dead-code removal requires later classification and evidence.

## HC-D-0006 — Operational GEF contract path
Status: APPROVED

The canonical local GEF contract is `.engineering/gef/`. It contains the project-adapted policy, execution protocol, review protocol, evidence specification and machine-readable state. Operational invariants are derived from the common GEF V1 pattern used in HIVE and Hive Crypto Trader; project-specific overrides remain local.

## HC-D-0007 — Shadow Assurance starts ON
Status: APPROVED

Proof carry-forward and impacted-test recommendations may be calculated, but they do not skip required hosted gates until separately promoted by measured evidence.

## HC-D-0008 — Solo maintainer construction model
Status: APPROVED

`@KayzenRoot` is the sole human maintainer and project builder for Hive Code. The project does not accept external contributors, co-maintainers, shared code ownership or unsolicited implementation PRs by default. AI assistance may support construction, review and repository operations under `@KayzenRoot` direction without creating an independent maintainer/contributor role.

Historical Goose commit authors are preserved only as upstream provenance and attribution evidence. Their appearance in imported Git history does not confer current Hive Code maintainer or contributor status. Rewriting imported history solely to remove historical authors is forbidden unless separately authorized as a destructive migration with licensing and traceability evidence.
