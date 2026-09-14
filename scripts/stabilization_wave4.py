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

path = "crates/goose-provider-types/src/formats/openai.rs"

# HC-AUD-010: strict OpenAI-compatible APIs require every tool result for one assistant
# tool-call batch to remain consecutive. Synthetic user/image messages must follow the full batch.
replace_exact(
    path,
    '''        i = insert_at + num_collected;
    }
}

/// True if `msg` is a synthetic image-only user message (content is exclusively image_url items).
''',
    '''        i = insert_at + num_collected;
    }

    move_tool_result_images_after_complete_batch(messages);
}

/// Move synthetic image messages emitted for tool results until after every result belonging to
/// the preceding assistant tool-call batch. This preserves the OpenAI invariant that an assistant
/// message with N tool_calls is followed by N uninterrupted tool messages.
fn move_tool_result_images_after_complete_batch(messages: &mut Vec<Value>) {
    let mut i = 0;
    while i < messages.len() {
        let expected: std::collections::HashSet<String> = messages[i]
            .get("tool_calls")
            .and_then(Value::as_array)
            .into_iter()
            .flatten()
            .filter_map(|call| call.get("id").and_then(Value::as_str).map(str::to_owned))
            .collect();
        if messages[i].get("role") != Some(&json!("assistant")) || expected.is_empty() {
            i += 1;
            continue;
        }

        let mut seen = std::collections::HashSet::new();
        let mut tools = Vec::new();
        let mut images = Vec::new();
        let mut scan = i + 1;
        while scan < messages.len() {
            if messages[scan].get("role") == Some(&json!("tool")) {
                let Some(id) = messages[scan].get("tool_call_id").and_then(Value::as_str) else {
                    break;
                };
                if !expected.contains(id) || !seen.insert(id.to_owned()) {
                    break;
                }
                tools.push(messages[scan].clone());
                scan += 1;
                continue;
            }
            if !seen.is_empty() && is_image_only_user_message(&messages[scan]) {
                images.push(messages[scan].clone());
                scan += 1;
                continue;
            }
            break;
        }

        if seen == expected && !images.is_empty() {
            let mut replacement = tools;
            replacement.extend(images);
            messages.splice(i + 1..scan, replacement);
            i = scan;
        } else {
            i += 1;
        }
    }
}

/// True if `msg` is a synthetic image-only user message (content is exclusively image_url items).
''',
)

replace_exact(
    path,
    '''    #[test]
    fn test_merge_split_tool_calls_with_image_gap() {
        let mut messages = vec![
            json!({"role": "assistant", "tool_calls": [{"id": "tc1", "type": "function", "function": {"name": "screenshot", "arguments": "{}"}}], "reasoning_content": "thinking..."}),
            json!({"role": "tool", "tool_call_id": "tc1", "content": "This tool result included an image that is uploaded in the next message."}),
            json!({"role": "user", "content": [{"type": "image_url", "image_url": {"url": "data:image/png;base64,abc"}}]}),
            json!({"role": "assistant", "tool_calls": [{"id": "tc2", "type": "function", "function": {"name": "click", "arguments": "{}"}}], "reasoning_content": "thinking..."}),
            json!({"role": "tool", "tool_call_id": "tc2", "content": "clicked"}),
        ];
        merge_split_tool_call_messages(&mut messages);

        assert_eq!(messages.len(), 4);
        assert_eq!(messages[0]["tool_calls"].as_array().unwrap().len(), 2);
        assert_eq!(messages[0]["role"], "assistant");
        assert_eq!(messages[1]["role"], "tool");
        assert_eq!(messages[1]["tool_call_id"], "tc1");
        assert_eq!(messages[2]["role"], "user");
        assert_eq!(messages[3]["role"], "tool");
        assert_eq!(messages[3]["tool_call_id"], "tc2");
    }
''',
    '''    #[test]
    fn test_merge_split_tool_calls_with_image_gap() {
        let mut messages = vec![
            json!({"role": "assistant", "tool_calls": [{"id": "tc1", "type": "function", "function": {"name": "screenshot", "arguments": "{}"}}], "reasoning_content": "thinking..."}),
            json!({"role": "tool", "tool_call_id": "tc1", "content": "This tool result included an image that is uploaded in the next message."}),
            json!({"role": "user", "content": [{"type": "image_url", "image_url": {"url": "data:image/png;base64,abc"}}]}),
            json!({"role": "assistant", "tool_calls": [{"id": "tc2", "type": "function", "function": {"name": "click", "arguments": "{}"}}], "reasoning_content": "thinking..."}),
            json!({"role": "tool", "tool_call_id": "tc2", "content": "clicked with image"}),
            json!({"role": "user", "content": [{"type": "image_url", "image_url": {"url": "data:image/png;base64,def"}}]}),
        ];
        merge_split_tool_call_messages(&mut messages);

        assert_eq!(messages.len(), 5);
        assert_eq!(messages[0]["tool_calls"].as_array().unwrap().len(), 2);
        assert_eq!(messages[0]["role"], "assistant");
        assert_eq!(messages[1]["role"], "tool");
        assert_eq!(messages[1]["tool_call_id"], "tc1");
        assert_eq!(messages[2]["role"], "tool");
        assert_eq!(messages[2]["tool_call_id"], "tc2");
        assert_eq!(messages[3]["role"], "user");
        assert_eq!(messages[4]["role"], "user");
    }
''',
)

print("wave 4 stabilization patches applied")
