from AgentGenerator.generator.generator_base import AgentGeneratorBase
from AgentGenerator.prompt import get_base_prompt

base_code = """
import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']
openai.base_url = os.environ['OPENAI_API_URL'] 

def process_data(input_streams: dict[str, list]):
    prompt = %s.format(input_streams)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", 
                "content": prompt
            },
        ]
    )
    target_stream = response.choices[0].text
    
    return target_stream: dict[str, list]    
"""


class NativeGPTZeroshotGenerator(AgentGeneratorBase):
    def __init__(self):
        super().__init__()

    def generate_agent_impl(self, chainstream_doc: str, input_and_output_prompt: str) -> str:
        gpt_prompt = NATIVE_GPT_PROMPT.format(input_and_output_prompt)
        agent_code = base_code % gpt_prompt
        return agent_code
