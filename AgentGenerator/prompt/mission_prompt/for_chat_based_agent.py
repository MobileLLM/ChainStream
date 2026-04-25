"""
Chat-based mission prompt for interactive agent generation.
This prompt includes history, current code, and user message for iterative development.
"""

CHAT_BASED_MISSION_PROMPT_FOR_CHAINSTREAM = """
Your mission is to interactively develop an agent with chainstream framework based on user's conversation.

**Target Output Streams:**
{output_stream}

**Available Input Streams:**
{input_stream}

**User's Knowledge Base / Reference Material:**
{knowledge_base}

**Chat Context:**

{chat_context}

**User's Current Message:**
{user_message}

Please understand the user's request in the context of the conversation history, knowledge base, and current code, then generate or modify the agent code accordingly.
"""

