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

## HC-D-0009 — Hive Code is the canonical product brand
Status: APPROVED

The official product name is `Hive Code`. Goose is upstream technical provenance and a temporary compatibility identifier where inherited technical surfaces still require it. User-facing current-project identity should migrate to Hive Code unless a compatibility, legal or historical reason requires the Goose reference.

## HC-D-0010 — Branding migration is layered, not global replacement
Status: APPROVED

Branding changes are classified into: low-risk user-facing identity, medium-risk packaging/distribution identity, high-risk executable/package/data-path compatibility, and preserved provenance. A repository-wide blind `goose -> hive` replacement is forbidden.

## HC-D-0011 — Final visual assets are delegated to UGAS
Status: APPROVED

Final Hive Code logo/icon/splash/favicons/installer and social/README artwork are `UGAS_PENDING`. Text-first and neutral temporary branding may proceed now. UGAS availability does not block naming, documentation, distribution planning or compatibility engineering.