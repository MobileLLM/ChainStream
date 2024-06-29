from chainstream.interfaces import StreamInterface
from chainstream.runtime import cs_server_core
from .stream_recorder import StreamRecorder
import logging
import datetime
import queue
import threading
import inspect
from threading import Event


class StreamMeta:
    def __init__(self, *args, **kwargs):
        self.stream_id = kwargs.get('stream_id')
        self.description = kwargs.get('description')
        self.create_time = datetime.datetime.now()
        self.create_by_agent_file = kwargs.get('create_by_agent_file')

    def __dict__(self):
        return {
            "stream_id": self.stream_id,
            "description": self.description,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "create_by": self.create_by_agent_file
        }


class BaseStream(StreamInterface):
    STOP_SIGNAL = object()

    def __init__(self, stream_id, description=None, create_by_agent_file=None) -> None:
        super().__init__()
        self.metaData = StreamMeta(stream_id=stream_id, description=description, create_by_agent_file=create_by_agent_file)
        self.logger = logging.getLogger(self.metaData.stream_id)

        self.is_clear = Event()
        self.is_clear.set()

        self.listeners = []
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.process_item)
        self.is_running = False
        self.recorder = StreamRecorder(self.metaData, self.queue)
        cs_server_core.register_stream(self)

    def register_listener(self, agent, listener_func):
        try:
            self.listeners.append((agent.agent_id, listener_func))
            self.recorder.record_listener_actions("register_listener", agent.agent_id, listener_func.__name__)
            self.recorder.record_listener_change(len(self.listeners))
            if not self.is_running:
                self.is_running = True
                self.thread.start()
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
        if len(self.listeners) == 0:
            self.is_running = False
            self.queue.put(self.STOP_SIGNAL)
            self.thread.join()
            # print("No more listeners, stopping stream")

    def add_item(self, item):
        self.logger.debug(f'stream {self.metaData.stream_id} send an item type: {type(item)}')
        self.queue.put(item)
        call_from = inspect.stack()[1]
        self.recorder.record_new_item(call_from.filename, call_from.function)

    def send_item(self, item):
        self.add_item(item)

    def process_item(self):
        while True:
            item = self.queue.get()
            if item is self.STOP_SIGNAL:
                break
            if item is not None:
                self.logger.debug(f'stream {self.metaData.stream_id} process an item type: {type(item)}')
                self.is_clear.clear()
                for agent_, listener_func_ in self.listeners:
                    listener_func_(item)
                    self.recorder.record_send_item(agent_, listener_func_.__name__)
                self.is_clear.set()

    def get_meta_data(self):
        data = self.metaData.__dict__()
        data['listeners'] = [str(agent_) + ":" + str(listener_func_.__name__) for agent_, listener_func_ in self.listeners]
        return data

    def get_record_data(self):
        return self.recorder.get_record_data()

    def shutdown(self):
        self.is_running = False
        # print(self.metaData.stream_id, "Shutting down stream")
        self.queue.put(self.STOP_SIGNAL)
        # print(self.metaData.stream_id, "Waiting for stream thread to stop")
        if self.thread.is_alive():
            self.thread.join()
        # print(self.metaData.stream_id, "Stream thread stopped")
