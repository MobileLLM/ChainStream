import os.path
import traceback
import tempfile
import importlib.util

from chainstream.runtime import reset_chainstream_server
import json
import datetime

from chainstream.agent.base_agent import Agent
from chainstream.stream import get_stream
from chainstream.sandbox_recorder import start_sandbox_recording

import io
import sys

if __name__ == '__main__':
    from utils import extract_imports, escape_string_literals
else:
    from .utils import extract_imports, escape_string_literals


class SandboxError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.error_message = None


class ExecError(SandboxError):
    def __init__(self, message):
        super().__init__(message)
        self.error_message = "Error while executing agent code"


class StartError(SandboxError):
    def __init__(self, message):
        super().__init__(message)
        self.error_message = "Error while starting agent"


class RunningError(SandboxError):
    def __init__(self, message):
        super().__init__(message)
        self.error_message = "Error while running agent"


class FindAgentError(SandboxError):
    def __init__(self, message):
        super().__init__(message)
        self.error_message = "Error while finding agent class"


class InitializeError(SandboxError):
    def __init__(self, message):
        super().__init__(message)
        self.error_message = "Error while initializing agent"


class SandboxBase:
    def __init__(self, task, agent_code, save_result=True, save_path=os.path.join(os.path.dirname(__file__), 'results'),
                 raise_exception=True, only_init_agent=False, sandbox_type=None):
        self.sandbox_type = sandbox_type

        self.raise_exception = raise_exception

        self.task = task
        self.agent_code = agent_code
        self.agent_instance = None

        self.only_init_agent = only_init_agent

        if self.only_init_agent:
            self.result = {'sandbox_info': {
                'sandbox_init_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'sandbox_type': self.sandbox_type,
                'agent_code': self.agent_code
            }}
        else:
            self.result = {'sandbox_info': {
                'sandbox_init_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'sandbox_type': self.sandbox_type,
                'task_name': self.task.task_id,
                'agent_code': self.agent_code
            }}

        if save_result:
            self.save_path = save_path
        else:
            self.save_path = None

    # def prepare_environment(self):
    #     raise NotImplementedError("Subclasses must implement prepare_environment")

    def prepare_input_environment(self):
        raise NotImplementedError("Subclasses must implement prepare_input_environment")

    def prepare_output_environment(self):
        raise NotImplementedError("Subclasses must implement prepare_output_environment")

    # def start_agent(self) -> object:
    #     raise NotImplementedError("Subclasses must implement start_agent")

    def import_and_init(self, module):
        raise NotImplementedError("Subclasses must implement import_and_init")

    def start_task(self) -> dict:
        raise NotImplementedError("Subclasses must implement start_task")

    def wait_task_finish(self):
        raise NotImplementedError("Subclasses must implement wait_task_finish")

    def get_output_list(self) -> dict:
        raise NotImplementedError("Subclasses must implement get_output_list")

    def get_runtime_report(self) -> dict:
        raise NotImplementedError("Subclasses must implement get_runtime_report")

    def get_error_msg(self) -> dict:
        raise NotImplementedError("Subclasses must implement get_error_msg")

    def stop_runtime(self):
        raise NotImplementedError("Subclasses must implement stop_runtime")

    def _process_item_list_to_str(self, item_list):
        str_sent_item = []
        for item in item_list:
            if isinstance(item, str) or isinstance(item, float):
                str_sent_item.append(item)
            elif isinstance(item, dict):
                tmp_str_item = {}
                for k, v in item.items():
                    tmp_str_item[k] = str(v)
                str_sent_item.append(tmp_str_item)
            elif isinstance(item, list):
                str_sent_item.append([str(i) for i in item])
            else:
                raise RunningError("Unsupported item type: " + str(type(item)))

        return str_sent_item

    def _save_result(self, result):
        file_path = None
        if self.save_path is not None:
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
            if self.agent_instance is not None and hasattr(self.agent_instance, 'agent_id'):
                file_path = os.path.join(
                    self.save_path,
                    datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + self.task.task_id + "_" +
                    self.agent_instance.agent_id + ".json"
                )
            else:
                file_path = os.path.join(
                    self.save_path,
                    datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + self.task.task_id + "_" +
                    "agent_instance_not_found" + ".json"
                )
            with open(file_path, 'w') as f:
                json.dump(result, f, indent=4)
            return os.path.abspath(file_path)
        return None

    def _start_agent(self):
        # starting_captured_output = None
        try:
            # namespace = {}
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_file:
                    temp_file.write(self.agent_code.encode('utf-8'))
                    temp_file_path = temp_file.name

                module_name = os.path.splitext(os.path.basename(temp_file_path))[0]
                spec = importlib.util.spec_from_file_location(module_name, temp_file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                self.import_list = extract_imports(self.agent_code)

                os.remove(temp_file_path)

                # exec(self.agent_code, globals(), namespace)

            except Exception as e:
                raise ExecError(traceback.format_exc())

            original_stdout = sys.stdout
            global_output_buffer = io.StringIO()
            try:
                sys.stdout = global_output_buffer
                self.import_and_init(module)
                tmp_starting_captured_output = global_output_buffer.getvalue()
            except Exception as e:
                raise InitializeError(traceback.format_exc())
            else:
                self.result["stdout"] = {"starting": tmp_starting_captured_output}
            finally:
                sys.stdout = original_stdout
                global_output_buffer.close()

        except Exception as e:
            self.result['start_agent'] = {
                "error_message": "[ERROR]" + e.error_message,
                "traceback": str(e),
                "error_type": str(type(e))
            }
            if self.raise_exception:
                raise RunningError("Error while starting agent: " + str(e))
            return str(e)
        else:
            self.result['start_agent'] = "[OK]"
            self.result['sandbox_info']['import_list'] = self.import_list
            return None

    def start_test_agent(self, return_report_path=False):

        env_vars = {
            "OPENAI_BASE_URL": "https://tbnx.plus7.plus/v1",
            "OPENAI_API_KEY": "sk-Eau4dcC9o9Bo1N3ID4EcD394F15b4c029bBaEfA9D06b219b"
        }

        os.environ.update(env_vars)
        try:
            self.result['sandbox_info']['sandbox_start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.task is not None:
                self.prepare_input_environment()

            res = self._start_agent()

            if self.task is not None:
                self.prepare_output_environment()

            if res is not None:
                self.result['start_agent'] = res
                raise StartError(res)

            if not self.only_init_agent:
                original_stdout = sys.stdout
                global_output_buffer = io.StringIO()
                try:
                    sys.stdout = global_output_buffer

                    sent_item = self.start_task()

                    running_captured_output = global_output_buffer.getvalue()

                except Exception as e:
                    self.result['start_task'] = {
                        "error_message": "[ERROR]" + str(e),
                        "traceback": traceback.format_exc(),
                        "error_type": str(type(e))
                    }
                    if self.raise_exception:
                        raise RunningError(traceback.format_exc())
                else:
                    self.result["stdout"]["running"] = running_captured_output

                    self.result['start_task'] = "[OK]"
                    self.result["input_stream_items"] = {}
                    for stream_id, data_items in sent_item.items():
                        self.result["input_stream_items"][stream_id] = self._process_item_list_to_str(data_items)
                finally:
                    sys.stdout = original_stdout
                    global_output_buffer.close()

                # we delete this line because we want decouple the evaluation process from the sandbox. In sandbox,
                # we only want to init the task environment and start the agent, then start the stream and record all
                # output into a file. self.task.evaluate_task(self.runtime)

                self.wait_task_finish()

                tmp_output = self.get_output_list()
                # print("before record output", tmp_output)

                for stream_id, data_items in tmp_output.items():
                    tmp_output[stream_id]['data'] = self._process_item_list_to_str(data_items['data'])
                self.result['output_stream_items'] = tmp_output

                self.result['sandbox_info']['sandbox_end_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                report = self.get_runtime_report()
                self.result['runtime_report'] = report

        except Exception as e:
            self.result['sandbox_info']['sandbox_end_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.result['sandbox_info']['sandbox_error'] = {
                "error_message": "[ERROR]" + e.error_message,
                "traceback": str(e),
                "error_type": str(type(e))
            }
            if self.raise_exception:
                raise e
        finally:
            self.result['error_message'] = self.get_error_msg()

            report_path = self._save_result(self.result)
            # print("Sandbox result saved to " + self.save_path)

            self.stop_runtime()

            if return_report_path:
                print("Sandbox result saved to ", report_path)
                return report_path
            return self.result


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
            tmp_stream_record = self.input_records[tmp_stream_id]

            def record_input_func(item):
                tmp_stream_record.append(item)

            return record_input_func

        for stream_id in self.stream_ids:
            self.stream_list[stream_id].for_each(get_func(stream_id))

    def stop(self):
        pass

    def get_input_records(self):
        return self.input_records


class BatchSandbox(SandboxBase):
    def __init__(self, task, agent_code, save_result=True, save_path=os.path.join(os.path.dirname(__file__), 'results'),
                 raise_exception=True, only_init_agent=False, sandbox_type=None, api_func_name="process_data"):
        super().__init__(task, agent_code, save_result=save_result, save_path=save_path,
                         raise_exception=raise_exception, only_init_agent=only_init_agent, sandbox_type=sandbox_type)
        from chainstream.runtime import cs_server
        cs_server.init(server_type='core')
        cs_server.start()

        start_sandbox_recording()

        self.runtime = cs_server.get_chainstream_core()

        self.api_func_name = api_func_name

        self.all_input_stream_ids = [stream_description.stream_id for stream_description in
                                     self.task.input_stream_description.streams]
        self.input_recorder = None

        self.code_instance = None
        self.input_list = []
        self.output_list = []
        self.all_input_data = None

    # def prepare_environment(self):
    #     self.task.init_environment(self.runtime)
    #     self.input_recorder = TmpInputRecordAgent(self.all_input_stream_ids)

    def prepare_input_environment(self):
        self.task.init_environment(self.runtime)
        self.input_recorder = TmpInputRecordAgent(self.all_input_stream_ids)

    def prepare_output_environment(self):
        pass

    # def start_agent(self) -> object:
    #     raise NotImplementedError("Subclasses must implement start_agent")

    def import_and_init(self, module):
        func_object = None
        for name, obj in module.__dict__.items():
            if callable(obj) and name == self.api_func_name:
                func_object = obj
                break
        if func_object is None:
            raise ExecError("process_data function not found in the module")
        else:
            try:
                self.code_instance = func_object
            except Exception as e:
                traceback.print_exc()
                raise InitializeError(traceback.format_exc())

        self.input_recorder.start()

    def start_task(self) -> list:
        return self.task.start_task(self.runtime)

    def wait_task_finish(self):
        self.runtime.wait_all_stream_clear()
        self.all_input_data = self.input_recorder.get_input_records()

    def run_func(self, all_input_data) -> dict:
        raise NotImplementedError("run_func method is not implemented yet")

    def get_output_list(self) -> dict:
        try:
            output_list = self.run_func(self.all_input_data)

            for stream_id, record in output_list.items():
                if len(record) == 0:
                    output_list[stream_id] = {
                        "status": "[ERROR] No output message found",
                        "data": []
                    }

                else:
                    output_list[stream_id] = {
                        "status": "[OK] Task completed",
                        "data": record
                    }
            return output_list
        except Exception as e:
            traceback.print_exc()
            raise RunningError(traceback.format_exc())

    def get_runtime_report(self) -> dict:
        return {"Note": "Native Python does not support runtime report"}

    def get_error_msg(self) -> dict:
        return {"Note": "Native Python does not support error message"}

    def stop_runtime(self):
        self.runtime.shutdown()
        reset_chainstream_server()
