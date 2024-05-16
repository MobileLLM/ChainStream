_model_instances = {}

def get_model(name=['text']):
    if name in _model_instances and _model_instances[name] is not None:
        return _model_instances[name]

    if name is [] or not all(n in ['text', 'image', 'audio'] for n in name):
        raise ValueError(f'invalid name: {name}')

    if name == ['text']:
        from chainstream.llm.python_base_openai import TextGPTModel
        inst = TextGPTModel()
    elif 'image' in name and 'audio' not in name:
        from chainstream.llm.python_base_openai import ImageGPTModel
        inst = ImageGPTModel()
    elif 'audio' in name and 'image' not in name:
        from chainstream.llm.python_base_openai import AudioGPTModel
        inst = AudioGPTModel()
    else:
        from chainstream.llm.python_base_openai import AudioImageGPTModel
        inst = AudioImageGPTModel()
    _model_instances[name] = inst
    return inst

def make_prompt(*args, **kwargs):
    pass

def parse_response(response, target=None):
    pass

