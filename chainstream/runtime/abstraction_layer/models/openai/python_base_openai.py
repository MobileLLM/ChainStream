# import base64
# import os
# import time
# import random
# from abc import abstractmethod
#
# from openai import OpenAI
# import collections
# import logging
# from pathlib import Path
#
# from io import BytesIO
# from PIL import Image
#
# logger = logging.getLogger(__name__)
#
# GPT_CONFIG = {
#     "url": os.getenv("GPT_API_URL"),
#     "key": os.getenv("GPT_API_KEY")
# }
#
#
# class BaseOpenAI:
#     def __init__(self, model='gpt-3.5-turbo-1106', model_type='text', temperature=0.7, verbose=True, retry=3,
#                  timeout=15, identifier=""):
#         self.prompt_tokens = 0
#         self.completion_tokens = 0
#         self.history = collections.OrderedDict()
#
#         self.model = model
#
#         if model_type in ['text', 'image', 'audio']:
#             self.model_type = model_type
#         else:
#             raise ValueError("Invalid model type.")
#
#         try:
#             # self.url = os.environ['GPT_API_URL']
#             # self.api_key = os.environ['GPT_API_KEY']
#             self.url = GPT_CONFIG['url']
#             self.api_key = GPT_CONFIG['key']
#             self.temperature = temperature
#             self.retry = retry
#             self.client = OpenAI(
#                 base_url=self.url,
#                 api_key=self.api_key,
#                 timeout=timeout,
#                 max_retries=retry,
#             )
#         except KeyError:
#             print("Please set GPT_API_URL and GPT_API_KEY environment variables.")
#             exit()
#
#         self.verbose = verbose
#
#         self.identifier = identifier if identifier != "" else model
#
#     def query(self, *args, **kwargs):
#         raise RuntimeError("must implement query method")
#
#
# class TextGPTModel(BaseOpenAI):
#     def __init__(self, model='gpt-3.5-turbo-1106', temperature=0.7, verbose=True, retry=3, timeout=15, identifier=""):
#         super().__init__(model=model, model_type='text', temperature=temperature, verbose=verbose, retry=retry,
#                          timeout=timeout, identifier=identifier)
#
#     def query(self, prompt):
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=self.temperature
#         )
#         res = response.choices[0].message.content
#         self.prompt_tokens += response.usage.prompt_tokens
#         self.completion_tokens += response.usage.completion_tokens
#         self.history[prompt] = res
#
#         return res
#
#
# class ImageGPTModel(BaseOpenAI):
#     def __init__(self, model='gpt-4-vision-preview', temperature=0.7, verbose=True, retry=3, timeout=15, identifier="",
#                  detail='low', resize_width=512):
#         super().__init__(model=model, model_type='image', temperature=temperature, verbose=verbose, retry=retry,
#                          timeout=timeout, identifier=identifier)
#         self.detail = detail
#         self.resize_width = resize_width
#
#     def query(self, prompt, image_file_paths):
#         if not isinstance(image_file_paths, list):
#             image_file_paths = [image_file_paths]
#         base64_images = [self._encode_image(image_file_path) for image_file_path in image_file_paths]
#         contents = [{
#             "type": "text",
#             "text": prompt
#         }]
#         for base64_image in base64_images:
#             contents.append(
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": base64_image,
#                         "detail": self.detail
#                     }
#                 }
#             )
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=[
#                 {
#                     "role": "user",
#                     "content": contents
#                 }
#             ],
#             temperature=self.temperature,
#             max_tokens=300,
#         )
#         res = response.choices[0].message.content
#         self.prompt_tokens += response.usage.prompt_tokens
#         self.completion_tokens += response.usage.completion_tokens
#         self.history[prompt] = res
#
#         return res
#
#     def _resize_maintain_aspect_ratio(self, image, new_width=None):
#         if new_width is None:
#             if self.resize_width:
#                 new_width = self.resize_width
#             else:
#                 return image
#         img = image
#         width_percent = (new_width / float(img.size[0]))
#         new_height = int((float(img.size[1]) * float(width_percent)))
#         resized_img = img.resize((new_width, new_height))
#         return resized_img
#
#     def _encode_image(self, image_path):
#         pil_image = None
#         if isinstance(image_path, str):
#             pil_image = Image.open(image_path)
#         elif isinstance(image_path, Image.Image):
#             pil_image = image_path
#
#         pil_image = self._resize_maintain_aspect_ratio(pil_image)
#         # Ensure the image is in a supported format
#         if pil_image.format is None or pil_image.format.lower() not in ['png', 'jpeg', 'gif', 'webp']:
#             # Convert the image to JPEG format, for example
#             pil_image = pil_image.convert("RGB")
#             image_format = "jpeg"
#         else:
#             image_format = pil_image.format.lower()
#
#         # Convert PIL Image to BytesIO
#         image_bytesio = BytesIO()
#         pil_image.save(image_bytesio, format=image_format)
#
#         # Encode the BytesIO as base64
#         base64_image = base64.b64encode(image_bytesio.getvalue()).decode('utf-8')
#         return f"data:image/{image_format};base64,{base64_image}"
#
#
# class AudioGPTModel(BaseOpenAI):
#     def __init__(self, model='whisper-1', temperature=0.7, verbose=True, retry=3, timeout=15, identifier="",
#                  chat_model="gpt-3.5-turbo-1106"):
#         super().__init__(model=model, model_type='audio', temperature=temperature, verbose=verbose, retry=retry,
#                          timeout=timeout, identifier=identifier)
#         self.chat_model = chat_model
#
#     def query(self, prompt, audio_file_path):
#         audio_file = open(audio_file_path, "rb")
#
#         transcript = self.client.audio.transcriptions.create(
#             model=self.model,
#             file=audio_file,
#             temperature=self.temperature,
#         )
#
#         response = self.client.chat.completions.create(
#             model=self.chat_model,
#             temperature=self.temperature,
#             messages=[
#                 {
#                     "role": "system",
#                     "content": prompt
#                 },
#                 {
#                     "role": "user",
#                     "content": transcript.text
#                 }
#             ]
#         )
#
#         res = response.choices[0].message.content
#         self.prompt_tokens += response.usage.prompt_tokens
#         self.completion_tokens += response.usage.completion_tokens
#         self.history[prompt] = res
#
#         return res, transcript
#
#
# # TODO: finish and test this model
# class AudioImageGPTModel(BaseOpenAI):
#     def __init__(self, model='whisper-1', temperature=0.7, verbose=True, retry=3, timeout=15, identifier="",
#                  chat_model="gpt-4-vision-preview"):
#         super().__init__(model=model, model_type='audio', temperature=temperature, verbose=verbose, retry=retry,
#                          timeout=timeout, identifier=identifier)
#         self.chat_model = chat_model
#
#     def query(self, prompt, audio_file_path):
#         audio_file = open(audio_file_path, "rb")
#
#         transcript = self.client.audio.transcriptions.create(
#             model=self.model,
#             file=audio_file,
#             temperature=self.temperature,
#         )
#
#         response = self.client.chat.completions.create(
#             model=self.chat_model,
#             temperature=self.temperature,
#             messages=[
#                 {
#                     "role": "system",
#                     "content": prompt
#                 },
#                 {
#                     "role": "user",
#                     "content": transcript.text
#                 }
#             ]
#         )
#
#         res = response.choices[0].message.content
#         self.prompt_tokens += response.usage.prompt_tokens
#         self.completion_tokens += response.usage.completion_tokens
#         self.history[prompt] = res
#
#         return res, transcript
#
#
# if __name__ == '__main__':
#     # prompt = "你好，你是什么模型，具体是什么型号?"
#     # model = TextGPTModel()
#     #
#     # print(model.query(prompt))
#
#     # prompt = "请概括这里说了什么"
#     #
#     # audio_file_path = "/Users/liou/Project/LLM/ChainStream/chainstream/llm/tmp_img/test_audio.wav"
#     # model = AudioGPTModel()
#     #
#     # print(model.query(prompt, audio_file_path))
#
#     prompt = "第一张图片中的动画片有再次出现在后面其他图片中吗"
#
#     image_file_path1 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img.jpeg")
#     image_file_path2 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img2.jpeg")
#     image_file_path3 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img3.jpg")
#     image_file_path4 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img4.jpeg")
#     image_file_path5 = os.path.join(Path(__file__).parent.parent.parent, "ChainStreamTest/llm/tmp_img/test_img5.jpeg")
#
#     model = ImageGPTModel()
#
#     # print(model.query(prompt, [image_file_path1, image_file_path2,
#     #                            image_file_path1, image_file_path2,
#     #                            image_file_path1, image_file_path2,
#     #                            image_file_path1, image_file_path2,
#     #                            image_file_path1, image_file_path2,
#     #                            image_file_path3, image_file_path3,
#     #                            image_file_path3, image_file_path3,
#     #                            image_file_path4, image_file_path4,
#     #                            image_file_path4, image_file_path4,
#     #                            image_file_path5, image_file_path5,
#     #                            image_file_path5, image_file_path5,
#     #                            ]))
#     print(model.query(prompt, [image_file_path1, image_file_path2,
#                                image_file_path3, image_file_path4,
#                                image_file_path5
#                                ]))
