import os.path
import time
import traceback
import tempfile
import importlib.util

from chainstream.runtime import reset_chainstream_server
import json
import datetime


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

    def prepare_environment(self):
        raise NotImplementedError("Subclasses must implement prepare_environment")

    # def start_agent(self) -> object:
    #     raise NotImplementedError("Subclasses must implement start_agent")

    def import_and_init(self, module):
        raise NotImplementedError("Subclasses must implement import_and_init")

    def start_task(self) -> list:
        raise NotImplementedError("Subclasses must implement start_task")

    def wait_task_finish(self):
        raise NotImplementedError("Subclasses must implement wait_task_finish")

    def get_output_list(self) -> list:
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
            if isinstance(item, str):
                str_sent_item.append(item)
            elif isinstance(item, dict):
                tmp_str_item = {}
                for k, v in item.items():
                    tmp_str_item[k] = str(v)
                str_sent_item.append(tmp_str_item)
            elif isinstance(item, list):
                str_sent_item.append([str(i) for i in item])
            else:
                raise RunningError("Unsupported item type: "+ str(type(item)))

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
        return file_path

    def _start_agent(self):
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

                os.remove(temp_file_path)

                # exec(self.agent_code, globals(), namespace)

            except Exception as e:
                raise ExecError(traceback.format_exc())

            self.import_and_init(module)

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
            return None

    def start_test_agent(self, return_report_path=False):
        try:
            self.result['sandbox_info']['sandbox_start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.task is not None:
                self.prepare_environment()

            res = self._start_agent()

            if res is not None:
                self.result['start_agent'] = res
                raise StartError(res)

            if not self.only_init_agent:
                try:
                    sent_item = self.start_task()
                except Exception as e:
                    self.result['start_task'] = {
                        "error_message": "[ERROR]" + str(e),
                        "traceback": traceback.format_exc(),
                        "error_type": str(type(e))
                    }
                    if self.raise_exception:
                        raise RunningError(traceback.format_exc())
                else:
                    self.result['start_task'] = "[OK]"
                    self.result['input_stream_item'] = self._process_item_list_to_str(sent_item)

                # we delete this line because we want decouple the evaluation process from the sandbox. In sandbox,
                # we only want to init the task environment and start the agent, then start the stream and record all output
                # into a file. self.task.evaluate_task(self.runtime)

                self.wait_task_finish()

                tmp_output = self.get_output_list()
                # print("before record output", tmp_output)
                tmp_output['data'] = self._process_item_list_to_str(tmp_output['data'])
                self.result['output_stream_output'] = tmp_output

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


