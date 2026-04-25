"""
Chat-based command prompt for interactive agent generation.
This prompt defines the JSON output format required for chat-based generation.
"""

CHAT_BASED_COMMAND_PROMPT = """
**Output Format:**

Please respond with a JSON object containing the following fields:

```json
{
    "new_code": "string - The complete updated agent code",
    "pseudocode": "string - Natural-language pseudocode for non-programmers (see rules below)",
    "new_history": "string - A summary of the editing history and context for future reference",
    "message_to_user": "string - Your feedback message to the user explaining what was done (MUST be in English)"
}
```

**Important:**
1. Return ONLY the JSON object, no additional text or explanation outside the JSON.
2. The `new_code` field should contain the complete, executable agent code.
3. The `pseudocode` field MUST be written in **Chinese** (简体中文). It must be a plain-language, step-by-step explanation of what `new_code` does, aligned with the code structure (imports, classes, functions, main flow, stream handling). Use numbered steps or short indented paragraphs; **do not** use programming syntax (no braces, semicolons, or code keywords as code). A non-technical reader should understand the agent's behavior. If `new_code` is empty or unchanged, still provide a brief explanation of the current state.
4. The `new_history` field should summarize what has been done so far to maintain context for future interactions.
5. The `message_to_user` field MUST be written in English, explaining the changes made in a user-friendly way.

Your response:
"""

