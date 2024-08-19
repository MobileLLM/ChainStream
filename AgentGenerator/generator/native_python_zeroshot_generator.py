from AgentGenerator.utils.llm_utils import TextGPTModel
from AgentGenerator.generator.generator_base import DirectAgentGenerator
from AgentGenerator.io_model import StreamListDescription
from AgentGenerator.prompt import get_base_prompt


class NativePythonZeroShotGenerator(DirectAgentGenerator):
    def __init__(self):
        super().__init__()

    # def generate_agent_impl(self, chainstream_doc: str, input_and_output_prompt: str) -> str:
    #     input_and_output_prompt = "\n".join(input_and_output_prompt.split("\n")[:-3])
    #     prompt = f"{NATIVE_PYTHON_CHAINSTREAM_ENGLISH_PROMPT}\n{input_and_output_prompt}\n\nCode:\n"
    #
    #     print(f"Prompt: {prompt}")
    #
    #     prompt = [{
    #         "role": "system",
    #         "content": prompt,
    #     }]
    #
    #     response = self.llm.query(prompt)
    #     return response.replace("'''", " ").replace("```", " ").replace("python", "")

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(output_stream, input_stream,
                               framework_name="native_python",
                               example_number=0,
                               mission_name="batch",
                               command_name="few_shot",
                               need_feedback_example=False)

    def process_response(self, response) -> str:
        return response.replace("'''", " ").replace("```", " ").replace("python", "")


if __name__ == "__main__":
    agent_generator = NativePythonZeroShotGenerator()
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
