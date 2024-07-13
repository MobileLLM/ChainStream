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
import os


class StreamForAgent:
    def __init__(self, agent, stream):
        self.stream = stream
        self.agent = agent

    def for_each(self, listener_func: AgentFunction, to_stream=None):
        return self.stream.for_each(self.agent, listener_func, to_stream=to_stream)

    def batch(self, by_count=None, by_time=None, by_key=None, by_func=None, to_stream=None):
        return self.stream.batch(self.agent, by_count=by_count, by_time=by_time, by_key=by_key, by_func=by_func,
                                 to_stream=to_stream)

    def unregister_all(self, listener_func=None):
        self.stream.unregister_all(self.agent, listener_func)

    def add_item(self, item: [dict, list]):
        if isinstance(item, dict):
            self.stream.add_item(self.agent, item)
        elif isinstance(item, list):
            for i in item:
                self.stream.add_item(self.agent, i)

    def send_item(self, item):
        self.add_item(item)

    def shutdown(self):
        self.stream.shutdown()

    def get_record_data(self):
        return self.stream.get_record_data()


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

    def for_each(self, agent, listener_func, to_stream=None):
        listener_func = AgentFunction(agent, listener_func)
        try:
            self.listeners.append((agent.agent_id, listener_func))
            self.recorder.record_listener_actions("for_each", agent.agent_id, listener_func.func_id)
            self.recorder.record_listener_change(len(self.listeners))
            if not self.is_running:
                self.is_running = True
                self.thread.start()

            if to_stream is None:
                if "[anonymous]__" not in self.metaData.stream_id:
                    next_stream_id = "[anonymous]__" + self.metaData.stream_id + "_" + agent.agent_id + "__[func]__" + str(
                        listener_func.func_id + "__[count]__" + "0")
                else:
                    tmp_agent_name = self.metaData.stream_id.split("__[func]__")[0]
                    tmp_count = self.metaData.stream_id.split("__[count]__")[1]

                    next_stream_id = tmp_agent_name + "__[func]__" + str(listener_func.func_id) + "__[count]__" + str(
                        int(tmp_count) + 1)

                create_by_agent_file = self.metaData.create_by_agent_file
                next_stream = BaseStream(next_stream_id, create_by_agent_file=create_by_agent_file, is_anonymous=True)
                self.next_anonymous[(agent.agent_id, listener_func.func_id)] = next_stream

                stream_for_agent = StreamForAgent(agent, self.next_anonymous[(agent.agent_id, listener_func.func_id)])
            else:
                if isinstance(to_stream, StreamForAgent):
                    stream_for_agent = to_stream
                else:
                    raise ValueError("to_stream should be a StreamForAgent object")

            listener_func.set_output_stream(stream_for_agent)

            return stream_for_agent

        except Exception as e:
            print("Error registering listener: ", e)
            self.recorder.record_listener_actions("for_each", agent.agent_id, listener_func.__name__, error=str(e))
            self.recorder.record_listener_change(len(self.listeners))

            return None

    def batch(self, agent, by_count=None, by_time=None, by_key=None, by_func=None, to_stream=None):
        none_count = 0
        if by_count is None:
            none_count += 1
        if by_time is None:
            none_count += 1
        if by_key is None:
            none_count += 1
        if by_func is None:
            none_count += 1
        if 4 - none_count == 0:
            raise ValueError("At least one of by_count, by_time, by_key, by_func should be specified")
        if 4 - none_count > 1:
            raise ValueError("Only one of by_count, by_time, by_key, by_func should be specified")

        new_buffer = Buffer()
        # self.anonymous_func_params[agent.agent_id] = self.anonymous_func_params.get(agent.agent_id, []).append(
        #     new_buffer)
        if agent.agent_id not in self.anonymous_func_params:
            self.anonymous_func_params[agent.agent_id] = []
        self.anonymous_func_params[agent.agent_id].append(new_buffer)

        if by_count is not None:
            def anonymous_batch_func_by_count(item):
                if len(new_buffer) < by_count - 1:
                    new_buffer.append(item)
                else:
                    new_buffer.append(item)
                    all_items = new_buffer.pop_all()
                    return {"item_list": all_items}

            return self.for_each(agent, anonymous_batch_func_by_count, to_stream=to_stream)

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
                    return {"item_list": all_items}

            return self.for_each(agent, anonymous_batch_func_by_time, to_stream=to_stream)

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
                    return {"item_list": all_items}

            return self.for_each(agent, anonymous_batch_func_by_key, to_stream=to_stream)

        if by_func is not None:
            return self.for_each(agent, by_func, to_stream=to_stream)

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

    def add_item(self, agent, item):
        self.logger.debug(f'stream {self.metaData.stream_id} send an item type: {type(item)}')
        self.queue.put(item)
        call_from = inspect.stack()[2]
        # for i in call_from:
        #     print(i)
        # print("call from 2", call_from[2])
        # print("call from 3", call_from[3])

        current_frame = inspect.currentframe()
        # print("first frame", current_frame.f_back)
        # print("second frame", current_frame.f_back.f_back)
        # print("third frame", current_frame.f_back.f_back.f_back)
        call_frame = current_frame.f_back.f_back
        caller_instance = call_frame.f_locals.get('self', None)
        # print(caller_instance)

        # print(call_from.filename, call_from.function)

        if isinstance(caller_instance, AgentFunction):
            """
            In case of data from return of agent function
            """
            # print(caller_instance.agent.agent_store_base_path)
            # agent_full_path = caller_instance.agent.metaData.agent_file_path
            # agent_base_path = caller_instance.agent.agent_store_base_path
            # agent_path = os.path.relpath(agent_full_path, agent_base_path)
            # print(agent_path)
            self.recorder.record_new_item(caller_instance.agent.metaData.agent_file_path, caller_instance.func_id)
        elif isinstance(current_frame.f_back.f_back.f_back.f_locals.get('self', None), threading.Thread):
            """
            In case of data from thread, means it is from an original stream
            """
            self.recorder.record_new_item(call_from.filename, call_from.function)
        else:
            """
            In case of data from from func inside, not from return
            """
            # print(call_from.filename)
            tmp_caller_instance = current_frame.f_back.f_back.f_back.f_locals.get('self', None)
            # print("tmp_caller_instance", tmp_caller_instance)
            if tmp_caller_instance.__class__.__name__ == "SandBox":
                func_id = "__[sandbox]__"
            else:
                func_id = tmp_caller_instance.func_id
            self.recorder.record_new_item(call_from.filename, func_id)

        # self.recorder.record_new_item(caller_instance.__file__, caller_instance)

    # def send_item(self, agent, item):
    #     self.add_item(agent, item)

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
                    self.recorder.record_send_item(agent_, listener_func_.func_id)
                self.is_clear.set()

    def get_meta_data(self):
        data = self.metaData.__dict__()
        data['listeners'] = [str(agent_) + ":" + str(listener_func_.func_id) for agent_, listener_func_ in
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
