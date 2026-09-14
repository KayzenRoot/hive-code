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

# HC-AUD-009: reasoning is useful provider state, but it is not an answer by itself.
replace_exact(
    "crates/goose-agent/src/inference.rs",
    '''fn is_empty_response(message: &Message) -> bool {
    message.content.iter().all(|content| match content {
        MessageContent::Text(text) => text.text.trim().is_empty(),
        MessageContent::Thinking(thinking) => {
            thinking.thinking.trim().is_empty() && thinking.signature.is_empty()
        }
        _ => false,
    })
}
''',
    '''fn is_empty_response(message: &Message) -> bool {
    message.content.iter().all(|content| match content {
        MessageContent::Text(text) => text.text.trim().is_empty(),
        MessageContent::Thinking(_) | MessageContent::RedactedThinking(_) => true,
        _ => false,
    })
}
''',
)

replace_exact(
    "crates/goose-agent/src/inference.rs",
    '''    #[test]
    fn signed_thinking_without_text_is_not_an_empty_response() {
        assert!(is_empty_response(
            &Message::assistant().with_content(MessageContent::thinking("", ""))
        ));
        assert!(!is_empty_response(
            &Message::assistant().with_content(MessageContent::thinking("", "sig-omitted"))
        ));
    }
''',
    '''    #[test]
    fn thinking_without_answer_is_an_empty_response() {
        assert!(is_empty_response(
            &Message::assistant().with_content(MessageContent::thinking("reasoning", "signature"))
        ));
        assert!(is_empty_response(
            &Message::assistant().with_content(MessageContent::redacted_thinking("encrypted"))
        ));
        assert!(!is_empty_response(
            &Message::assistant()
                .with_content(MessageContent::thinking("reasoning", "signature"))
                .with_text("final answer")
        ));
    }
''',
)

print("wave 9 thinking-only correction applied")
