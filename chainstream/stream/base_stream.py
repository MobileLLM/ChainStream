from chainstream.interfaces import StreamInterface
from chainstream.runtime import cs_server_core
from .stream_recorder import StreamRecorder
import logging
import datetime
import queue
import threading
import inspect
from threading import Event
from ..context import Buffer
from ..function import AgentFunction


class StreamForAgent:
    def __init__(self, agent, stream):
        self.stream = stream
        self.agent = agent

    def for_each(self, listener_func):
        return self.stream.for_each(self.agent, listener_func)

    def batch(self, by_count=None, by_time=None, by_key=None, by_fucn=None):
        pass

    def unregister_all(self, listener_func=None):
        self.stream.unregister_all(self.agent, listener_func)

    def add_item(self, item):
        self.stream.add_item(item)

    def send_item(self, item):
        self.add_item(item)

    def shutdown(self):
        self.stream.shutdown()


class StreamMeta:
    def __init__(self, *args, **kwargs):
        self.stream_id = kwargs.get('stream_id')
        self.description = kwargs.get('description')
        self.create_time = datetime.datetime.now()
        self.create_by_agent_file = kwargs.get('create_by_agent_file')
        self.is_anonymous = kwargs.get('is_anonymous')

    def __dict__(self):
        return {
            "stream_id": self.stream_id,
            "description": self.description,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "create_by": self.create_by_agent_file
        }


class BaseStream(StreamInterface):
    STOP_SIGNAL = object()

    def __init__(self, stream_id, description=None, create_by_agent_file=None, is_anonymous=False) -> None:
        super().__init__()
        self.metaData = StreamMeta(
            stream_id=stream_id,
            description=description,
            create_by_agent_file=create_by_agent_file,
            is_anonymous=is_anonymous
        )
        self.logger = logging.getLogger(self.metaData.stream_id)

        self.is_anonymous = is_anonymous
        self.next_anonymous = {}

        self.anonymous_func_params = {}

        self.is_clear = Event()
        self.is_clear.set()

        self.listeners = []
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.process_item)

        self.is_running = False

        self.recorder = StreamRecorder(self.metaData, self.queue)

        cs_server_core.register_stream(self)

    def for_each(self, agent, listener_func):
        listener_func = AgentFunction(listener_func)
        try:
            self.listeners.append((agent.agent_id, listener_func))
            self.recorder.record_listener_actions("for_each", agent.agent_id, listener_func.__name__)
            self.recorder.record_listener_change(len(self.listeners))
            if not self.is_running:
                self.is_running = True
                self.thread.start()

            next_stream_id = "anonymous_" + self.metaData.stream_id + "_" + agent.agent_id + "_" + str(
                listener_func.__name__)
            create_by_agent_file = self.metaData.create_by_agent_file
            next_stream = BaseStream(next_stream_id, create_by_agent_file=create_by_agent_file, is_anonymous=True)
            self.next_anonymous[(agent.agent_id, listener_func.__name__)] = next_stream

            listener_func.set_output_stream(next_stream)

            return StreamForAgent(agent, self.next_anonymous[(agent.agent_id, listener_func.__name__)])

        except Exception as e:
            print("Error registering listener: ", e)
            self.recorder.record_listener_actions("for_each", agent.agent_id, listener_func.__name__, error=str(e))
            self.recorder.record_listener_change(len(self.listeners))

            return None

    def batch(self, agent, by_count=None, by_time=None, by_key=None, by_func=None):
        none_count = 0
        if by_count is None:
            none_count += 1
        if by_time is None:
            none_count += 1
        if by_key is None:
            none_count += 1
        if by_func is None:
            none_count += 1
        if none_count == 0:
            raise ValueError("At least one of by_count, by_time, by_key, by_func should be specified")
        if none_count > 1:
            raise ValueError("Only one of by_count, by_time, by_key, by_func should be specified")

        new_buffer = Buffer()
        self.anonymous_func_params[agent.agent_id] = self.anonymous_func_params.get(agent.agent_id, []).append(
            new_buffer)

        if by_count is not None:
            def anonymous_batch_func_by_count(item):
                if len(new_buffer) < by_count:
                    new_buffer.append(item)
                else:
                    new_buffer.append(item)
                    all_items = new_buffer.pop_all()
                    return all_items

            return self.for_each(agent, anonymous_batch_func_by_count)

        if by_time is not None:
            time_start = datetime.datetime.now()
            self.anonymous_func_params[agent.agent_id] = self.anonymous_func_params.get(agent.agent_id, []).append(
                time_start)

            def anonymous_batch_func_by_time(item):
                if datetime.datetime.now() - time_start < by_time:
                    new_buffer.append(item)
                else:
                    all_items = new_buffer.pop_all()
                    new_buffer.append(item)
                    return all_items

            return self.for_each(agent, anonymous_batch_func_by_time)

        if by_key is not None:
            key_item = by_key
            self.anonymous_func_params[agent.agent_id] = self.anonymous_func_params.get(agent.agent_id, []).append(
                key_item)

            def anonymous_batch_func_by_key(item):
                if key_item != item:
                    new_buffer.append(item)

                else:
                    new_buffer.append(item)
                    all_items = new_buffer.pop_all()
                    return all_items

            return self.for_each(agent, anonymous_batch_func_by_key)

        if by_func is not None:
            return self.for_each(agent, by_func)

    def unregister_all(self, agent, listener_func=None):
        new_listeners = []
        for agent_, listener_func_ in self.listeners:
            if agent_ != agent.agent_id:
                new_listeners.append((agent_, listener_func_))
            elif listener_func is not None and listener_func_ == listener_func:
                new_listeners.append((agent_, listener_func_))
        self.listeners = new_listeners

        for agent_id, listener_func_ in self.next_anonymous:
            if agent_id == agent.agent_id and (listener_func is None or listener_func_ == listener_func):
                self.next_anonymous[(agent_id, listener_func_)].unregister_all(agent)
                self.next_anonymous[(agent_id, listener_func_)].shutdown()

        for agent_id, params_list in self.anonymous_func_params.items():
            if agent_id == agent.agent_id:
                for params in params_list:
                    del params
                del self.anonymous_func_params[agent_id]

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
        data['listeners'] = [str(agent_) + ":" + str(listener_func_.__name__) for agent_, listener_func_ in
                             self.listeners]
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
