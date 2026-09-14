# Hive Code Solo Maintainer Policy

Status: `APPROVED_POLICY_CANDIDATE`

## Human maintainer
`@KayzenRoot` is the sole human maintainer and project builder for Hive Code.

## Contribution model
Hive Code does not accept external contributors, co-maintainers, unsolicited implementation PRs, or shared ownership by default.

External people may report issues, suggest ideas, or provide references when explicitly invited, but such participation does not grant contributor, maintainer, code-owner, or authorship status in Hive Code.

## AI assistance
AI systems may assist with planning, analysis, code generation, review, testing, documentation, and repository operations under KayzenRoot's direction. This assistance does not create an independent human contributor or maintainer role in repository governance.

## Upstream provenance
Hive Code is derived from the Goose codebase. Historical commits and authors imported from Goose are preserved as upstream provenance and license/history evidence. Their presence in Git history does not mean they are current Hive Code maintainers or contributors to Hive Code development after the adoption baseline.

The imported history must not be rewritten merely to remove historical contributor names unless an explicit future destructive-history migration is separately authorized and proven compatible with licensing, attribution, traceability, release, and upstream-sync requirements.

## Ownership rules
- `.github/CODEOWNERS` must designate only `@KayzenRoot` unless this policy is explicitly superseded.
- New project commits, PRs, releases, architectural decisions, and governance changes are controlled by `@KayzenRoot`.
- No external reviewer approval is required as a human-identity requirement. Semantic review may still be performed by automated/AI assurance under GEF.
- No external account may receive write/maintain/admin ownership as part of the normal construction model.
- External pull requests are not part of the accepted construction path.

## GEF interpretation
GEF independent semantic assurance means independence of review reasoning/evidence, not a requirement for a second human contributor. The project remains solo-maintainer while preserving fail-closed review, exact-head evidence, A0-A4 assurance, and HEDS Delta semantics.

## Exception rule
Any future change from solo-maintainer status requires an explicit decision record approved by `@KayzenRoot` before repository permissions, CODEOWNERS, or contribution policy are changed.
