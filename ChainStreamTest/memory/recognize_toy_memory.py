import chainstream as cs
from PIL import Image
import os

blue_file = os.path.join(os.path.dirname(__file__), 'toy_img/blue.jpg')
red_file = os.path.join(os.path.dirname(__file__), 'toy_img/red.jpg')
pig_file = os.path.join(os.path.dirname(__file__), 'toy_img/pig.jpg')
yellow_file = os.path.join(os.path.dirname(__file__), 'toy_img/yellow.jpg')
moss_file = os.path.join(os.path.dirname(__file__), 'toy_img/moss.jpg')


def set_toy_memory():
    # toy_list = [('悲伤小蓝', Image.open(blue_file)),
    #             ('小红鸭', Image.open(red_file)),
    #             ('小猪', Image.open(pig_file)),
    #             ('小黄鸭', Image.open(yellow_file)),
    #             ('moss', Image.open(moss_file))]

    toy_list = [('悲伤小蓝', Image.open(blue_file)),
                ('小猪', Image.open(pig_file)),]

    memory = cs.memory.create('known_toy', type='relational')
    for toy in toy_list:
        memory.add_item({'name': toy[0], 'img': toy[1]})


if __name__ == '__main__':
    set_toy_memory()

    memory = cs.memory.fetch('known_toy')
    print(memory.select_keys(['name', 'img']))

