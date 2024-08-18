from AgentGenerator.generator.generator_base import AgentGeneratorBase
from AgentGenerator.prompt.without_chainstream_prompt import NATIVE_GPT_PROMPT

base_code = """
from openai import OpenAI

def process_data(input_streams: dict[str, list]):
    gpt = OpenAI('gpt3-api-key')
    prompt = %s.format(input_streams)
    response = gpt.Completion.create(engine='gpt-4o', prompt=prompt)
    target_stream = {'output_response': [response.choices[0].text]}
    
    return target_stream: dict[str, list]
    
"""


class NativeGPTZeroshotGenerator(AgentGeneratorBase):
    def __init__(self):
        super().__init__()

    def generate_agent_impl(self, chainstream_doc: str, input_and_output_prompt: str) -> str:
        gpt_prompt = NATIVE_GPT_PROMPT.format(input_and_output_prompt)
        agent_code = base_code % gpt_prompt
        return agent_code
