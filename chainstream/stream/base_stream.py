from chainstream.interfaces import StreamInterface
from chainstream.runtime import cs_server
import logging


class BaseStream(StreamInterface):
    def __init__(self, stream_id) -> None:
        super().__init__()
        self.stream_id = stream_id
        cs_server.register_stream(self)
        self.logger = logging.getLogger(self.stream_id)
        self.listeners = []

    def register_listener(self, agent, listener_func):
        self.listeners.append[(agent, listener_func)]

    def unregister_listener(self, agent, listener_func=None):
        new_listeners = []
        for agent_, listener_func_ in self.listeners:
            if agent_ != agent:
                new_listeners.append((agent_, listener_func_))
            elif listener_func is not None and listener_func_ == listener_func:
                new_listeners.append((agent_, listener_func_))
        self.listeners = new_listeners

    def send_item(self, item):
        self.logger.info(f'stream {self.stream_id} send an item {item}')
        for agent_, listener_func_ in self.listeners:
            listener_func_(item)

