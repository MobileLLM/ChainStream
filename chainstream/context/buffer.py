from chainstream.interfaces import ContextInterface
from collections import deque
import re


class Buffer(ContextInterface):
    """
    Use the `Buffer` module to create data containers if you need to store processed data during task execution. This
    container is a queue where data can be added to the end and retrieved from the front. The main purposes of the
    `Buffer` tool are:
        1. to temporarily store batches within the function used in `.batch(by_func=func)`
        2. to temporarily store data when you need to listen to multiple input streams.

    """

    def __init__(self, maxlen=None, item_type=None):
        self.maxlen = maxlen
        self.item_type = item_type
        self.buffer = deque(maxlen=self.maxlen)

    def append(self, data) -> None:
        """
        Add data to the end of the container. The data can be of any form, including images, text, and audio,
        but needs to be encapsulated in a dictionary format.

        """
        self.buffer.append(data)

    def pop(self):
        """
        Retrieve the data at the front of the container and remove it from the container.
        """
        return self.buffer.popleft()

    def popright(self):
        return self.buffer.pop()

    def get(self, index):
        """
        Retrieve the data at the specified index in the container but do not remove it from the container.
        """
        return self.buffer[index]

    def get_all(self):
        """
        Retrieve all data from the container as a list but do not remove them from the container.
        """
        return list(self.buffer)

    def pop_all(self):
        """
        Retrieve all data from the container as a list and remove them from the container.
        """
        return [self.buffer.popleft() for _ in range(len(self.buffer))]

    def __getitem__(self, index):
        return self.buffer[index]

    def __len__(self):
        return len(self.buffer)


# Old version of Buffer class, will be removed in the future
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
