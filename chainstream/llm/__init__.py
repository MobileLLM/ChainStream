from utils import convert_audio_to_text, convert_image_to_base64
from PIL import Image
import os

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

def make_prompt(*args, system_prompt=None):
    '''
    args:
    - string: user input
    - PIL.Image: user image
    - audio file path string: user audio file
    - image file path string: user image file
    - list: [user image, user audio]
    
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
    
        if isinstance(arg, str) and not os.path.isfile(arg):
            user_content.append({
                "type": "text",
                "text": arg
            })
        elif isinstance(arg, Image.Image) or (isinstance(arg, str) and arg.split('.')[-1].lower() in ['jpg', 'png', 'jpeg']):
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
            if isinstance(arg[0], Image.Image) or (isinstance(arg[0], str) and arg[0].split('.')[-1].lower() in ['jpg', 'png', 'jpeg']):
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
        else:
            raise ValueError(f'unsupported type: {type(arg)}')
    message_prompt.append({
        "role": "user",
        "content": user_content
    })
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
