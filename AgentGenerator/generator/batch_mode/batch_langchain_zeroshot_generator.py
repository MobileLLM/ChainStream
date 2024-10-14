from AgentGenerator.utils.llm_utils import TextGPTModel
from AgentGenerator.generator.generator_base import DirectAgentGenerator
from AgentGenerator.io_model import StreamListDescription
from AgentGenerator.prompt import get_base_prompt


class LangChainZeroshotGenerator(DirectAgentGenerator):
    def __init__(self, model_name='gpt-4o'):
        super().__init__()

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(input_stream, output_stream,
                               framework_name='batch_langchain',
                               example_number=0,
                               mission_name='batch',
                               command_name='few_shot',
                               need_feedback_example=False)

    def process_response(self, response) -> str:
        return response.replace("'''", " ").replace("```", " ").replace("python", "")


if __name__ == "__main__":
    agent_generator = LangChainZeroshotGenerator()
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
