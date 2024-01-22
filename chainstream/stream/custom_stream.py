from chainstream.interfaces import StreamInterface
from .base_stream import BaseStream


class CustomStream(BaseStream):
    def __init__(self) -> None:
        super().__init__()

    def register_listener(self, agent, listener_func):
        pass

    def unregister_listener(self, agent, listener_func=None):
        pass

