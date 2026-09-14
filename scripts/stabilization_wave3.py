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

# HC-AUD-004: an approval response without a persisted tool response is ambiguous after a crash.
# Do not automatically re-dispatch a potentially completed side effect. Only a still-pending
# approval is safe to resume automatically.
replace_exact(
    "crates/goose/src/acp/server/load_session.rs",
    '''        let should_resume_state_machine = crate::agents::state_machine::enabled()
            && (!pending_confirmations.is_empty()
                || session
                    .conversation
                    .as_ref()
                    .is_some_and(has_unapplied_tool_confirmation_response));
''',
    '''        let has_ambiguous_executed_tool = session
            .conversation
            .as_ref()
            .is_some_and(has_unapplied_tool_confirmation_response);
        if crate::agents::state_machine::enabled()
            && pending_confirmations.is_empty()
            && has_ambiguous_executed_tool
        {
            warn!(
                session_id = session_id_str,
                "Not auto-resuming an approved tool call without a persisted response; the tool may already have produced side effects before interruption"
            );
        }
        let should_resume_state_machine =
            crate::agents::state_machine::enabled() && !pending_confirmations.is_empty();
''',
)

# HC-AUD-008: prefer the widely deployed pre-discovery MCP initialization protocol by default.
# Newer 2026 protocol behavior remains available through explicit protocol_version configuration.
replace_exact(
    "crates/goose/src/agents/agent.rs",
    '''            mcp_host_info: None,
            elicitation_handler: None,
            mcp_protocol_version: None,
            session_name_update_tx: None,
''',
    '''            mcp_host_info: None,
            elicitation_handler: None,
            mcp_protocol_version: Some(ProtocolVersion::V_2025_11_25),
            session_name_update_tx: None,
''',
)

print("wave 3 stabilization patches applied")
