from chainstream.interfaces import StreamInterface
from chainstream.runtime import cs_server_core
import logging
import datetime

class StreamMeta:
    def __init__(self, *args, **kwargs):
        self.stream_id = kwargs.get('stream_id')
        self.description = kwargs.get('description')
        self.create_time = datetime.datetime.now()
        self.create_by = kwargs.get('create_by')


class BaseStream(StreamInterface):
    def __init__(self, stream_id) -> None:
        super().__init__()
        self.stream_id = stream_id
        cs_server_core.register_stream(self)
        self.logger = logging.getLogger(self.stream_id)
        self.listeners = []

    def register_listener(self, agent, listener_func):
        try:
            self.listeners.append((agent.agent_id, listener_func))
        except Exception as e:
            print("Error registering listener: ", e)

    def unregister_listener(self, agent, listener_func=None):
        new_listeners = []
        for agent_, listener_func_ in self.listeners:
            if agent_ != agent.agent_id:
                new_listeners.append((agent_, listener_func_))
            elif listener_func is not None and listener_func_ == listener_func:
                new_listeners.append((agent_, listener_func_))
        self.listeners = new_listeners

    def send_item(self, item):
        self.logger.info(f'stream {self.stream_id} send an item type: {type(item)}')
        for agent_, listener_func_ in self.listeners:
            listener_func_(item)

