use std::collections::{HashMap, HashSet};

use tokio::sync::{oneshot, Mutex};
use tracing::warn;

use crate::permission::PermissionConfirmation;

const MAX_SEEN_CONFIRMATION_IDS: usize = 8_192;

pub(super) struct ToolConfirmationRouter {
    pending: Mutex<HashMap<(String, String), oneshot::Sender<PermissionConfirmation>>>,
    seen: Mutex<HashSet<(String, String)>>,
    max_seen_confirmation_ids: usize,
}

impl ToolConfirmationRouter {
    pub(super) fn new() -> Self {
        Self::with_max_seen_confirmation_ids(MAX_SEEN_CONFIRMATION_IDS)
    }

    fn with_max_seen_confirmation_ids(max_seen_confirmation_ids: usize) -> Self {
        Self {
            pending: Mutex::new(HashMap::new()),
            seen: Mutex::new(HashSet::new()),
            max_seen_confirmation_ids,
        }
    }

    pub(super) async fn register(
        &self,
        session_id: String,
        request_id: String,
    ) -> oneshot::Receiver<PermissionConfirmation> {
        let key = (session_id, request_id);
        let (tx, rx) = oneshot::channel();

        let mut seen = self.seen.lock().await;
        if seen.contains(&key) {
            warn!(
                session_id = %key.0,
                request_id = %key.1,
                "Rejected reused tool confirmation request id"
            );
            drop(tx);
            return rx;
        }

        if seen.len() >= self.max_seen_confirmation_ids {
            warn!(
                session_id = %key.0,
                request_id = %key.1,
                max_seen_confirmation_ids = self.max_seen_confirmation_ids,
                "Rejected tool confirmation request because anti-replay tombstone capacity was reached"
            );
            drop(tx);
            return rx;
        }

        seen.insert(key.clone());
        drop(seen);

        let mut pending = self.pending.lock().await;
        pending.retain(|_, sender| !sender.is_closed());
        pending.insert(key, tx);
        rx
    }

    pub(super) async fn deliver(
        &self,
        session_id: &str,
        request_id: &str,
        confirmation: PermissionConfirmation,
    ) -> bool {
        let key = (session_id.to_string(), request_id.to_string());
        if let Some(tx) = self.pending.lock().await.remove(&key) {
            if tx.send(confirmation).is_err() {
                warn!(
                    request_id = %request_id,
                    "Confirmation receiver was dropped (task cancelled)"
                );
                false
            } else {
                true
            }
        } else {
            false
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::permission::permission_confirmation::PrincipalType;
    use crate::permission::Permission;

    fn test_confirmation() -> PermissionConfirmation {
        PermissionConfirmation {
            principal_type: PrincipalType::Tool,
            permission: Permission::AllowOnce,
        }
    }

    #[tokio::test]
    async fn test_register_then_deliver() {
        let router = ToolConfirmationRouter::new();
        let rx = router
            .register("session_1".to_string(), "req_1".to_string())
            .await;
        assert!(
            router
                .deliver("session_1", "req_1", test_confirmation())
                .await
        );
        let confirmation = rx.await.unwrap();
        assert_eq!(confirmation.permission, Permission::AllowOnce);
    }

    #[tokio::test]
    async fn test_deliver_unknown_request() {
        let router = ToolConfirmationRouter::new();
        assert!(
            !router
                .deliver("session_1", "unknown", test_confirmation())
                .await
        );
    }

    #[tokio::test]
    async fn test_request_cannot_be_delivered_from_another_session() {
        let router = ToolConfirmationRouter::new();
        let _rx = router
            .register("session_1".to_string(), "req_1".to_string())
            .await;

        assert!(
            !router
                .deliver("session_2", "req_1", test_confirmation())
                .await
        );
        assert_eq!(router.pending.lock().await.len(), 1);
    }

    #[tokio::test]
    async fn test_cancelled_receiver() {
        let router = ToolConfirmationRouter::new();
        let rx = router
            .register("session_1".to_string(), "req_1".to_string())
            .await;
        drop(rx); // simulate task cancellation
        assert!(
            !router
                .deliver("session_1", "req_1", test_confirmation())
                .await
        );
    }

    #[tokio::test]
    async fn test_stale_entries_pruned_on_register() {
        let router = ToolConfirmationRouter::new();
        let rx = router
            .register("session_1".to_string(), "req_1".to_string())
            .await;
        drop(rx); // simulate task cancellation — entry is now stale

        assert_eq!(router.pending.lock().await.len(), 1);

        let _rx2 = router
            .register("session_1".to_string(), "req_2".to_string())
            .await;
        assert_eq!(router.pending.lock().await.len(), 1); // only req_2 remains
        assert!(router
            .pending
            .lock()
            .await
            .contains_key(&("session_1".to_string(), "req_2".to_string())));
    }

    #[tokio::test]
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

    #[tokio::test]
    async fn test_tombstone_capacity_fails_closed_without_reopening_old_ids() {
        let router = ToolConfirmationRouter::with_max_seen_confirmation_ids(2);

        let first = router
            .register("session_1".to_string(), "req_1".to_string())
            .await;
        drop(first);
        let second = router
            .register("session_1".to_string(), "req_2".to_string())
            .await;
        drop(second);

        let over_capacity = router
            .register("session_1".to_string(), "req_3".to_string())
            .await;
        assert!(over_capacity.await.is_err());
        assert!(
            !router
                .deliver("session_1", "req_3", test_confirmation())
                .await
        );

        let reused = router
            .register("session_1".to_string(), "req_1".to_string())
            .await;
        assert!(reused.await.is_err());
        assert_eq!(router.seen.lock().await.len(), 2);
    }

    #[tokio::test]
    async fn test_concurrent_requests_out_of_order() {
        use std::sync::Arc;

        let router = Arc::new(ToolConfirmationRouter::new());

        // Register two requests
        let rx1 = router
            .register("session_1".to_string(), "req_1".to_string())
            .await;
        let rx2 = router
            .register("session_1".to_string(), "req_2".to_string())
            .await;

        // Deliver in reverse order
        assert!(
            router
                .deliver(
                    "session_1",
                    "req_2",
                    PermissionConfirmation {
                        principal_type: PrincipalType::Tool,
                        permission: Permission::DenyOnce,
                    }
                )
                .await
        );
        assert_eq!(router.pending.lock().await.len(), 1);
        assert!(
            router
                .deliver("session_1", "req_1", test_confirmation())
                .await
        );
        assert_eq!(router.pending.lock().await.len(), 0);

        let c1 = rx1.await.unwrap();
        assert_eq!(c1.permission, Permission::AllowOnce);
        let c2 = rx2.await.unwrap();
        assert_eq!(c2.permission, Permission::DenyOnce);
    }
}
