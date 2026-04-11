from chainstream.llm import API_LLM_TYPE
from .openai_llm_instance_base import OpenAIBase


class OpenAIImageLLMBase(OpenAIBase):
    def __init__(self, model, temperature=0.7, timeout=15, retry=3):
        super().__init__(temperature, timeout, retry)
        self.model = model

    def process_query(self, prompt_message) -> object:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=prompt_message,
            temperature=self.temperature
        )
        res = response.choices[0].message.content
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        return res, prompt_tokens, completion_tokens

    def release_resources(self):
        return True

    def init_resources(self):
        return True


class OpenAITextGPT4(OpenAIImageLLMBase):
    model_name = "openai-gpt-4-vision-preview"
    model_type = API_LLM_TYPE['T']

    def __init__(self, model="gpt-4-vision-preview", temperature=0.7, timeout=15, retry=3):
        super().__init__(model, temperature, timeout, retry)
