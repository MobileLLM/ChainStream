from ..llm_instance_base import LLMInstanceBase
from openai import OpenAI

# TODO: change the GPT_CONFIG to a config file
GPT_CONFIG = {
    "url": "https://api.openai-proxy.org/v1",
    "key": "sk-qnAcq9g0VKZt3I49s99JLWPRBXzmxyT0aWYJh0cqGJPeKzx9"
}


class OpenAIBase(LLMInstanceBase):
    def __init__(self, temperature=0.7, timeout=15, retry=3):
        super().__init__()

        try:
            self.url = GPT_CONFIG['url']
            self.api_key = GPT_CONFIG['key']
            self.temperature = temperature
            self.retry = retry
            self.client = OpenAI(
                base_url=self.url,
                api_key=self.api_key,
                timeout=timeout,
                max_retries=retry,
            )
        except KeyError:
            print("Please set GPT_API_URL and GPT_API_KEY environment variables.")
            exit()


class OpenAITextLLMBase(OpenAIBase):
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


class OpenAITextGPT35(OpenAITextLLMBase):
    def __init__(self, model="gpt-3.5-turbo-1106", temperature=0.7, timeout=15, retry=3):
        super().__init__(model, temperature, timeout, retry)


class OpenAITextGPT4(OpenAITextLLMBase):
    def __init__(self, model="gpt-4", temperature=0.7, timeout=15, retry=3):
        super().__init__(model, temperature, timeout, retry)
