# Hive Code Governance

Hive Code is a solo-maintainer project governed by `@KayzenRoot`.

## Authority

`@KayzenRoot` is the sole human maintainer, code owner, release authority and final decision-maker for Hive Code.

AI systems may assist with planning, coding, testing, review, documentation and repository operations under the maintainer's direction. They do not become independent human maintainers or contributors.

## Contribution model

Hive Code does not accept external implementation contributors, co-maintainers, unsolicited code contributions or shared code ownership by default.

External users may report bugs, suggest features, share references or participate in discussion when enabled, but those activities do not grant maintainer, contributor or authorship status in Hive Code governance.

## Development workflow

All governed implementation follows the local GEF V1 operational model under `.engineering/gef/`:

`REQUEST -> Source Drift Sentinel -> Task Class -> Context Radius -> UPIR/Task Manifest -> Decision Freeze Capsule -> Context Slice -> Patch Recipe -> Budgets -> SOURCE_MATCH -> bounded execution -> A0/A1/A2 -> publication -> A3 hosted gates + HEDS Delta -> exact-head verdict`

Semantic review independence is provided through evidence and review separation, not by requiring a second human maintainer.

## Decision making

- The canonical project Source Pack and Decisions Ledger define current project truth.
- Significant architecture, security, release or governance decisions are recorded before implementation.
- The maintainer may use AI-assisted analysis and independent semantic review, but final project authority remains with `@KayzenRoot`.
- No external vote, maintainer quorum or community consensus is required for project decisions.

## Code ownership

`.github/CODEOWNERS` must resolve project ownership to `@KayzenRoot` unless an explicit future governance decision changes the solo-maintainer model.

## Reviews and assurance

Hive Code retains professional review discipline despite having one human maintainer:

- exact-head evidence;
- fail-closed STOP states;
- A0-A4 assurance;
- HEDS Delta semantic review;
- security and architecture gates where applicable;
- no HIGH or CRITICAL unresolved defects at approval.

A second human reviewer is not a standing requirement.

## Upstream Goose provenance

Hive Code was bootstrapped from the Goose codebase. Historical Goose commits, authors and applicable attribution/licensing records are preserved as upstream provenance. Their presence in imported history does not make those authors current Hive Code maintainers or contributors to post-adoption Hive Code development.

Historical provenance must not be rewritten solely to make the contributor graph appear single-author unless a separate destructive migration is explicitly approved with licensing and traceability evidence.

## Governance changes

Changing the solo-maintainer model requires an explicit Decision Ledger entry approved by `@KayzenRoot` before CODEOWNERS, repository permissions, contribution rules or maintainer records are changed.

See `.engineering/SOLO-MAINTAINER-POLICY.md` for the canonical detailed policy.
