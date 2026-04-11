# Chat Mode for Agent Generator

## Overview

The Chat Mode is an interactive agent development feature that allows users to iteratively create and modify agents through natural language conversations. This mode maintains conversation history and current code state, enabling context-aware code generation.

## Architecture

### Three-Part Prompt Structure

The Chat Mode follows the standard ChainStream prompt architecture with three components:

1. **Framework Prompt** (`get_framework_doc`)
   - Contains ChainStream framework documentation
   - Includes examples based on target language (Python/Java)
   - Provides API references and best practices

2. **Mission Prompt** (`get_mission_prompt` with `mission_type='chat'`)
   - Defines the agent development task
   - Includes conversation history
   - Shows current code state
   - Presents user's current message
   - Specifies input/output stream requirements

3. **Command Prompt** (`get_command_prompt` with `command_type='chat'`)
   - Defines the JSON output format
   - Requires three fields: `new_code`, `new_history`, `message_to_user`

### Data Flow

```
Frontend (generator.vue)
    ↓ [message, code, memory]
Backend API (/api/generator/chat)
    ↓ [chat_message_dict]
ChainStreamChatGenerator (Python/Java)
    ↓ [formatted prompt]
LLM (GPT-4)
    ↓ [JSON response]
process_response()
    ↓ [new_code, new_history, message_to_user]
Backend API
    ↓ [reply, new_code, new_memory, stats]
Frontend (updates editor & chat)
```

## Components

### New Files

1. **`AgentGenerator/prompt/mission_prompt/for_chat_based_agent.py`**
   - Chat-specific mission prompt template
   - Includes placeholders for history, code, and user message

2. **`AgentGenerator/prompt/command_prompt/chat_based.py`**
   - JSON output format specification
   - Defines required fields for chat response

### Modified Files

1. **`AgentGenerator/prompt/mission_prompt/__init__.py`**
   - Added `mission_type='chat'` support
   - Implements chat message parsing and formatting

2. **`AgentGenerator/prompt/command_prompt/__init__.py`**
   - Added `command_type='chat'` support

3. **`AgentGenerator/prompt/__init__.py`**
   - Updated type definitions to include `'chat'`

4. **`AgentGenerator/generator/stream_mode/chainstream_chat_generator_python.py`**
   - Updated to use `mission_name='chat'` and `command_name='chat'`
   - Added JSON response parsing in `process_response()`
   - Added `get_last_response_metadata()` to extract history and message

5. **`AgentGenerator/generator/stream_mode/chainstream_chat_generator_java.py`**
   - Same updates as Python version

6. **`chainstream/runtime/web/backend/monitor/agents.py`**
   - Constructs `chat_message_dict` with history, code, message
   - Extracts metadata from generator response
   - Returns structured response with reply, new_code, new_memory, stats

## Usage

### Frontend

```javascript
// Send a chat message
const response = await request.post('/api/generator/chat', {
  message: 'Add a function to filter emails',
  code: currentCode,
  memory: sessionMemory,
  language: 'python',
  generator_type: 'python_single'
})

// Update state
generatedCode.value = response.new_code
sessionMemory.value = response.new_memory
chatMessages.value.push({
  role: 'assistant',
  content: response.reply,
  stats: response.stats
})
```

### Backend

```python
# Generator receives chat_message_dict
chat_message_dict = {
    'history': memory,
    'code': code,
    'message': message
}

agent_code, latency, tokens = gen.generate_agent_chat(
    message=chat_message_dict,
    output_description=output_desc,
    input_description=input_desc
)

# Extract metadata
metadata = gen.get_last_response_metadata()
new_memory = metadata.get('new_history', '')
reply = metadata.get('message_to_user', '')
```

### Generator

```python
# In chainstream_chat_generator_python.py
def get_base_prompt(self, output_stream, input_stream, message=None):
    return get_base_prompt(
        output_stream, input_stream,
        framework_name="chainstream",
        mission_name="chat",      # Use chat mode
        command_name="chat",      # Use chat command
        chat_message=message,     # Pass chat_message_dict
        target_language="python"
    )
```

## JSON Response Format

The LLM must return a JSON object with the following structure:

```json
{
    "new_code": "# Complete updated agent code\nfrom chainstream import Agent\n...",
    "new_history": "Summary of changes: Added email filtering function, implemented regex pattern matching...",
    "message_to_user": "I've added a filter_emails() function that uses regex to filter out spam emails. The function is integrated with the existing email processing stream."
}
```

### Field Descriptions

- **`new_code`**: Complete, executable agent code (Python or Java)
- **`new_history`**: Summary of editing history and context for future reference
- **`message_to_user`**: User-friendly explanation of changes made

## Token Count Fix

The backend now correctly handles token counts returned as tuples:

```python
if isinstance(tokens, (list, tuple)) and len(tokens) >= 2:
    pt_raw, ct_raw = tokens[0], tokens[1]
    pt = int(pt_raw)
    ct = int(ct_raw)
    tt = pt + ct
```

This ensures that `(prompt_tokens, completion_tokens)` tuples from `llm.get_token_count()` are properly parsed.

## Error Handling

1. **JSON Parsing Failure**: Falls back to returning raw response with warning
2. **Missing Fields**: Uses empty strings as defaults
3. **Generator Failure**: Falls back to mock generator with simulated response

## Future Enhancements

1. Support for multi-turn refinement with sandbox testing
2. Integration with exception handler for error-driven iteration
3. Support for other languages (JavaScript, Go, etc.)
4. Enhanced history summarization with context compression
5. Real-time code validation and linting feedback


