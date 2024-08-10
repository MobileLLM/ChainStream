from AgentGenerator.utils.llm_utils import TextGPTModel
from AgentGenerator.generator.generator_base import AgentGeneratorBase
from AgentGenerator.io_model import StreamListDescription
from AgentGenerator.prompt.without_chainstream_prompt import WITHOUT_CHAINSTREAM_CHINESE_PROMPT


class AgentGeneratorWithoutChainstream(AgentGeneratorBase):
    def __init__(self, model_name='gpt-4o'):
        super().__init__()
        self.model_name = model_name
        self.model = TextGPTModel(model_name)

    def generate_agent_impl(self, chainstream_doc: str, input_and_output_prompt: str) -> str:
        input_and_output_prompt = "\n".join(input_and_output_prompt.split("\n")[:-3])
        prompt = f"{WITHOUT_CHAINSTREAM_CHINESE_PROMPT}\n{input_and_output_prompt}\n\nCode:\n"

        print(f"Prompt: {prompt}")

        prompt = [{
            "role": "system",
            "content": prompt,
        }]

        response = self.model.query(prompt)
        return response.replace("'''", " ").replace("```", " ").replace("python", "")


if __name__ == "__main__":
    agent_generator = AgentGeneratorWithoutChainstream()
    agent_code = agent_generator.generate_agent(
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
