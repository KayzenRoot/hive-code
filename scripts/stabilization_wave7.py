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

# HC-AUD-008 review correction: do not pin the legacy MCP protocol globally.
# None activates McpClient's Auto negotiation (current preferred + legacy fallback).
replace_exact(
    "crates/goose/src/agents/agent.rs",
    "            mcp_protocol_version: Some(ProtocolVersion::V_2025_11_25),\n",
    "            mcp_protocol_version: None,\n",
)

# HC-AUD-004: a persisted approval without a durable ToolResponse is ambiguous after
# interruption. Normal live approvals stay in the same stream and are unaffected.
# On a resumed process we must not automatically redispatch a possibly completed side effect.
replace_exact(
    "crates/goose/src/agents/agent.rs",
    '''        let pending_confirmations = pending_tool_confirmations(conversation);
        let resume_from_persisted_response = pending_confirmations.is_empty()
            && has_unapplied_tool_confirmation_response(conversation);
        if pending_confirmations.is_empty() && !resume_from_persisted_response {
            return Ok(None);
        }
''',
    '''        let pending_confirmations = pending_tool_confirmations(conversation);
        if pending_confirmations.is_empty() {
            if has_unapplied_tool_confirmation_response(conversation) {
                warn!(
                    session_id = %session_config.id,
                    "Refusing to auto-resume a persisted tool approval without a durable ToolResponse; execution state is ambiguous after interruption"
                );
            }
            return Ok(None);
        }
''',
)

replace_exact(
    "crates/goose/src/agents/agent.rs",
    '''        let agent = Arc::clone(self);
        Ok(Some(Box::pin(async_stream::try_stream! {
            let initial_stream = if resume_from_persisted_response {
                Some(
                    agent
                        .stream_state_machine_session(
                            session_config.clone(),
                            cancel.clone(),
                        )
                        .await?,
                )
            } else {
                None
            };
            let mut stream = agent.stream_state_machine_turn(
                session_config,
                cancel,
                turn_guard,
                initial_stream,
            );
''',
    '''        let agent = Arc::clone(self);
        Ok(Some(Box::pin(async_stream::try_stream! {
            let mut stream = agent.stream_state_machine_turn(
                session_config,
                cancel,
                turn_guard,
                None,
            );
''',
)

# Regression: an approval persisted immediately before interruption is not sufficient
# evidence to redispatch a tool automatically on resume.
replace_exact(
    "crates/goose/src/agents/state_machine/tests/agent_reply.rs",
    '''    drop(stream);
    let stream = agent
        .resume_state_machine_turn(session_config.clone(), CancellationToken::new())
        .await?
        .expect("persisted confirmation response should resume the state-machine turn");
    messages.extend(stream_messages(stream).await?);
    assert!(messages.iter().any(|message| message
        .get_tool_response_ids()
        .contains(&confirmation_id.as_str())));
    assert_eq!(calculator.total(), 1);
    assert_eq!(api.call_count(), 2);

    assert!(agent
        .submit_tool_confirmation(&session_config.id, &confirmation_id, Permission::AllowOnce)
        .await
        .is_err());
    assert_eq!(calculator.total(), 1);
''',
    '''    drop(stream);
    let resumed = agent
        .resume_state_machine_turn(session_config.clone(), CancellationToken::new())
        .await?;
    assert!(
        resumed.is_none(),
        "persisted approval without a durable ToolResponse must fail closed after interruption"
    );
    assert_eq!(
        calculator.total(),
        0,
        "an ambiguous approved tool must not be redispatched automatically"
    );
    assert_eq!(api.call_count(), 1);

    assert!(agent
        .submit_tool_confirmation(&session_config.id, &confirmation_id, Permission::AllowOnce)
        .await
        .is_err());
    assert_eq!(calculator.total(), 0);
''',
)

# Permission persistence: undo the misleading startup fallback. The wider panic-free Result
# refactor remains a separate bounded correction; until then startup must not pretend durable
# permission storage exists when its directory cannot be created.
replace_exact(
    "crates/goose/src/config/permission.rs",
    '''            if let Err(error) = fs::create_dir_all(&config_dir) {
                tracing::warn!(
                    path = %config_dir.display(),
                    %error,
                    "Failed to create permission config directory; continuing with in-memory defaults"
                );
            }
            HashMap::new()
''',
    '''            fs::create_dir_all(&config_dir).expect("Failed to create config directory");
            HashMap::new()
''',
)

print("wave 7 corrections applied")
