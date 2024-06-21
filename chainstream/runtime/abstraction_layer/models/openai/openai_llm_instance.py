from ..llm_instance_base import LLMInstanceBase
from openai import OpenAI

class OpenAIBase(LLMInstanceBase):
    def __init__(self):
        super().__init__()
        pass

    def process_query(self, input_data) -> object:
        raise NotImplementedError("process_query method not implemented")

    def release_resources(self):
        raise NotImplementedError("release_resources method not implemented")

    def init_resources(self):
        raise NotImplementedError("init_resources method not implemented")
    

