from chainstream.interfaces import MemoryInterface


class SequentialMemory(MemoryInterface):
    def __init__(self) -> None:
        super().__init__()
        self.items = []

    def add_item(self, data_item):
        self.items.append(data_item)

    def remove_item(self, data_item):
        if data_item in self.items:
            self.items.remove(data_item)

