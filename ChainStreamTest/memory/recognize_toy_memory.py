import chainstream as cs
from PIL import Image
import os

blue_file = os.path.join(os.path.dirname(__file__), 'toy_img/blue.jpg')
red_file = os.path.join(os.path.dirname(__file__), 'toy_img/red.jpg')
pig_file = os.path.join(os.path.dirname(__file__), 'toy_img/pig.jpg')
yellow_file = os.path.join(os.path.dirname(__file__), 'toy_img/yellow.jpg')
moss_file = os.path.join(os.path.dirname(__file__), 'toy_img/moss.jpg')


def set_toy_memory():
    # 存储图像文件路径而不是Image对象，因为Image对象无法序列化为JSON
    toy_list = [('悲伤小蓝', blue_file),
                ('小猪', pig_file),
                ('小黄鸭', yellow_file),
                ]

    memory = cs.memory.create_memory('known_toy', type='kv')
    for toy in toy_list:
        memory.add_item({'name': toy[0], 'img_path': toy[1]})


if __name__ == '__main__':
    set_toy_memory()

    memory = cs.memory.fetch('known_toy')
    print(memory.select_keys(['name', 'img_path']))

