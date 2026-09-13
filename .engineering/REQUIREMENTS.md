# Requirements

## Governance requirements
- R-GOV-001: Every implementation increment must have a stable Work Order ID.
- R-GOV-002: Every increment must declare objective, context, scope, out-of-scope, sources, requirements, architecture rules, constraints, acceptance criteria, tests, deliverables, review format and stop condition.
- R-GOV-003: No next increment may start while the current increment is `CORRECTION REQUIRED` or `BLOCKED`.
- R-GOV-004: Checkpoint promotion occurs only after objective audit.
- R-GOV-005: Evidence must bind to exact Git base/head SHAs.
- R-GOV-006: Existing-project adoption must be preservation-first and non-destructive.

## Engineering requirements
- R-ENG-001: Code, tests and Git evidence are authoritative over unsupported documentation claims.
- R-ENG-002: Architecture changes require explicit scope and evidence.
- R-ENG-003: HIGH/CRITICAL known defects block advancement.
- R-ENG-004: Cleanup must not be mixed with process adoption unless strictly necessary.

## Hive Code bootstrap requirements
- R-HC-001: Preserve the imported Goose baseline until subsystem audit classifies changes.
- R-HC-002: Product rebranding must be a separate governed increment.
- R-HC-003: CI/CD restoration must be Hive Code-specific, not a blind copy of excluded Goose workflows.