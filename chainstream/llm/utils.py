from PIL import Image
import base64
from io import BytesIO
from openai import OpenAI

GPT_CONFIG = {
    "url": "https://tbnx.plus7.plus/v1",
    "key": "sk-Eau4dcC9o9Bo1N3ID4EcD394F15b4c029bBaEfA9D06b219b"
}

# GPT_CONFIG = {
#     "url": "https://api.openai-proxy.org/v1",
#     "key": "sk-43Kn6GuGNxD0KwGB1XgiEyQ8htVDan44XXdnQqXA7VkZ7sMI"
# }


def convert_audio_to_text(audio_path, model="whisper-1", temperature=0.9):
    client = OpenAI(api_key=GPT_CONFIG["key"], api_endpoint=GPT_CONFIG["url"])
    audio_file = open(audio_path, "rb")
    transcript = client.audio.transcriptions.create(
        model=model,
        file=audio_file,
        temperature=temperature,
    )
    return transcript.text


def convert_text_to_audio(text, model="davinci-tts", temperature=0.9, output_file="output.wav"):
    client = OpenAI(api_key=GPT_CONFIG["key"], api_endpoint=GPT_CONFIG["url"])
    response = client.text_to_speech(
        text=text,
        voice=model,
        temperature=temperature,
        output_format="wav"
    )
    with open(output_file, "wb") as f:
        f.write(response.content)

    return output_file


def convert_image_to_base64(image_path):
    pil_image = None
    if isinstance(image_path, str):
        pil_image = Image.open(image_path)
    elif isinstance(image_path, Image.Image):
        pil_image = image_path

    pil_image = _resize_maintain_aspect_ratio(pil_image)
    # Ensure the image is in a supported format
    if pil_image.format is None or pil_image.format.lower() not in ['png', 'jpeg', 'gif', 'webp']:
        # Convert the image to JPEG format, for example
        pil_image = pil_image.convert("RGB")
        image_format = "jpeg"
    else:
        image_format = pil_image.format.lower()

    # Convert PIL Image to BytesIO
    image_bytesio = BytesIO()
    pil_image.save(image_bytesio, format=image_format)

    # Encode the BytesIO as base64
    base64_image = base64.b64encode(image_bytesio.getvalue()).decode('utf-8')
    return f"data:image/{image_format};base64,{base64_image}"


def _resize_maintain_aspect_ratio(image, new_width=512):
    if new_width is None:
        return image

    img = image
    width_percent = (new_width / float(img.size[0]))
    new_height = int((float(img.size[1]) * float(width_percent)))
    resized_img = img.resize((new_width, new_height))
    return resized_img
