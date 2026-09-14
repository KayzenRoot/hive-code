# Stabilization Security Note — RUSTSEC-2023-0071

Status: ACCEPTED WITH CONSTRAINTS
Owner: @KayzenRoot
Work Order: HIVECODE-WO-0002C

Hive Code inherits `rsa 0.9.x` through the `jsonwebtoken/rust_crypto` backend used by the optional `native-tls` feature. The portable `rustls-tls` path uses `jsonwebtoken/aws_lc_rs` instead.

The directly identified private-key operation is GCP service-account RS256 JWT signing in `crates/goose/src/providers/gcpauth.rs`. The current path signs an outbound authentication assertion using a locally held service-account key; it is not an RSA decryption service accepting attacker-selected ciphertext.

`RUSTSEC-2023-0071` has no patched release in the affected rsa line. Removing native-tls/GCP compatibility solely to clear the scanner would introduce a compatibility regression without evidence that Hive Code currently exposes the adaptive remote private-key oracle required by the advisory's threat model.

Therefore the existing `deny.toml` exception remains accepted for the current dependency graph. The exception expires and must be revisited if any of the following occurs:

- `rsa`, `jsonwebtoken`, TLS backend, or GCP authentication dependencies change;
- Hive Code exposes remotely observable RSA private-key operations to attacker-controlled inputs;
- a safe patched/migrated dependency path becomes available;
- the default/production distribution changes to a backend that makes `jsonwebtoken/rust_crypto` the primary path.

CI must use the version-controlled advisory policy in `deny.toml` through `cargo deny check advisories`. The advisory must remain visible in source control; it must not be silently removed or duplicated as an opaque workflow-only ignore.
