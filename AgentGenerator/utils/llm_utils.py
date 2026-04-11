import base64
import os
import time
from abc import abstractmethod

from openai import OpenAI
import collections
import logging
from pathlib import Path

from io import BytesIO
from PIL import Image
# os.environ["GPT_API_URL"] = "http://localhost:8001/v1"
# os.environ["GPT_API_KEY"] = "empty"
logger = logging.getLogger(__name__)

# GPT_CONFIG = {
#     "url": os.getenv("GPT_API_URL"),
#     "key": os.getenv("GPT_API_KEY")
# }
GPT_CONFIG = {
    "url": os.getenv("GPT_API_URL"),
    "key": os.getenv("GPT_API_KEY")
}

# GPT_CONFIG = {
#     "url": "http://localhost:8001/v1",
#     "key": "EMPTY"
# }
MODEL='/data2/models/Qwen/Qwen3-8B'
# MODEL='gpt-4o'
class BaseOpenAI:
    def __init__(self, model=MODEL, model_type='text', temperature=0.7, verbose=True, retry=3,
                 timeout=15, identifier=""):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.history = []

        self.model = model

        if model_type in ['text', 'image', 'audio']:
            self.model_type = model_type
        else:
            raise ValueError("Invalid model type.")

        try:
            # self.url = os.environ['GPT_API_URL']
            # self.api_key = os.environ['GPT_API_KEY']
            if self.model=='/data2/models/Qwen/Qwen3-8B':
                self.url = "http://localhost:8001/v1"
                self.api_key = "EMPTY"
            else:
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

        self.verbose = verbose

        self.identifier = identifier if identifier != "" else model

    def query(self, *args, **kwargs):
        raise RuntimeError("must implement query method")

    def get_token_count(self):
        return self.prompt_tokens, self.completion_tokens


class TextGPTModel(BaseOpenAI):
    def __init__(self, model=MODEL, temperature=0.7, verbose=True, retry=3, timeout=15, identifier=""):
        super().__init__(model=model, model_type='text', temperature=temperature, verbose=verbose, retry=retry,
                         timeout=timeout, identifier=identifier)

    def query(self, prompt, stop=None):
        # print(self.model)
        if self.model=='/data2/models/Qwen/Qwen3-8B':
            sampling_params = {
                "temperature": self.temperature,
                "top_p": 1,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
                "extra_body":{
                "chat_template_kwargs": {
                    "enable_thinking": False  # 关键参数
                }
                }
            }
        else:
            sampling_params = {
                "temperature": self.temperature,
                "top_p": 1,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
            }   
        if stop is None:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=prompt,
                **sampling_params
                # temperature=self.temperature,
                # top_p=1,
                # frequency_penalty=0.0,
                # presence_penalty=0.0,
                # extra_body={
                # "chat_template_kwargs": {
                #     "enable_thinking": False  # 关键参数
                # }
                # }
              
            )
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=prompt,
                **sampling_params,
                # temperature=self.temperature,
                # top_p=1,
                # frequency_penalty=0.0,
                # presence_penalty=0.0,
                stop=stop
                # extra_body={
                # "chat_template_kwargs": {
                #     "enable_thinking": False  # 关键参数
                # }
                # }
            )
        res = response.choices[0].message.content
        self.prompt_tokens += response.usage.prompt_tokens
        self.completion_tokens += response.usage.completion_tokens
        self.history.append(res)

        return res


if __name__ == '__main__':
    prompt = [{
        "role": "user",
        "content": "tell me a story"
    }]
    model = TextGPTModel(model=MODEL)
    # model = TextGPTModel(model='gpt-4o')
    # model = TextGPTModel(model='qwen-plus')
    print(model.query(prompt))

    # prompt = "请概括这里说了什么"
    #
    # audio_file_path = "/Users/liou/Project/LLM/ChainStream/chainstream/llm/tmp_img/test_audio.wav"
    # model = AudioGPTModel()
    #
    # print(model.query(prompt, audio_file_path))

    # prompt = "第一张图片中的动画片有再次出现在后面其他图片中吗"

    # image_file_path1 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img.jpeg")
    # image_file_path2 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img2.jpeg")
    # image_file_path3 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img3.jpg")
    # image_file_path4 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img4.jpeg")
    # image_file_path5 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img5.jpeg")

    # model = ImageGPTModel()

    # # print(model.query(prompt, [image_file_path1, image_file_path2,
    # #                            image_file_path1, image_file_path2,
    # #                            image_file_path1, image_file_path2,
    # #                            image_file_path1, image_file_path2,
    # #                            image_file_path1, image_file_path2,
    # #                            image_file_path3, image_file_path3,
    # #                            image_file_path3, image_file_path3,
    # #                            image_file_path4, image_file_path4,
    # #                            image_file_path4, image_file_path4,
    # #                            image_file_path5, image_file_path5,
    # #                            image_file_path5, image_file_path5,
    # #                            ]))
    # print(model.query(prompt, [image_file_path1, image_file_path2,
    #                            image_file_path3, image_file_path4,
    #                            image_file_path5
    #                            ]))
