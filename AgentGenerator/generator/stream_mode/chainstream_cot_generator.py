from AgentGenerator.generator.generator_base import DirectAgentGenerator
from AgentGenerator.prompt import get_base_prompt
from AgentGenerator.io_model import StreamListDescription


class ChainStreamCoTGenerator(DirectAgentGenerator):
    def __init__(self, example_number=0):
        super().__init__()

        self.example_number = example_number

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(output_stream, input_stream,
                               framework_name="chainstream",
                               example_number=self.example_number,
                               mission_name="stream",
                               command_name="cot",
                               need_feedback_example=False)

    def process_response(self, response) -> str:
        try:
            code = response.strip().split("CODE<<")[-1].split(">>")[0].strip()
            if code.startswith("```python") and code.endswith("```"):
                code = code[len("```python"):-3]
        except Exception as e:
            try:
                code = response.strip().split("Thought: ")[1].strip()
            except Exception as e:
                return ""

        return code



if __name__ == "__main__":
    agent_generator = ChainStreamCoTGenerator()
    agent_code, latency, tokens = agent_generator.generate_agent(
        StreamListDescription(streams=[{
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
