# Decisions Ledger

## HC-D-0001 — Hive Code adopts GEF V1
Status: APPROVED

Hive Code uses GEF V1 as the default prompt/review engineering and governed-construction model. Changes to this decision require an explicit ADR/ledger entry.

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