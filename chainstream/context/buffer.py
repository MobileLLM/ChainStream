from chainstream.interfaces import ContextInterface
from collections import deque
import re


class Buffer(ContextInterface):
    def __init__(self, maxlen=None, item_type=None):
        self.maxlen = maxlen
        self.item_type = item_type
        self.buffer = deque(maxlen=self.maxlen)

    def append(self, data):
        self.buffer.append(data)

    def pop(self):
        return self.buffer.popleft()

    def popright(self):
        return self.buffer.pop()

    def get(self, index):
        return self.buffer[index]

    def get_all(self):
        return list(self.buffer)

    def pop_all(self):
        return [self.buffer.popleft() for _ in range(len(self.buffer))]

    def __getitem__(self, index):
        return self.buffer[index]

    def __len__(self):
        return len(self.buffer)


class AudioBuffer(Buffer):
    def __init__(self, duration=None):
        super().__init__(maxlen=duration, item_type='audio')

    def snapshot(self):
        return self.get_all()


class TextBuffer(Buffer):
    def __init__(self, max_text_num=None):
        super().__init__(maxlen=max_text_num, item_type='text')

    def read(self):
        return self.get_all()


class ImageBuffer(Buffer):
    def __init__(self, max_image_num=None):
        super().__init__(maxlen=max_image_num, item_type='image')

    def read(self):
        return self.get_all()
