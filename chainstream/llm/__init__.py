from .utils import convert_audio_to_text, convert_image_to_base64
from PIL import Image
from chainstream.context import Buffer
import os
import inspect
import warnings

_model_instances = {}


def reset_model_instances():
    """
    Reset all model instances, used for runtime or sandbox restarting
    """
    global _model_instances
    for k in list(_model_instances.keys()):
        del _model_instances[k]
    _model_instances = {}


def check_has_model_working():
    """
    Check if all model instances message queue is empty, used for sandbox judging the end of the simulation
    """
    global _model_instances
    for k in list(_model_instances.keys()):
        if _model_instances[k].is_working.is_set():
            return True
    return False

API_LLM_TYPE = {
    "T": ['text'],
    "TI": ['text', 'image'],
    "TA": ['text', 'audio'],
    "TIA": ['text', 'image', 'audio']
}


def get_model(llm_type=['text']):
    '''
    `chainstream.llm.get_model(List[Union[Literal["text", "image", "audio"]]]) -> chainstream.llm.LLM`: Instantiate
    an `LLM` object to obtain a model for data processing. The parameter specifies the types of data the model needs
    to handle.

    llm_type: list of model llm_type, e.g. ['text', 'image', 'audio']
    '''

    if llm_type is None:
        raise ValueError('llm_type cannot be None')
    if not isinstance(llm_type, list) and not isinstance(llm_type, str):
        raise ValueError(f'invalid llm_type type: {type(llm_type)}, must be a list or string')
    if isinstance(llm_type, list) and llm_type == []:
        raise ValueError('llm_type cannot be an empty list')

    if isinstance(llm_type, str):
        if llm_type.lower() not in ['text', 'image', 'audio']:
            raise ValueError(f'invalid llm_type name: {llm_type}, must be one of text, image, audio')
        llm_type = [llm_type.lower()]

    llm_type = list(set(llm_type))

    if tuple(sorted(llm_type)) in _model_instances and _model_instances[tuple(sorted(llm_type))] is not None:
        return _model_instances[tuple(sorted(llm_type))]

    if llm_type is [] or not all(n in ['text', 'image', 'audio'] for n in llm_type):
        raise ValueError(f'invalid name: {llm_type}')

    if llm_type == ['text']:
        if os.getenv('ERNIE_API_KEY') is not None:
            from chainstream.runtime.abstraction_layer.models.ernie.ernie_make_prompt import TextGPTModel
        elif os.getenv('GPT_API_KEY') is None:
            from chainstream.runtime.abstraction_layer.models.openai.python_base_openai_make_prompt import TextGPTModel
        inst = TextGPTModel()
    elif 'image' in llm_type and 'audio' not in llm_type:
        from chainstream.runtime.abstraction_layer.models.openai.python_base_openai_make_prompt import ImageGPTModel
        inst = ImageGPTModel()
    elif 'audio' in llm_type and 'image' not in llm_type:
        from chainstream.runtime.abstraction_layer.models.openai.python_base_openai_make_prompt import AudioGPTModel
        inst = AudioGPTModel()
    else:
        from chainstream.runtime.abstraction_layer.models.openai.python_base_openai_make_prompt import AudioImageGPTModel
        inst = AudioImageGPTModel()

    from chainstream.sandbox_recorder import SANDBOX_RECORDER
    if SANDBOX_RECORDER is not None:
        inspect_stack = inspect.stack()
        SANDBOX_RECORDER.record_get_model(inst.__class__.__name__, inspect_stack)

    _model_instances[tuple(sorted(llm_type))] = inst
    return inst


def make_prompt(*args, system_prompt=None):
    '''
    `chainstream.llm.make_prompt(Union[Literal['str'], dict, chainstream.context.Buffer]) -> str`: Process and
    concatenate all input parameters, converting dictionaries and Buffer contents to strings, and returning a single
    prompt string.

    Note that the `make_prompt` method only directly processes and concatenates all input content
    without any additional processing, you must provide a task description prompt for LLM to describe your processing
    needs in detail.

    args:
    - string: user input
    - PIL.Image: user image
    - audio file path string: user audio file
    - image file path string: user image file
    - list: [user image, user audio]
    - buffer: user input buffer
    
    usage:
    text_prompt = make_prompt("can you tell me a joke?")
    image_prompt = make_prompt("front camera shot is here", image)
    image_prompt = make_prompt("front camera shot is here", "image.jpg")
    image_prompt = make_prompt("front camera shot is here", [image1, image2])
    audio_prompt = make_prompt("audio recording is here", audio)
    audio_image_prompt = make_prompt("front camera shot is here", image, "audio recording is here", audio)

    '''
    message_prompt = []
    if system_prompt is not None:
        if not isinstance(system_prompt, str):
            raise ValueError(f'system_prompt must be a string, got {type(system_prompt)}')
        message_prompt.append({
            "role": "system",
            "content": system_prompt
        })
    user_content = []
    for arg in args:
        if isinstance(arg, Buffer):
            arg = arg.get_all()
        if isinstance(arg, str) and not os.path.isfile(arg):
            user_content.append({
                "type": "text",
                "text": arg
            })
        elif isinstance(arg, Image.Image) or (
                isinstance(arg, str) and arg.split('.')[-1].lower() in ['jpg', 'png', 'jpeg']):
            user_content.append({
                "type": "image_url",
                "image_url": {
                    'url': convert_image_to_base64(arg)
                }
            })
        elif isinstance(arg, str) and arg.split('.')[-1].lower() in ['wav', 'flac', 'mp3']:
            user_content.append({
                "type": "text",
                "text": convert_audio_to_text(arg)
            })
        elif isinstance(arg, list):
            # check if all elements are same type
            if not all(isinstance(a, type(arg[0])) for a in arg):
                raise ValueError(f'all elements must be of the same type, got {type(arg[0])}')
            if arg is None or len(arg) == 0:
                warnings.warn("your argument is empty, please provide at least one element")
                continue
            if isinstance(arg[0], Image.Image) or (
                    isinstance(arg[0], str) and arg[0].split('.')[-1].lower() in ['jpg', 'png', 'jpeg']):
                for a in arg:
                    user_content.append({
                        "type": "image_url",
                        "image_url": {
                            'url': convert_image_to_base64(a)
                        }
                    })
            elif isinstance(arg[0], str) and arg[0].split('.')[-1].lower() in ['wav', 'flac', 'mp3']:
                for a in arg:
                    user_content.append({
                        "type": "text",
                        "text": convert_audio_to_text(a)
                    })
        elif isinstance(arg, dict):
            user_content.append({
                "type": "text",
                "text": str(arg),
            })
        else:
            raise ValueError(f'unsupported type: {type(arg)}')
    message_prompt.append({
        "role": "user",
        "content": user_content
    })

    from chainstream.sandbox_recorder import SANDBOX_RECORDER
    if SANDBOX_RECORDER is not None:
        inspect_stack = inspect.stack()
        input_args = [str(a) for a in args]
        prompt = message_prompt

        SANDBOX_RECORDER.record_make_prompt(prompt, input_args, inspect_stack)

    return message_prompt


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
