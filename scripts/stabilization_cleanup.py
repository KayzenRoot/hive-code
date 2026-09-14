#!/usr/bin/env python3
from pathlib import Path

path = Path("crates/goose/src/oauth/mod.rs")
text = path.read_text()
line = "    let mut preserve_credentials_after_refresh_failure = false;\n"
while text.count(line) > 1:
    first = text.find(line)
    second = text.find(line, first + len(line))
    text = text[:second] + text[second + len(line):]
path.write_text(text)
print("stabilization cleanup complete")
