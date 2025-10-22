from AgentGenerator.prompt import get_base_prompt
from AgentGenerator.generator.generator_base import DirectAgentGenerator
from AgentGenerator.io_model import StreamListDescription


class ChainStreamChatGeneratorPython(DirectAgentGenerator):
    def __init__(self, framework_example_number=0, base_prompt_example_select_policy='random'):
        super().__init__()

        self.example_number = framework_example_number
        self.base_prompt_example_select_policy = base_prompt_example_select_policy

    def get_base_prompt(self, output_stream, input_stream, message=None) -> str:
        if message is None:
            raise ValueError("Message is required for chainstream chat generator")
        return get_base_prompt(output_stream, input_stream,
                               framework_name="chainstream",
                               example_number=self.example_number,
                               mission_name="chat",
                               command_name="chat",
                               need_feedback_example=False,
                               task_now=self.task.__class__.__name__ if self.task else "ChatTask",
                               example_select_policy=self.base_prompt_example_select_policy,
                               chat_message=message,
                               target_language="python"
                               )

    def process_response(self, response) -> str:
        """
        Process the LLM response which should be in JSON format.
        Expected JSON structure:
        {
            "new_code": "...",
            "new_history": "...",
            "message_to_user": "..."
        }
        """
        import json
        import re
        
        # Try to extract JSON from response (in case there's extra text)
        json_match = re.search(r'\{[\s\S]*"new_code"[\s\S]*\}', response)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = response.strip()
        
        try:
            result = json.loads(json_str)
            # Store the additional fields for backend to use
            self._last_new_history = result.get('new_history', '')
            self._last_message_to_user = result.get('message_to_user', '')
            # Return the new_code as the main output
            return result.get('new_code', '')
        except json.JSONDecodeError as e:
            # Fallback: if JSON parsing fails, return the response as-is (but cleaned)
            self._last_new_history = ''
            self._last_message_to_user = f'Warning: Failed to parse JSON response. Error: {e}'
            return response.replace("'''", " ").replace("```", " ").replace("python", "").strip()
    
    def get_last_response_metadata(self):
        """Return the last new_history and message_to_user from process_response"""
        return {
            'new_history': getattr(self, '_last_new_history', ''),
            'message_to_user': getattr(self, '_last_message_to_user', '')
        }


if __name__ == "__main__":
    agent_generator = ChainStreamChatGeneratorPython()
    agent_code, latency, tokens = agent_generator.generate_agent_chat(
        message="xxx",
        output_description=StreamListDescription(streams=[{
            "stream_id": "summary_by_sender",
            "description": "A list of email summaries grouped by each email sender for pre 3 emails, excluding advertisement emails",
            "fields": {
                "sender": "name xxx, string",
                "summary": "sum xxx, string"
            }
        }]),
        input_description=StreamListDescription(streams=[{
            "stream_id": "all_email",
            "description": "All email messages",
            "fields": {
                "sender": "name xxx, string",
                "Content": "text xxx, string"
            }
        }])
    )
    print(agent_code)
    print(latency)
    print(tokens)
