from chainstream.interfaces import MemoryInterface
import cv2


class KV_Memory(MemoryInterface):
    def __init__(self, dict_key) -> None:
        super().__init__()
        self.name = dict_key  # known_people
        self.items = {}

    # add or change
    def add_item(self, data_item):
        self.items[data_item[0]] = data_item[1]

    def delete_item(self, data_key):
        if data_key in self.items.keys():
            del self.items[data_key]
        else:
            print('there is no ' + str(data_key))
            raise RuntimeError("Item not found")

    def find_item(self, data_key):
        if data_key in self.items.keys():
            return self.items[data_key]
        else:
            print('there is no ' + str(data_key))
            return None

    def get_keys(self):
        return self.items.keys()


def main():
    image = cv2.imread('image.jpeg')
    temp = KV_Memory('known_people')
    temp.add_item('face', image)
    temp.add_item('name', 'image')
    print(temp.get_keys())
    image_1 = temp.find_item('face')
    temp.delete_item('name')
    print(temp.get_keys())
    temp.find_item('name')
    print(temp.get_keys())


if __name__ == "__main__":
    main()
