from AgentGenerator.prompt import get_base_prompt
from AgentGenerator.generator.generator_base import DirectAgentGenerator
from AgentGenerator.io_model import StreamListDescription


class ChainStreamFewShotGenerator(DirectAgentGenerator):
    def __init__(self, framework_example_number=0, base_prompt_example_select_policy='random'):
        super().__init__()

        self.example_number = framework_example_number
        self.base_prompt_example_select_policy = base_prompt_example_select_policy

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(output_stream, input_stream,
                               framework_name="chainstream",
                               example_number=self.example_number,
                               mission_name="stream",
                               command_name="few_shot",
                               need_feedback_example=False,
                               task_now=self.task.__class__.__name__,
                               example_select_policy=self.base_prompt_example_select_policy
                               )

    def process_response(self, response) -> str:
        return response.replace("'''", " ").replace("```", " ").replace("python", "")


if __name__ == "__main__":
    agent_generator = ChainStreamFewShotGenerator(example_number=1)
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
