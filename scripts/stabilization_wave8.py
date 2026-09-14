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

stream_cap = r'''//! Wall-clock cap for one provider response.
//!
//! Byte/read timeouts are reset by SSE keepalive bytes. A provider or gateway can therefore
//! remain connected forever while producing no useful model response. This cap bounds the
//! complete lifetime of a single provider response without imposing a short event-level timeout.

use std::time::Duration;

use async_stream::try_stream;
use futures::StreamExt;

use crate::base::MessageStream;
use crate::errors::ProviderError;

pub const DEFAULT_STREAM_MAX_DURATION_SECS: u64 = 900;

/// Maximum wall-clock duration of one provider response.
/// `GOOSE_STREAM_MAX_DURATION=0` disables the cap for compatibility/debugging.
pub fn stream_max_duration() -> Option<Duration> {
    let secs = std::env::var("GOOSE_STREAM_MAX_DURATION")
        .ok()
        .and_then(|value| value.parse::<u64>().ok())
        .unwrap_or(DEFAULT_STREAM_MAX_DURATION_SECS);
    (secs > 0).then(|| Duration::from_secs(secs))
}

/// Cap a provider response unless the provider owns its entire context/session lifecycle.
pub fn cap_stream_duration(stream: MessageStream, manages_own_context: bool) -> MessageStream {
    if manages_own_context {
        return stream;
    }
    let Some(max_duration) = stream_max_duration() else {
        return stream;
    };
    let Some(deadline) = tokio::time::Instant::now().checked_add(max_duration) else {
        return stream;
    };

    Box::pin(try_stream! {
        let mut stream = stream;
        loop {
            match tokio::time::timeout_at(deadline, stream.next()).await {
                Ok(Some(item)) => yield item?,
                Ok(None) => break,
                Err(_) => {
                    Err(ProviderError::RequestFailed(format!(
                        "Provider response exceeded the maximum duration of {}s without completing. The upstream model or gateway may be stalled behind keepalive traffic. Increase GOOSE_STREAM_MAX_DURATION (seconds, 0 to disable) only when a single healthy response legitimately needs longer.",
                        max_duration.as_secs()
                    )))?;
                }
            }
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::conversation::message::Message;
    use crate::retry::{should_retry, RetryConfig};
    use futures::stream;

    fn text_item() -> Result<
        (
            Option<Message>,
            Option<crate::conversation::token_usage::ProviderUsage>,
        ),
        ProviderError,
    > {
        Ok((Some(Message::assistant().with_text("a")), None))
    }

    #[test]
    fn stream_max_duration_parses_env() {
        {
            let _guard = env_lock::lock_env([("GOOSE_STREAM_MAX_DURATION", None::<&str>)]);
            assert_eq!(stream_max_duration(), Some(Duration::from_secs(900)));
        }
        {
            let _guard = env_lock::lock_env([("GOOSE_STREAM_MAX_DURATION", Some("90"))]);
            assert_eq!(stream_max_duration(), Some(Duration::from_secs(90)));
        }
        {
            let _guard = env_lock::lock_env([("GOOSE_STREAM_MAX_DURATION", Some("0"))]);
            assert_eq!(stream_max_duration(), None);
        }
        {
            let _guard = env_lock::lock_env([("GOOSE_STREAM_MAX_DURATION", Some("invalid"))]);
            assert_eq!(stream_max_duration(), Some(Duration::from_secs(900)));
        }
    }

    #[tokio::test(start_paused = true)]
    async fn capped_stream_passes_items_through() {
        let _guard = env_lock::lock_env([("GOOSE_STREAM_MAX_DURATION", Some("60"))]);
        let inner: MessageStream = Box::pin(stream::iter(vec![text_item(), text_item()]));
        let items: Vec<_> = cap_stream_duration(inner, false).collect().await;
        assert_eq!(items.len(), 2);
        assert!(items.iter().all(Result::is_ok));
    }

    #[tokio::test(start_paused = true)]
    async fn wedged_stream_errors_at_cap_without_retrying_transiently() {
        let _guard = env_lock::lock_env([("GOOSE_STREAM_MAX_DURATION", Some("60"))]);
        let inner: MessageStream = Box::pin(
            stream::once(async { text_item() }).chain(stream::pending()),
        );
        let mut capped = cap_stream_duration(inner, false);
        assert!(capped.next().await.unwrap().is_ok());
        let error = capped.next().await.unwrap().unwrap_err();
        assert!(matches!(error, ProviderError::RequestFailed(ref msg) if msg.contains("maximum duration")));
        assert!(!should_retry(&error, &RetryConfig::default().transient_only()));
        assert!(capped.next().await.is_none());
    }

    #[tokio::test(start_paused = true)]
    async fn zero_disables_cap() {
        let _guard = env_lock::lock_env([("GOOSE_STREAM_MAX_DURATION", Some("0"))]);
        let inner: MessageStream = Box::pin(stream::pending());
        let mut uncapped = cap_stream_duration(inner, false);
        assert!(tokio::time::timeout(Duration::from_secs(86_400), uncapped.next()).await.is_err());
    }

    #[tokio::test(start_paused = true)]
    async fn managed_context_provider_is_not_capped() {
        let _guard = env_lock::lock_env([("GOOSE_STREAM_MAX_DURATION", Some("60"))]);
        let inner: MessageStream = Box::pin(stream::pending());
        let mut uncapped = cap_stream_duration(inner, true);
        assert!(tokio::time::timeout(Duration::from_secs(86_400), uncapped.next()).await.is_err());
    }
}
'''
Path("crates/goose-provider-types/src/stream_cap.rs").write_text(stream_cap)

replace_exact(
    "crates/goose-provider-types/src/lib.rs",
    "pub mod retry;\npub mod thinking;",
    "pub mod retry;\npub mod stream_cap;\npub mod thinking;",
)

replace_exact(
    "crates/goose-providers/src/lib.rs",
    "    goose_mode, images, json, model, permission, request_log, retry, thinking, utils,\n",
    "    goose_mode, images, json, model, permission, request_log, retry, stream_cap, thinking, utils,\n",
)

replace_exact(
    "crates/goose-provider-types/src/base.rs",
    '''        let stream = self.stream(model_config, system, messages, tools).await?;
        collect_stream(stream).await
''',
    '''        let stream = self.stream(model_config, system, messages, tools).await?;
        collect_stream(crate::stream_cap::cap_stream_duration(
            stream,
            self.manages_own_context(),
        ))
        .await
''',
)

replace_exact(
    "crates/goose/src/agents/reply_parts.rs",
    '''    let mut stream = match stream_result {
        Ok(s) => s,
''',
    '''    let mut stream = match stream_result {
        Ok(s) => goose_providers::stream_cap::cap_stream_duration(
            s,
            provider.manages_own_context(),
        ),
''',
)

replace_exact(
    "crates/goose/src/providers/githubcopilot.rs",
    '''                collect_stream(self.stream(model_config, system, messages, tools).await?).await
''',
    '''                let stream = self.stream(model_config, system, messages, tools).await?;
                collect_stream(goose_providers::stream_cap::cap_stream_duration(
                    stream,
                    self.manages_own_context(),
                ))
                .await
''',
)

replace_exact(
    "crates/goose-provider-types/Cargo.toml",
    '''tokio = { workspace = true, features = ["rt-multi-thread"] }
''',
    '''tokio = { workspace = true, features = ["rt-multi-thread", "test-util"] }
''',
)

print("wave 8 stream-cap correction applied")
