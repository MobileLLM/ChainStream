from . import openai

chatgpt_inst = None

def get_llm(llm='ChatGPT'):
    if llm == 'ChatGPT':
        if chatgpt_inst is None:
            chatgpt_inst = openai.ChatGPT()
        return chatgpt_inst
    else:
        # TODO support other local LLMs
        raise RuntimeError(f'unknown LLM: {llm}')

def make_prompt(args):
    pass

def parse_response(response, target=None):
    pass

