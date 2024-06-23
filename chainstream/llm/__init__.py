from .make_prompt import make_prompt
from chainstream.runtime import cs_server_core


_model_interfaces = {}


def get_model(agent, type=['text']):

    # TODO: we need new model type check here
    # if type is [] or not all(n in ['text', 'image', 'audio'] for n in type):
    #     raise ValueError(f'invalid name: {type}')

    if type == ['text']:
        from .llm_interface import LLMTextInterface
        inst = LLMTextInterface(agent)

    _model_interfaces[tuple(sorted(type))] = inst

    cs_server_core.register_llm(agent, inst)

    return inst


def parse_response(response, target=None):
    pass


if __name__ == '__main__':
    # test make_prompt
    pass

