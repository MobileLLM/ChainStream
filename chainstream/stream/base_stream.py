from chainstream.interfaces import StreamInterface
from chainstream.runtime import cs_server_core
from .stream_recorder import StreamRecorder
import logging
import datetime
import queue
import threading


class StreamMeta:
    def __init__(self, *args, **kwargs):
        self.stream_id = kwargs.get('stream_id')
        self.description = kwargs.get('description')
        self.create_time = datetime.datetime.now()
        self.create_by = kwargs.get('create_by')


class BaseStream(StreamInterface):
    def __init__(self, stream_id, description=None, create_by=None) -> None:
        super().__init__()
        self.metaData = StreamMeta(stream_id=stream_id, description=description, create_by=create_by)
        self.logger = logging.getLogger(self.metaData.stream_id)
        self.listeners = []
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.process_item)
        cs_server_core.register_stream(self)
        self.recorder = StreamRecorder(self.metaData, self.queue)

    def register_listener(self, agent, listener_func):
        try:
            self.listeners.append((agent.agent_id, listener_func))
            self.recorder.record_listener_change(len(self.listeners))
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
        self.recorder.record_listener_change(len(self.listeners))

    def send_item(self, item):
        self.logger.info(f'stream {self.metaData.stream_id} send an item type: {type(item)}')
        self.queue.put(item)
        self.recorder.record_new_item()

    def process_item(self, item):
        self.logger.info(f'stream {self.metaData.stream_id} process an item type: {type(item)}')
        while True:
            item = self.queue.get()
            if item is not None:
                for agent_, listener_func_ in self.listeners:
                    listener_func_(item)
                    self.recorder.record_send_item(agent_)

    def get_record_data(self):
        return self.recorder.get_record_data()
