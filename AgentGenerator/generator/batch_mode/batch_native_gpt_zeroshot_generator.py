from AgentGenerator.generator.generator_base import AgentGeneratorBase
from AgentGenerator.prompt import get_base_prompt

base_code = """
import openai
import os
import PIL.Image
from chainstream.llm import make_prompt

openai.api_key = os.environ['OPENAI_API_KEY']
openai.base_url = os.environ['OPENAI_BASE_URL'] 

base_prompt = {base_prompt}

def process_data(input_streams: dict[str, list]):
    new_dict = {{}}
    image_list = []
    for key, value in input_streams.items():
        # print(f"key: {{key}}, value: {{value}}, type: {{type(value[0])}}")
        new_dict[key] = []
        for item in value:
            new_item = dict()
            for k, v in item.items():
                if isinstance(v, list) and isinstance(v[0], PIL.Image.Image):
                    # print(f"Image found: {{v}}")
                    new_item[k] = ["Image stream, the image is at the end of the prompt"]
                    image_list.append(v)
                else:
                    # print(f"Image found: {{v}}")
                    new_item[k] = v
            new_dict[key].append(new_item)
    
    prompt = base_prompt.format(input_data=new_dict)
    # print("Prompt before: ", prompt)
    message = make_prompt(prompt, *image_list)
    
    client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'], base_url=os.environ['OPENAI_BASE_URL'])
    # print("Prompt: ", message)
    response = client.chat.completions.create(
        model={model_name},
        messages=message
    )
    target_stream = response.choices[0].message.content
    
    return target_stream
"""


class NativeGPTGenerator(AgentGeneratorBase):
    def __init__(self, model_name="gpt-4o"):
        super().__init__()
        self.model_name = model_name

    def generate_agent_impl(self, output_stream, input_stream) -> str:
        base_prompt = get_base_prompt(output_stream, input_stream,
                                      framework_name="native_gpt",
                                      example_number=0,
                                      mission_name="native_gpt",
                                      command_name="native_gpt",
                                      need_feedback_example=False)
        # print(base_prompt)
        prompt = base_code.format(base_prompt="'''" + base_prompt.replace("\n", "\\n").replace("{", "{{").replace("}", "}}").replace("[input_data]", "{input_data}") + "'''", model_name="'" + self.model_name + "'")
        # print(prompt)
        return prompt

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return """"""


if __name__ == "__main__":
    from ChainStreamSandBox.tasks import get_task_with_data_batch
    agent_generator = NativeGPTGenerator()
    task = get_task_with_data_batch()["EmailTask1"]()
    agent_code, latency, tokens = agent_generator.generate_agent(
        task.output_stream_description, input_description=task.input_stream_description
    )

    print(agent_code)
    print(latency)
    print(tokens)
