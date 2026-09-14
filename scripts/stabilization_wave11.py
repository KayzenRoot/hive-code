#!/usr/bin/env python3
from pathlib import Path

# CI-only hygiene: remove imports/helpers made obsolete by the stabilization patches.
cli = Path("crates/goose-cli/src/recipes/extract_from_cli.rs")
text = cli.read_text()
old = "use std::path::{Path, PathBuf};"
new = "use std::path::PathBuf;"
if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise SystemExit("unexpected extract_from_cli.rs import state")
cli.write_text(text)

agent_test = Path("crates/goose/src/agents/state_machine/tests/agent_reply.rs")
text = agent_test.read_text()
start = text.find("async fn stream_messages(\n")
if start != -1:
    end_marker = "\n}\n\n#[tokio::test]"
    end = text.find(end_marker, start)
    if end == -1:
        raise SystemExit("could not locate end of obsolete stream_messages helper")
    text = text[:start] + text[end + 3:]
agent_test.write_text(text)

print("wave 11 Rust CI hygiene applied")
