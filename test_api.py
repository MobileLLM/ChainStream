
from openai import OpenAI
import base64
from PIL import Image
import requests
from io import BytesIO

# 初始化客户端
client = OpenAI(
    # base_url="http://8.130.122.196:7788/v1",
    # base_url="http://localhost:3000/v1",
    base_url="https://ruyi.wisewk.com/v1",
    api_key="sk-VHvpoWvuAWNyGPBy9dB31e3225E94a7b910c736a91C1C4B0",
)


def test_text_chat():
    """测试纯文本对话"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个有帮助的AI助手。"},
                {"role": "user", "content": "你好，请介绍一下你自己。"}
            ],
            temperature=0.7,
            max_tokens=1024
        )

        # 打印响应
        print("\n=== 文本对话测试 ===")
        print("问题: 你好，请介绍一下你自己。")
        print("回答:", response.choices[0].message.content)
        print("====================\n")

    except Exception as e:
        print("文本对话测试出错:", str(e))


def test_vision_chat():
    """测试视觉对话"""
    try:
        # 加载本地图片
        image_path = "./test_img.jpeg"
        with open(image_path, "rb") as image_file:
            img_str = base64.b64encode(image_file.read()).decode()

        # 发送请求
        response = client.chat.completions.create(
            model="ruyillm",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "这张图片里有什么？"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_str}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1024
        )

        # 打印响应
        print("\n=== 视觉对话测试 ===")
        print("问题: 这张图片里有什么？")
        print("回答:", response.choices[0].message.content)
        print("====================\n")

    except Exception as e:
        print("视觉对话测试出错:", str(e))


if __name__ == "__main__":
    # 测试纯文本对话
    test_text_chat()

    # 测试视觉对话
    test_vision_chat()