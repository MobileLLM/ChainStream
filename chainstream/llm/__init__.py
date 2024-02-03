_model_instances = {}

def get_model(name='gpt3.5'):
    if name in _model_instances and _model_instances[name] is not None:
        return _model_instances[name]
    if name == 'gpt3.5':
        from . import request_base_openai
        inst = openai.ChatGPT()
    else:
        # TODO support other local LLMs
        raise RuntimeError(f'unknown LLM: {name}')
    _model_instances[name] = inst
    return inst

def make_prompt(args):
    pass

def parse_response(response, target=None):
    pass

