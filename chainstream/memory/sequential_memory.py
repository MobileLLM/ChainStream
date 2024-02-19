from chainstream.interfaces import MemoryInterface


class SequentialMemory(MemoryInterface):
    def __init__(self, memory_id) -> None:
        super().__init__()
        self.memory_id = memory_id
        self.items = []

    def add_item(self, data_item):
        self.items.append(data_item)

    def remove_item(self, data_item):#移除元素
        if data_item in self.items:
            self.items.remove(data_item)
        else:
            raise ValueError("The data item does not exist")

    def change_item(self,old_item,new_item):#修改元素
        if old_item in self.items:
            index = self.items.index(old_item)
            self.items[index] = new_item
        else:
            raise ValueError("The data item does not exist")

    def read_item(self,index):#读任意元素
        if index < len(self.items):
            return self.items[index]

    def get_item(self):#获取第一个元素
        if len(self.items)>0:
            first_item=self.items.pop(0)
            return first_item
        else:
            raise ValueError("No data item exists")


