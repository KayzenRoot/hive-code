from pathlib import Path

path = Path("crates/goose/src/execution/manager.rs")
text = path.read_text()

old = '''        if agent.provider().await.is_err() {
            if let Some(error) = provider_restore_error {
                return Err(error);
            }
            anyhow::bail!("Provider not set for session {session_id}");
        }
'''
new = '''        if agent.provider().await.is_err() {
            // A failed persisted-provider restore must never poison the LRU with
            // an unusable agent. Provider-less sessions, however, are valid:
            // callers may create an agent before selecting a provider, and the
            // long-standing manager tests rely on that lifecycle. Only the
            // failed-restore case is fail-closed here.
            if let Some(error) = provider_restore_error {
                return Err(error);
            }
        }
'''

if old not in text:
    if new in text:
        print("wave12 already applied")
        raise SystemExit(0)
    raise SystemExit("expected provider restore guard not found; refusing broad mutation")

text = text.replace(old, new, 1)
path.write_text(text)
print("wave12 providerless-session regression correction applied")
