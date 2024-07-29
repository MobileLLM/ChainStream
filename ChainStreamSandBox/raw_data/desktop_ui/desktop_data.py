import os
import json
import random
import PIL.Image as Image

random.seed(42)


class DesktopData:
    def __init__(self):
        self.image_path = os.path.join(os.path.dirname(__file__), "images")
        self.xml_path = os.path.join(os.path.dirname(__file__), "xmls")

        self.data = []

        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"Image path {self.image_path} does not exist.")

        if not os.path.exists(self.xml_path):
            raise FileNotFoundError(f"XML path {self.xml_path} does not exist.")

        for image_file in os.listdir(self.image_path):
            if not image_file.endswith(".jpg") and not image_file.endswith(".png") and not image_file.endswith(".jpeg") and not image_file.endswith(".JPG"):
                continue

            self.data.append({
                "image_file": Image.open(os.path.join(self.image_path, image_file)),
                "xml_file": image_file.replace(".jpg", ".xml").replace(".png", ".xml")
            })

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def get_random_sample(self, num_samples=5):
        tmp_list = random.sample(self.data, num_samples)
        return tmp_list


if __name__ == "__main__":
    data = DesktopData()
    print(len(data))
    print(data.get_random_sample())
