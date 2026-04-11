# import os
# import time
# import random
#
# import openai
# import collections
# import logging
#
# logger = logging.getLogger(__name__)
#
#
# class BaseOpenAI:
#     def __init__(self, model='gpt-3.5-turbo-1106', model_type='text', temperature=0.7, verbose=True, retry=3,
#                  timeout=15, identifier=""):
#         self.prompt_tokens = 0
#         self.completion_tokens = 0
#         self.history = collections.OrderedDict()
#
#         if model_type in ['text', 'image', 'audio']:
#             self.model_type = model_type
#         else:
#             raise ValueError("Invalid model type.")
#
#         self.model = model
#         self.temperature = temperature
#         self.verbose = verbose
#
#         try:
#             self.url = os.environ['GPT_API_URL']
#             self.api_key = os.environ['GPT_API_KEY']
#             openai.api_key = self.api_key
#             openai.api_base = self.url
#         except KeyError:
#             print("Please set GPT_API_URL and GPT_API_KEY environment variables.")
#             exit()
#
#         self.retry = retry
#         self.timeout = timeout
#
#         self.identifier = identifier if identifier != "" else model
#
#     def query(self, prompt):
#         tmp_retry = 0
#         while tmp_retry < self.retry:
#             try:
#                 res = self.single_query(prompt)
#                 break
#             except:
#                 tmp_retry += 1
#                 logger.debug(f"Task {self.identifier} retry {tmp_retry} times.")
#             time.sleep(random.uniform(0.5 + 1 * tmp_retry, 1.5 + 1 * tmp_retry))
#         else:
#             logger.debug(f"Task {self.identifier} fails.")
#             return None
#         return res
#
#
# class TextGPTModel(BaseOpenAI):
#     def __init__(self, model='gpt-3.5-turbo-1106', temperature=0.7, verbose=True, retry=3, timeout=15, identifier=""):
#         super().__init__(model=model, model_type='text', temperature=temperature, verbose=verbose, retry=retry,
#                          timeout=timeout, identifier=identifier)
#
#     def single_query(self, prompt):
#         response = openai.ChatCompletion.create(
#             engine=self.model,
#             prompt=prompt,
#             temperature=self.temperature,
#             timeout=self.timeout,
#             message=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ]
#         )
#         res = response["choices"][0]["message"]["content"]
#         self.prompt_tokens += response['usage']['prompt_tokens']
#         self.completion_tokens += response['usage']['completion_tokens']
#         self.history[prompt] = res
#
#         return res
#
#
# class ImageGPTModel(BaseOpenAI):
#     def __init__(self, model='gpt-4-vision-preview', temperature=0.7, verbose=True, retry=3, timeout=15, identifier=""):
#         super().__init__(model=model, model_type='image', temperature=temperature, verbose=verbose, retry=retry,
#                          timeout=timeout, identifier=identifier)
#
#     def single_query(self, prompt):
#         response = openai.ChatCompletion.create(
#             engine=self.model,
#             prompt=prompt,
#             temperature=self.temperature,
#             timeout=self.timeout,
#             message=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ]
#         )
#         res = response["choices"][0]["text"]
#         self.prompt_tokens += response['usage']['prompt_tokens']
#         self.completion_tokens += response['usage']['completion_tokens']
#         self.history[prompt] = res
#
#         return res
#
#
# class AudioGPTModel(BaseOpenAI):
#     def __init__(self, model='whisper-1', temperature=0.7, verbose=True, retry=3, timeout=15, identifier=""):
#         super().__init__(model=model, model_type='audio', temperature=temperature, verbose=verbose, retry=retry,
#                          timeout=timeout, identifier=identifier)
#
#     def single_query(self, prompt):
#         response = openai.ChatCompletion.create(
#             engine=self.model,
#             prompt=prompt,
#             temperature=self.temperature,
#             timeout=self.timeout,
#             message=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#
#             ]
#
#         )
#
#         res = response["choices"][0]["text"]
#         self.prompt_tokens += response['usage']['prompt_tokens']
#
#
# if __name__ == '__main__':
#     prompt = "你好，你是什么模型?"
#     textgpt = TextGPTModel()
#     res = textgpt.single_query(prompt)
#     print(res)
