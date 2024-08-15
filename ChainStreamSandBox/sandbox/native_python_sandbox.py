from .sandbox_base import *
import os
from chainstream.agent.base_agent import Agent
from chainstream.stream import get_stream

class TmpInputRecordAgent(Agent):
    def __init__(self, stream_ids):
        super().__init__("TmpInputRecordAgent")
        self.stream_ids = stream_ids
        self.input_records = {}
        self.stream_list = {}
        for stream in stream_ids:
            self.input_records[stream] = []
            self.stream_list[stream] = get_stream(self, stream)

    def start(self):
        def get_func(tmp_stream_id):
            tmp_stream = self.stream_list[tmp_stream_id]
            def record_input_func(item):
                self.input_records[tmp_stream_id].append(item)
            return record_input_func
        for stream_id in self.stream_ids:
            self.stream_list[stream_id].for_each(get_func(stream_id))

    def stop(self):
        pass

    def get_input_records(self):
        return self.input_records


class NativePythonSandbox(SandboxBase):
    def __init__(self, task, agent_code, save_result=True, save_path=os.path.join(os.path.dirname(__file__), 'results'),
                 raise_exception=True, only_init_agent=False):
        super().__init__(task, agent_code, save_result=save_result, save_path=save_path,
                         raise_exception=raise_exception, only_init_agent=only_init_agent, sandbox_type="native_python")
        from chainstream.runtime import cs_server
        cs_server.init(server_type='core')
        cs_server.start()

        start_sandbox_recording()

        self.runtime = cs_server.get_chainstream_core()

        self.all_input_stream_ids = [stream_description.stream_id for stream_description in self.task.input_stream_descriptions]
        self.input_recorder = None

        self.code_instance = None
        self.input_list = []
        self.output_list = []
        self.all_input_data = None

    def prepare_environment(self):
        self.task.init_environment(self.runtime)
        self.input_recorder = TmpInputRecordAgent(self.all_input_stream_ids)

    # def start_agent(self) -> object:
    #     raise NotImplementedError("Subclasses must implement start_agent")

    def import_and_init(self, module):
        func_object = None
        for name, obj in module.__dict__.items():
            if inspect.isclass(obj) and obj.__name__ == "process_data":
                func_object = obj
                break
        if func_object is None:
            raise
        else:
            try:
                self.code_instance = func_object()
            except Exception as e:
                traceback.print_exc()
                raise InitializeError(traceback.format_exc())

        self.input_recorder.start()

    def start_task(self) -> list:
        return self.task.start_task(self.runtime)

    def wait_task_finish(self):
        self.runtime.wait_all_stream_clear()
        self.all_input_data = self.input_recorder.get_input_records()

    def get_output_list(self) -> list:
        try:
            output_list = self.code_instance(self.all_input_data)
            return output_list
        except Exception as e:
            traceback.print_exc()
            raise RunningError(traceback.format_exc())

    def get_runtime_report(self) -> dict:
        return "Native Python does not support runtime report"

    def get_error_msg(self) -> dict:
        return "Native Python does not support runtime report"

    def stop_runtime(self):
        self.runtime.shutdown()
        reset_chainstream_server()

