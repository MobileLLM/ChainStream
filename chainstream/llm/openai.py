import os
import collections
import json
import requests
from chainstream.interfaces import LLM_Interface


class ChatGPT(LLM_Interface):
    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.history = collections.OrderedDict()

    # gpt-3.5-turbo-1106, gpt-4-1106-preview
    def query(self, prompt, model='gpt-3.5-turbo-1106', url=os.environ['GPT_API_URL'], api_key=os.environ['GPT_API_KEY'], temperature=0.7, verbose=True):
        body = {'model':model, 'messages':[{'role':'user','content':prompt}], 'temperature': temperature}
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}', }
        if verbose:
            print(f'-------- GPT query ---------\n{prompt}')
        if prompt in self.history:
            r_content = self.history[prompt]
        else:
            response = requests.post(url=url, json=body, headers=headers)
            r = json.loads(response.content)
            r_content = r['choices'][0]['message']['content']
            self.prompt_tokens += r['usage']['prompt_tokens']
            self.completion_tokens += r['usage']['completion_tokens']
            self.history[prompt] = r_content
        if verbose:
            print(f'-------- GPT response ---------\n{r_content}')
        return r_content


if __name__ == '__main__':
    chatbot = ChatGPT()
    while True:
        prompt = input('Prompt: ')
        response = chatbot.query(prompt)
