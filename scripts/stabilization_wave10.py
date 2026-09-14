#!/usr/bin/env python3
from pathlib import Path


def replace_exact(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text()
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"Expected source block not found in {path}")
    p.write_text(text.replace(old, new, 1))

# Preserve the distinction between a missing secret and an unavailable/corrupt credential store.
replace_exact(
    "crates/goose/src/oauth/persist.rs",
    "use crate::config::Config;\n",
    "use crate::config::{Config, ConfigError};\n",
)
replace_exact(
    "crates/goose/src/oauth/persist.rs",
    '''        match config.get_secret::<PersistedCredentials>(&key) {
            Ok(credentials) => Ok(Some(credentials)),
            Err(_) => Ok(None),
        }
''',
    '''        match config.get_secret::<PersistedCredentials>(&key) {
            Ok(credentials) => Ok(Some(credentials)),
            Err(ConfigError::NotFound(_)) => Ok(None),
            Err(error) => Err(AuthError::CredentialStoreError(format!(
                "Failed to load persisted OAuth credentials: {error}"
            ))),
        }
''',
)

# Helpers keep refresh-failure policy explicit and independently testable.
replace_exact(
    "crates/goose/src/oauth/mod.rs",
    '''const OAUTH_CALLBACK_TIMEOUT_ENV: &str = "GOOSE_OAUTH_CALLBACK_TIMEOUT_SECONDS";
''',
    '''const OAUTH_CALLBACK_TIMEOUT_ENV: &str = "GOOSE_OAUTH_CALLBACK_TIMEOUT_SECONDS";

fn refresh_failure_definitively_rejects_credentials(error: &AuthError) -> bool {
    matches!(error, AuthError::TokenRefreshRejected(_))
}

fn stored_credentials_unchanged(
    before: &StoredCredentials,
    current: &StoredCredentials,
) -> bool {
    match (serde_json::to_value(before), serde_json::to_value(current)) {
        (Ok(before), Ok(current)) => before == current,
        _ => false,
    }
}
''',
)

replace_exact(
    "crates/goose/src/oauth/mod.rs",
    "    let mut preserve_credentials_after_refresh_failure = false;\n",
    "    let mut clear_stored_credentials = true;\n",
)

replace_exact(
    "crates/goose/src/oauth/mod.rs",
    '''                Err(e) => {
                    warn!(
                        "[OAuth:{}] Token refresh failed: {} - preserving stored credentials and falling back to browser auth for this session",
                        name, e
                    );
                    preserve_credentials_after_refresh_failure = true;
                }
''',
    '''                Err(error) => {
                    if refresh_failure_definitively_rejects_credentials(&error) {
                        clear_stored_credentials = match credential_store.load().await {
                            Ok(Some(current)) => {
                                stored_credentials_unchanged(stored_credentials, &current)
                            }
                            Ok(None) => false,
                            Err(load_error) => {
                                warn!(
                                    "[OAuth:{}] could not re-read credentials after definitive refresh rejection: {} - preserving store fail-closed",
                                    name, load_error
                                );
                                false
                            }
                        };
                        if clear_stored_credentials {
                            warn!(
                                "[OAuth:{}] refresh token was definitively rejected and the persisted credential is unchanged; clearing it before browser reauthorization: {}",
                                name, error
                            );
                        } else {
                            warn!(
                                "[OAuth:{}] refresh token was rejected, but persisted credentials changed or became unavailable; preserving the current store to avoid deleting a concurrent refresh winner: {}",
                                name, error
                            );
                        }
                    } else {
                        clear_stored_credentials = false;
                        warn!(
                            "[OAuth:{}] token refresh failed without definitive credential rejection; preserving durable credentials and falling back to browser auth for this session: {}",
                            name, error
                        );
                    }
                }
''',
)

replace_exact(
    "crates/goose/src/oauth/mod.rs",
    '''        if !preserve_credentials_after_refresh_failure {
            if let Err(e) = credential_store.clear().await {
                warn!("[OAuth:{}] error clearing bad credentials: {}", name, e);
            }
        }
''',
    '''        if clear_stored_credentials {
            if let Err(e) = credential_store.clear().await {
                warn!("[OAuth:{}] error clearing bad credentials: {}", name, e);
            }
        }
''',
)

# Add focused policy regression tests to the existing OAuth test module.
p = Path("crates/goose/src/oauth/mod.rs")
text = p.read_text()
marker = '''    #[tokio::test]
    async fn wait_for_callback_times_out_with_authorization_url() {'''
tests = '''    #[test]
    fn refresh_failure_only_clears_on_definitive_rejection() {
        assert!(refresh_failure_definitively_rejects_credentials(
            &AuthError::TokenRefreshRejected("invalid_grant".to_string())
        ));
        assert!(!refresh_failure_definitively_rejects_credentials(
            &AuthError::TokenRefreshFailed("temporarily_unavailable".to_string())
        ));
        assert!(!refresh_failure_definitively_rejects_credentials(
            &AuthError::AuthorizationRequired
        ));
    }

    #[test]
    fn credential_snapshot_comparison_detects_concurrent_rotation() {
        let original = StoredCredentials::new(
            "client-id".to_string(),
            None,
            vec!["scope.read".to_string()],
            Some(100),
        );
        let same = original.clone();
        let rotated = StoredCredentials::new(
            "client-id".to_string(),
            None,
            vec!["scope.read".to_string()],
            Some(101),
        );

        assert!(stored_credentials_unchanged(&original, &same));
        assert!(!stored_credentials_unchanged(&original, &rotated));
    }

'''
if tests not in text:
    if marker not in text:
        raise SystemExit("OAuth test insertion marker not found")
    p.write_text(text.replace(marker, tests + marker, 1))

print("wave 10 OAuth credential-safety correction applied")
