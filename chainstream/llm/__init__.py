_model_instances = {}

def get_model(name='gpt-3.5'):
    if name in _model_instances and _model_instances[name] is not None:
        return _model_instances[name]
    if name == 'gpt-3.5':
        from chainstream.llm.python_base_openai import TextGPTModel
        inst = TextGPTModel()
    elif name == 'gpt-4-vision':
        from chainstream.llm.python_base_openai import ImageGPTModel
        inst = ImageGPTModel()
    elif name == 'gpt-audio':
        from chainstream.llm.python_base_openai import AudioGPTModel
        inst = AudioGPTModel()
    else:
        # TODO support other local LLMs
        raise RuntimeError(f'unknown LLM: {name}')
    _model_instances[name] = inst
    return inst

def make_prompt(args):
    pass

def parse_response(response, target=None):
    pass

