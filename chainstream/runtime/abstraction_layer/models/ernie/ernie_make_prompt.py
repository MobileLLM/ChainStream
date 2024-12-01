import base64
import os
import time
from abc import abstractmethod

import erniebot
import collections
import logging
from pathlib import Path

from threading import Event

from io import BytesIO
from PIL import Image

logger = logging.getLogger(__name__)

GPT_CONFIG = {
    "url": "",
    "key": os.getenv("ERNIE_API_KEY")
}


class BaseErnie:
    def __init__(self, model='ernie-bot', model_type='text', temperature=0.7, verbose=True, retry=3,
                 timeout=15, identifier=""):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.history = collections.OrderedDict()

        self.model = model

        self.is_working = Event()
        self.is_working.clear()

        erniebot.api_type = 'aistudio'
        erniebot.access_token = GPT_CONFIG['key']

        if model_type in ['text', 'image', 'audio']:
            self.model_type = model_type
        else:
            raise ValueError("Invalid model type.")

        try:
            # self.url = os.environ['GPT_API_URL']
            # self.api_key = os.environ['GPT_API_KEY']
            self.url = GPT_CONFIG['url']
            self.api_key = GPT_CONFIG['key']
            self.temperature = temperature
            self.retry = retry
            # self.client = OpenAI(
            #     base_url=self.url,
            #     api_key=self.api_key,
            #     timeout=timeout,
            #     max_retries=retry,
            # )
        except KeyError:
            print("Please set GPT_API_URL and GPT_API_KEY environment variables.")
            exit()

        self.verbose = verbose

        self.identifier = identifier if identifier != "" else model

    def query(self, *args, **kwargs):
        res = None
        error = None
        try:
            self.is_working.set()
            res = self.query_impl(*args, **kwargs)
            self.is_working.clear()
            # print(res)
        except Exception as e:
            if self.is_working.is_set():
                self.is_working.clear()
            error = e
            raise e
        else:
            return res
        finally:
            if self.is_working.is_set():
                self.is_working.clear()
            from chainstream.sandbox_recorder import SANDBOX_RECORDER
            import inspect
            if SANDBOX_RECORDER is not None:
                inspect_stack = inspect.stack()
                SANDBOX_RECORDER.record_query(args, kwargs, res, error, inspect_stack)

    def query_impl(self, prompt_message) -> str:
        raise RuntimeError("must implement query method")


class TextGPTModel(BaseErnie):
    def __init__(self, model='ernie-bot', temperature=0.7, verbose=True, retry=3, timeout=15, identifier=""):
        super().__init__(model=model, model_type='text', temperature=temperature, verbose=verbose, retry=retry,
                         timeout=timeout, identifier=identifier)

    def query_impl(self, prompt_message) -> str:
        tmp_prompt = []
        if type(prompt_message) == list:
            for part in prompt_message:
                tmp_prompt.append({
                    "role": "user",
                    "content": part['content'][0]['text'],
                })
        else:
            tmp_prompt = prompt_message
        response = erniebot.ChatCompletion.create(
            model=self.model,
            messages=tmp_prompt,
            # temperature=self.temperature
        )
        res = response["result"]
        self.history[str(prompt_message)] = res  # 将 prompt_message 转换为字符串

        return res


if __name__ == '__main__':
    from chainstream.llm import make_prompt

    prompt = "你好，你是什么模型，具体是什么型号?"
    model = TextGPTModel()

    print(model.query(make_prompt(prompt)))

    # prompt = "请概括这里说了什么"
    #
    # audio_file_path = "/Users/liou/Project/LLM/ChainStream/chainstream/llm/tmp_img/test_audio.wav"
    # model = AudioGPTModel()
    #
    # print(model.query(prompt, audio_file_path))

    # prompt = "第一张图片中的动画片有再次出现在后面其他图片中吗"
    #
    # image_file_path1 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img.jpeg")
    # image_file_path2 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img2.jpeg")
    # image_file_path3 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img3.jpg")
    # image_file_path4 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img4.jpeg")
    # image_file_path5 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img5.jpeg")
    #
    # model = ImageGPTModel()

    # print(model.query(prompt, [image_file_path1, image_file_path2,
    #                            image_file_path1, image_file_path2,
    #                            image_file_path1, image_file_path2,
    #                            image_file_path1, image_file_path2,
    #                            image_file_path1, image_file_path2,
    #                            image_file_path3, image_file_path3,
    #                            image_file_path3, image_file_path3,
    #                            image_file_path4, image_file_path4,
    #                            image_file_path4, image_file_path4,
    #                            image_file_path5, image_file_path5,
    #                            image_file_path5, image_file_path5,
    #                            ]))
    # print(model.query(prompt, [image_file_path1, image_file_path2,
    #                            image_file_path3, image_file_path4,
    #                            image_file_path5
    #                            ]))
    # print(str(model.query(make_prompt(prompt, image_file_path1, image_file_path2))))
