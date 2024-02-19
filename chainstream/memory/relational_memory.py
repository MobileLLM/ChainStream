from chainstream.interfaces import MemoryInterface

class RelationalMemory(MemoryInterface):
    def __init__(self, dict_key):
        super().__init__()
        self.dict_key = dict_key
        self.items = []

    def add_item(self, data_item):
        self.items.append(data_item)

    def delete_item(self, data_item):
        if data_item in self.items:
            self.items.remove(data_item)
        else:
            raise ValueError("Item not found in memory")

    def select_keys(self, keys, type='and', none_value=None):
        result = []
        for item in self.items:
            if type == 'and':
                if all(key in item for key in keys):
                    result.append({key: item[key] for key in keys})
            elif type == 'or':
                if any(key in item for key in keys):
                    tmp = {key: item[key] for key in item if key in keys}
                    tmp.update({k: none_value for k in keys if k not in tmp})
                    result.append(tmp)
        return result


if __name__ == '__main__':
    rm = RelationalMemory('id')
    rm.add_item({'id': 1, 'name': 'Alice', 'age': 25})
    rm.add_item({'idd': 2, 'name': 'Bob', 'age': 30})
    rm.add_item({'id': 3, 'namee': 'Charlie', 'age': 35})
    rm.add_item({'idd': 4, 'namee': 'Dave', 'age': 40})
    print(rm.select_keys(['id', 'name'], type='or'))
    print(rm.select_keys(['id', 'name'], type='and'))

