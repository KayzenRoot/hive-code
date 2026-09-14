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

# Session timestamp unit mismatch.
replace_exact(
    "crates/goose/src/session/session_manager.rs",
    '''        let created = message.created.max(latest.unwrap_or(message.created));
''',
    '''        let latest = latest.map(|timestamp| {
            if timestamp > MILLISECOND_TIMESTAMP_THRESHOLD {
                timestamp / 1000
            } else {
                timestamp
            }
        });
        let created = message.created.max(latest.unwrap_or(message.created));
''',
)

# Devcontainer must include the native build tools required by local inference / bindgen.
replace_exact(
    ".devcontainer/Dockerfile",
    '''    build-essential \\
    libdbus-1-dev \\
''',
    '''    build-essential \\
    cmake \\
    libclang-dev \\
    libdbus-1-dev \\
''',
)

# Permission initialization must not panic merely because the config directory is unavailable.
replace_exact(
    "crates/goose/src/config/permission.rs",
    '''            // Consolidate directory creation for re-use in global singleton or ACP.
            fs::create_dir_all(&config_dir).expect("Failed to create config directory");
            HashMap::new()
''',
    '''            // Consolidate directory creation for re-use in global singleton or ACP.
            if let Err(error) = fs::create_dir_all(&config_dir) {
                tracing::warn!(
                    path = %config_dir.display(),
                    %error,
                    "Failed to create permission config directory; continuing with in-memory defaults"
                );
            }
            HashMap::new()
''',
)

# Desktop must not offer 100% as an enabled auto-compaction threshold when backend semantics
# define >= 1.0 as disabled. Existing 1.0 values are surfaced as disabled.
path = "ui/desktop/src/components/alerts/AlertBox.tsx"
replace_exact(
    path,
    '''  compactNow: {
    id: 'alertBox.compactNow',
    defaultMessage: 'Compact now',
  },
''',
    '''  compactNow: {
    id: 'alertBox.compactNow',
    defaultMessage: 'Compact now',
  },
  autoCompactOff: {
    id: 'alertBox.autoCompactOff',
    defaultMessage: 'Auto compact: off',
  },
''',
)
replace_exact(
    path,
    '''          setThresholdValue(Math.max(1, Math.round(threshold * 100)));
''',
    '''          setThresholdValue(Math.max(1, Math.min(99, Math.round(threshold * 100))));
''',
)
replace_exact(
    path,
    '''    let validThreshold = Math.max(1, Math.min(100, thresholdValue));
''',
    '''    let validThreshold = Math.max(1, Math.min(99, thresholdValue));
''',
)
replace_exact(path, '                  max="100"\n', '                  max="99"\n')
replace_exact(
    path,
    '''                      setThresholdValue(Math.max(1, Math.min(100, val)));
''',
    '''                      setThresholdValue(Math.max(1, Math.min(99, val)));
''',
)
replace_exact(
    path,
    '''                    } else if (val > 100) {
                      setThresholdValue(100);
''',
    '''                    } else if (val > 99) {
                      setThresholdValue(99);
''',
)
replace_exact(
    path,
    '''                      const resetValue = Math.round(currentThreshold * 100);
                      setThresholdValue(Math.max(1, resetValue));
''',
    '''                      const resetValue = Math.round(currentThreshold * 100);
                      setThresholdValue(Math.max(1, Math.min(99, resetValue)));
''',
)
replace_exact(
    path,
    '''                  {intl.formatMessage(i18n.autoCompactAt)} {Math.round(currentThreshold * 100)}%
''',
    '''                  {currentThreshold >= 1
                    ? intl.formatMessage(i18n.autoCompactOff)
                    : `${intl.formatMessage(i18n.autoCompactAt)} ${Math.round(currentThreshold * 100)}%`}
''',
)

print("wave 5 stabilization patches applied")
