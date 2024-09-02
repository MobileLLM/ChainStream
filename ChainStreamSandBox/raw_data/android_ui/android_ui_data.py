import os
import random
import json
import PIL.Image as Image


class AndroidUIData:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'screenshot_data')
        if not os.path.exists(self.data_path):
            raise ValueError("Data path does not exist")

        self.data = []

        self._load_data()

    def _load_data(self):
        file_list = os.listdir(self.data_path)
        info_list = {}
        for file_name in file_list:
            if file_name.endswith('.json'):
                with open(os.path.join(self.data_path, file_name), 'r') as f:
                    info = json.load(f)
                    info_list[file_name.split('.')[0]] = info

        for id, info in info_list.items():
            img_path = os.path.join(self.data_path, id)
            if os.path.exists(img_path + '.png'):
                img_path += '.png'
                img = Image.open(img_path)
            elif os.path.exists(img_path + '.jpg'):
                img_path += '.jpg'
                img = Image.open(img_path)
            else:
                raise ValueError("Image file does not exist")
            self.data.append({
                'activity_name': info['activity_name'],
                'img': img,
                'info': info
            })

    def get_random_data(self, app_num_max=5, repid_max=5):

        res_list = []
        tmp_random = random.Random(42)
        app_num = tmp_random.randint(1, app_num_max)
        app_list = [tmp_random.choice(self.data) for _ in range(app_num)]

        for app in app_list:
            repid_num = tmp_random.randint(1, repid_max)
            res_list.extend([app for _ in range(repid_num)])

        return res_list


if __name__ == '__main__':
    data = AndroidUIData()
    print(data.get_random_data())
