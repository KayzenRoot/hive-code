#!/usr/bin/env python3
from pathlib import Path


def replace_exact(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text()
    if old not in text:
        if new in text:
            return
        raise SystemExit(f"Expected source block not found in {path}")
    p.write_text(text.replace(old, new, 1))

# HC-AUD-005: a refresh failure must not destructively clear durable credentials.
replace_exact(
    "crates/goose/src/oauth/mod.rs",
    '''    let previously_granted_scopes = stored_credentials
        .as_ref()
        .map(|stored| stored.granted_scopes.clone())
        .unwrap_or_default();
''',
    '''    let previously_granted_scopes = stored_credentials
        .as_ref()
        .map(|stored| stored.granted_scopes.clone())
        .unwrap_or_default();
    let mut preserve_credentials_after_refresh_failure = false;
''',
)
replace_exact(
    "crates/goose/src/oauth/mod.rs",
    '''                Err(e) => {
                    warn!(
                        "[OAuth:{}] Token refresh failed: {} - clearing stored credentials and falling back to browser auth",
                        name, e
                    );
                }
''',
    '''                Err(e) => {
                    warn!(
                        "[OAuth:{}] Token refresh failed: {} - preserving stored credentials and falling back to browser auth for this session",
                        name, e
                    );
                    preserve_credentials_after_refresh_failure = true;
                }
''',
)
replace_exact(
    "crates/goose/src/oauth/mod.rs",
    '''        if let Err(e) = credential_store.clear().await {
            warn!("[OAuth:{}] error clearing bad credentials: {}", name, e);
        }
''',
    '''        if !preserve_credentials_after_refresh_failure {
            if let Err(e) = credential_store.clear().await {
                warn!("[OAuth:{}] error clearing bad credentials: {}", name, e);
            }
        }
''',
)
replace_exact(
    "crates/goose/src/oauth/mod.rs",
    '''    let mut preserve_credentials_after_refresh_failure = false;
    let mut preserve_credentials_after_refresh_failure = false;
''',
    '''    let mut preserve_credentials_after_refresh_failure = false;
''',
)

# HC-AUD-002: until child ActionRequired routing exists, never weaken an approval-requiring
# parent into an autonomous subagent. Refuse delegation instead of bypassing the policy.
replace_exact(
    "crates/goose/src/agents/platform_extensions/summon.rs",
    '''        if session.session_type == SessionType::SubAgent {
            return Err("Delegated tasks cannot spawn further delegations".to_string());
        }

        if params.r#async {
''',
    '''        if session.session_type == SessionType::SubAgent {
            return Err("Delegated tasks cannot spawn further delegations".to_string());
        }

        if session.goose_mode != GooseMode::Auto {
            return Err(
                "Delegation is disabled while the parent session requires tool approval; Hive Code will not weaken the parent approval policy for a subagent"
                    .to_string(),
            );
        }

        if params.r#async {
''',
)

# HC-AUD-003: provider-controlled approval IDs cannot be safely reused. Keep a lifetime
# tombstone set per agent/router and fail a reused ID closed rather than routing a delayed answer.
replace_exact(
    "crates/goose/src/agents/tool_confirmation_router.rs",
    "use std::collections::HashMap;",
    "use std::collections::{HashMap, HashSet};",
)
replace_exact(
    "crates/goose/src/agents/tool_confirmation_router.rs",
    '''pub(super) struct ToolConfirmationRouter {
    pending: Mutex<HashMap<(String, String), oneshot::Sender<PermissionConfirmation>>>,
}
''',
    '''pub(super) struct ToolConfirmationRouter {
    pending: Mutex<HashMap<(String, String), oneshot::Sender<PermissionConfirmation>>>,
    seen: Mutex<HashSet<(String, String)>>,
}
''',
)
replace_exact(
    "crates/goose/src/agents/tool_confirmation_router.rs",
    '''        Self {
            pending: Mutex::new(HashMap::new()),
        }
''',
    '''        Self {
            pending: Mutex::new(HashMap::new()),
            seen: Mutex::new(HashSet::new()),
        }
''',
)
replace_exact(
    "crates/goose/src/agents/tool_confirmation_router.rs",
    '''        let (tx, rx) = oneshot::channel();
        let mut pending = self.pending.lock().await;
        pending.retain(|_, sender| !sender.is_closed());
        pending.insert((session_id, request_id), tx);
        rx
''',
    '''        let key = (session_id, request_id);
        let (tx, rx) = oneshot::channel();

        if !self.seen.lock().await.insert(key.clone()) {
            warn!(
                session_id = %key.0,
                request_id = %key.1,
                "Rejected reused tool confirmation request id"
            );
            drop(tx);
            return rx;
        }

        let mut pending = self.pending.lock().await;
        pending.retain(|_, sender| !sender.is_closed());
        pending.insert(key, tx);
        rx
''',
)

p = Path("crates/goose/src/agents/tool_confirmation_router.rs")
text = p.read_text()
marker = "    #[tokio::test]\n    async fn test_concurrent_requests_out_of_order() {"
test = '''    #[tokio::test]
    async fn test_reused_request_id_is_rejected_even_after_cancellation() {
        let router = ToolConfirmationRouter::new();
        let first = router
            .register("session_1".to_string(), "req_1".to_string())
            .await;
        drop(first);

        let reused = router
            .register("session_1".to_string(), "req_1".to_string())
            .await;
        assert!(reused.await.is_err());
        assert!(
            !router
                .deliver("session_1", "req_1", test_confirmation())
                .await
        );
    }

'''
if test not in text:
    if marker not in text:
        raise SystemExit("Router test insertion marker not found")
    p.write_text(text.replace(marker, test + marker, 1))

print("wave 2 stabilization patches applied")
