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
    "new_history": "string - A summary of the editing history and context for future reference",
    "message_to_user": "string - Your feedback message to the user explaining what was done (MUST be in English)"
}
```

**Important:**
1. Return ONLY the JSON object, no additional text or explanation outside the JSON.
2. The `new_code` field should contain the complete, executable agent code.
3. The `new_history` field should summarize what has been done so far to maintain context for future interactions.
4. The `message_to_user` field MUST be written in English, explaining the changes made in a user-friendly way.

Your response:
"""

