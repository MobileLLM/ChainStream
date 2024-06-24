from .make_prompt import make_prompt
from chainstream.runtime import cs_server_core


_model_interfaces = {}

API_LLM_TYPE = {
    "T": ['text'],
    "TI": ['text', 'image'],
    "TA": ['text', 'audio'],
    "TIA": ['text', 'image', 'audio']
}


def get_model(agent, type=['text']):
    """
    type: model type, can be 'text', 'image', 'audio'
        - ['text']
        - ['text', 'image']
        - ['text', 'audio']
        - ['text', 'image', 'audio']

    :param agent:
    :param type:
    :return:
    """

    if type is None or type is [] or not all(n in ['text', 'image', 'audio'] for n in type):
        raise ValueError(f'invalid name: {type}')

    if type.sort() == ['text'].sort():
        from .llm_interface import LLMTextInterface
        inst = LLMTextInterface(agent)
    elif type.sort() == ['text', 'image'].sort():
        from .llm_interface import LLMTextImageInterface
        inst = LLMTextImageInterface(agent)
    elif type.sort() == ['text', 'audio'].sort():
        from .llm_interface import LLMTextAudioInterface
        inst = LLMTextAudioInterface(agent)
    elif type.sort() == ['text', 'image', 'audio'].sort():
        from .llm_interface import LLMTextImageAudioInterface
        inst = LLMTextImageAudioInterface(agent)
    else:
        raise ValueError(f'invalid name: {type}')

    _model_interfaces[tuple(sorted(type))] = inst

    cs_server_core.register_llm(inst)

    return inst


def parse_response(response, target=None):
    pass


if __name__ == '__main__':
    # test make_prompt
    pass

