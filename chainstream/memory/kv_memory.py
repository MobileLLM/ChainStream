import json
from base_memory import BaseMemory, DATABASE_PATH_BASE


class KVMemory(BaseMemory):
    def __init__(self, memory_id, load_from=None):
        super().__init__(memory_id=memory_id)
        self.type = 'kv'
        self.file_path = self.create_json(load_from)

    def create_json(self, load_from=None):
        data = {}
        if load_from is not None:
            try:
                with open(load_from, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                raise RuntimeError(f"Failed to load data from {load_from}: {e}")
        file_path = DATABASE_PATH_BASE + f'/{self.memory_id}.json'
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)

        return file_path

    def __getitem__(self, key):
        return self.find_item([key])

    def load(self, file_path, mode='overwrite'):
        if mode == 'overwrite':
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                with open(self.file_path, 'w') as f:
                    json.dump(data, f)
            except Exception as e:
                raise RuntimeError(f"Failed to load data from {file_path}: {e}")
        elif mode == 'merge':
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                with open(self.file_path, 'r') as f:
                    old_data = json.load(f)
                new_data = {**old_data, **data}
                with open(self.file_path, 'w') as f:
                    json.dump(new_data, f)
            except Exception as e:
                raise RuntimeError(f"Failed to load data from {file_path}: {e}")

    # 规定data
    def add_item(self, data):
        # 定义传进来的数据是字典的形式
        with open(self.file_path, 'r') as file:
            file_data = json.load(file)
        for key, value in data.items():
            file_data[key] = value
        with open(self.file_path, 'w') as file:
            json.dump(file_data, file, indent=4)

    def remove_item(self, keys):
        with open(self.file_path, 'r') as file:
            file_data = json.load(file)
        for key in keys:
            if key in file_data:
                del file_data[key]
        with open(self.file_path, 'w') as file:
            json.dump(file_data, file, indent=4)

    def find_item(self, keys):
        data = {}
        with open(self.file_path, 'r') as file:
            file_data = json.load(file)
        for key in keys:
            if key in file_data:
                data[key] = file_data[key]

        return data


def test_kv():
    kv = KVMemory('test')
    kv.add_item({'name': 'test1', 'img': 'this is a img', 'test_num': 100})
    re = kv.find_item(['name', 'img', 'test_num'])
    print(re)
    kv.remove_item(['img'])
    re = kv.find_item(['img'])
    print(re)

if __name__ == '__main__':
    test_dict = {
        'a': 1,
        'b': 2
    }

    print(f'test_dict: {test_dict}')
