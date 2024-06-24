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
