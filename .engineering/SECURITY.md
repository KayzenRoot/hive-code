# Security

## Current posture
The imported Goose baseline has not yet received a Hive Code-specific security audit. No stronger claim is made.

## Mandatory rules
- Never commit secrets, credentials, private keys or tokens.
- Treat provider credentials, shell execution, local filesystem access, extension/tool execution and network access as trust boundaries.
- Privileged or irreversible operations require explicit safeguards and rollback/roll-forward strategy.
- Dependency and supply-chain changes require review before promotion.
- Security-relevant inherited behavior must be preserved until intentionally changed under a governed Work Order.

## Risk model
Default risk: `STANDARD`.
Escalate to `HIGH_ASSURANCE` for privileged authentication, signing, money/trading, critical security controls or irreversible actions.

## Required future evidence
Threat model, secret scan, dependency audit, permission/tool execution audit and security-focused regression plan before a production release.