from .make_prompt import make_prompt

_model_instances = {}


def get_model(type=['text']):
    '''
    name: list of model type, e.g. ['text', 'image', 'audio']
    '''
    if tuple(sorted(type)) in _model_instances and _model_instances[tuple(sorted(type))] is not None:
        return _model_instances[tuple(sorted(type))]

    if type is [] or not all(n in ['text', 'image', 'audio'] for n in type):
        raise ValueError(f'invalid name: {type}')

    if type == ['text']:
        from chainstream.runtime.abstraction_layer.models.openai.python_base_openai_make_prompt import TextGPTModel
        inst = TextGPTModel()
    elif 'image' in type and 'audio' not in type:
        from chainstream.runtime.abstraction_layer.models.openai.python_base_openai_make_prompt import ImageGPTModel
        inst = ImageGPTModel()
    elif 'audio' in type and 'image' not in type:
        from chainstream.runtime.abstraction_layer.models.openai.python_base_openai_make_prompt import AudioGPTModel
        inst = AudioGPTModel()
    else:
        from chainstream.runtime.abstraction_layer.models.openai.python_base_openai_make_prompt import AudioImageGPTModel
        inst = AudioImageGPTModel()

    _model_instances[tuple(sorted(type))] = inst
    return inst


def parse_response(response, target=None):
    pass


if __name__ == '__main__':
    # test make_prompt
    text_prompt = make_prompt("can you tell me a joke?")
    image_prompt = make_prompt("front camera shot is here", "image.jpg")
    audio_prompt = make_prompt("audio recording is here", "audio.wav")
    audio_image_prompt = make_prompt("front camera shot is here", "image.jpg", "audio recording is here", "audio.wav")
    print(text_prompt)
    print(image_prompt)
    print(audio_prompt)
    print(audio_image_prompt)

    # test get_model
    text_model = get_model(['text'])
    image_model = get_model(['image'])
    audio_model = get_model(['audio'])
    audio_image_model = get_model(['image', 'audio'])
    print(text_model)
    print(image_model)
    print(audio_model)
    print(audio_image_model)
