import base64
import os
import time
import random
from abc import abstractmethod

from openai import OpenAI
import collections
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class BaseOpenAI:
    def __init__(self, model='gpt-3.5-turbo-1106', model_type='text', temperature=0.7, verbose=True, retry=3,
                 timeout=15, identifier=""):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.history = collections.OrderedDict()

        self.model = model

        if model_type in ['text', 'image', 'audio']:
            self.model_type = model_type
        else:
            raise ValueError("Invalid model type.")

        try:
            self.url = os.environ['GPT_API_URL']
            self.api_key = os.environ['GPT_API_KEY']
            self.temperature = temperature
            self.retry = retry
            self.client = OpenAI(
                base_url=os.environ['GPT_API_URL'],
                api_key=os.environ['GPT_API_KEY'],
                timeout=timeout,
                max_retries=retry,
            )
        except KeyError:
            print("Please set GPT_API_URL and GPT_API_KEY environment variables.")
            exit()

        self.verbose = verbose

        self.identifier = identifier if identifier != "" else model

    def query(self, *args, **kwargs):
        raise RuntimeError("must implement query method")


class TextGPTModel(BaseOpenAI):
    def __init__(self, model='gpt-3.5-turbo-1106', temperature=0.7, verbose=True, retry=3, timeout=15, identifier=""):
        super().__init__(model=model, model_type='text', temperature=temperature, verbose=verbose, retry=retry,
                         timeout=timeout, identifier=identifier)

    def query(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=self.temperature
        )
        res = response.choices[0].message.content
        self.prompt_tokens += response.usage.prompt_tokens
        self.completion_tokens += response.usage.completion_tokens
        self.history[prompt] = res

        return res


class ImageGPTModel(BaseOpenAI):
    def __init__(self, model='gpt-4-vision-preview', temperature=0.7, verbose=True, retry=3, timeout=15, identifier=""):
        super().__init__(model=model, model_type='image', temperature=temperature, verbose=verbose, retry=retry,
                         timeout=timeout, identifier=identifier)

    def query(self, prompt, image_file_path):
        base64_image = self._encode_image(image_file_path)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=self.temperature
        )
        res = response.choices[0].message.content
        self.prompt_tokens += response.usage.prompt_tokens
        self.completion_tokens += response.usage.completion_tokens
        self.history[prompt] = res

        return res

    def _encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')


class AudioGPTModel(BaseOpenAI):
    def __init__(self, model='whisper-1', temperature=0.7, verbose=True, retry=3, timeout=15, identifier="",
                 chat_model="gpt-3.5-turbo-1106"):
        super().__init__(model=model, model_type='audio', temperature=temperature, verbose=verbose, retry=retry,
                         timeout=timeout, identifier=identifier)
        self.chat_model = chat_model

    def query(self, prompt, audio_file_path):
        audio_file = open(audio_file_path, "rb")

        transcript = self.client.audio.transcriptions.create(
            model=self.model,
            file=audio_file,
            temperature=self.temperature,
        )

        response = self.client.chat.completions.create(
            model=self.chat_model,
            temperature=self.temperature,
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": transcript.text
                }
            ]
        )

        res = response.choices[0].message.content
        self.prompt_tokens += response.usage.prompt_tokens
        self.completion_tokens += response.usage.completion_tokens
        self.history[prompt] = res

        return res, transcript


if __name__ == '__main__':
    # prompt = "你好，你是什么模型，具体是什么型号?"
    # model = TextGPTModel()
    #
    # print(model.query(prompt))

    # prompt = "请概括这里说了什么"
    #
    # audio_file_path = "/Users/liou/Project/LLM/ChainStream/chainstream/llm/tmp/test_audio.wav"
    # model = AudioGPTModel()
    #
    # print(model.query(prompt, audio_file_path))

    prompt = "请描述图片中有几个人物，都是谁"

    image_file_path = "/Users/liou/Project/LLM/ChainStream/chainstream/llm/tmp/test_img.jpeg"

    model = ImageGPTModel()

    print(model.query(prompt, image_file_path))
