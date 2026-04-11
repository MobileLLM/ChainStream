from chainstream.context import Buffer
from PIL import Image
from chainstream.llm.utils import convert_audio_to_text, convert_image_to_base64
import os


def make_prompt(*args, system_prompt=None):
    """
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
    """
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
        else:
            raise ValueError(f'unsupported type: {type(arg)}')
    message_prompt.append({
        "role": "user",
        "content": user_content
    })
    return message_prompt
