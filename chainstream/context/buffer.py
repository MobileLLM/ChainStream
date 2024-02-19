from chainstream.interfaces import ContextInterface
from collections import deque
import re

class BufferContext(ContextInterface):
    def __init__(self, maxlen, item_type):
        self.maxlen = maxlen
        self.item_type = item_type
        self.buffer = deque(maxlen=self.maxlen)

    def add(self, frame):
        self.buffer.append(frame)

    def get(self):
        return self.buffer.popleft()

    def __len__(self):
        return len(self.buffer)


class VideoBuffer(BufferContext):
    def __init__(self, duration):
        super().__init__(maxlen=duration, item_type='video')

    def save(self, item):
        self.add(item)

    def snapshot(self):
        # TODO: need discussion
        return self.get()


class AudioBuffer(BufferContext):
    def __init__(self, duration):
        super().__init__(maxlen=duration, item_type='audio')

    def save(self, item):
        self.add(item)

    def snapshot(self):
        return self.get()


class TextBuffer(BufferContext):
    def __init__(self, max_text_num):
        super().__init__(maxlen=max_text_num, item_type='text')

    def save(self, item):
        self.add(item)

    def read(self):
        return self.get()


class WordBuffer(BufferContext):
    def __init__(self, max_word_num):
        super().__init__(maxlen=max_word_num, item_type='word')

    def save(self, item):
        words = re.split(r",|\n", item)
        for word in words:
            self.add(word)

    def read(self):
        return self.get()


