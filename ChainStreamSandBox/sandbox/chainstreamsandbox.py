import os.path
import time
import traceback
import tempfile
import importlib.util

from chainstream.runtime import reset_chainstream_server
import json
import datetime

from chainstream.sandbox_recorder import start_sandbox_recording
from chainstream.agent.base_agent import Agent
from chainstream.stream import create_stream


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

    def start_agent(self) -> object:
        raise NotImplementedError("Subclasses must implement start_agent")

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

    def start_test_agent(self, return_report_path=False):
        try:
            self.result['sandbox_info']['sandbox_start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.task is not None:
                self.prepare_environment()

            res = self.start_agent()

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


class ChainStreamSandBox(SandboxBase):
    def __init__(self, task, agent_code, save_result=True, save_path=os.path.join(os.path.dirname(__file__), 'results'),
                 raise_exception=True, only_init_agent=False):
        super().__init__(task, agent_code, save_result=save_result, save_path=save_path, raise_exception=raise_exception, only_init_agent=only_init_agent, sandbox_type="chainstream")
        from chainstream.runtime import cs_server
        cs_server.init(server_type='core')
        cs_server.start()

        start_sandbox_recording()

        self.runtime = cs_server.get_chainstream_core()

        self.agent_instance = Agent("sandbox_tmp_agent")

    def prepare_environment(self):
        self.task.init_environment(self.runtime)

    def start_agent(self) -> object:
        return self._start_agent()

    def start_task(self) -> list:
        return self.task.start_task(self.runtime)

    def wait_task_finish(self):
        self.runtime.wait_all_stream_clear()

    def get_output_list(self) -> list:
        return self.task.record_output()

    def get_runtime_report(self) -> dict:
        from chainstream.sandbox_recorder import SANDBOX_RECORDER
        report = SANDBOX_RECORDER.get_event_recordings()
        return report

    def get_error_msg(self) -> dict:
        self.runtime.get_error_history()

    def stop_runtime(self):
        self.runtime.shutdown()
        reset_chainstream_server()

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

            class_object = None
            # globals().update(namespace)
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and not obj.__name__ == "Agent" and issubclass(obj, Agent):
                    class_object = obj
                    break

            if class_object is not None:
                try:
                    self.agent_instance = class_object()
                except Exception as e:
                    traceback.print_exc()
                    raise InitializeError(traceback.format_exc())
            else:
                raise FindAgentError(traceback.format_exc())
            try:
                self.agent_instance.start()
            except Exception as e:
                raise StartError(traceback.format_exc())

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

    def create_stream(self, stream_description):
        from AgentGenerator.io_model import StreamDescription
        if isinstance(stream_description, StreamDescription):
            stream_id = stream_description.stream_id
        else:
            stream_id = stream_description

        create_stream(self.agent_instance, stream_id)

    def get_agent(self):
        return self.agent_instance


if __name__ == "__main__":
    from ChainStreamSandBox.tasks import ALL_TASKS

    Config = ALL_TASKS['EmailTask1']

    agent_file = '''
import chainstream
from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.context import Buffer
from chainstream.llm import get_model, make_prompt

class EmailSummaryAgent(Agent):
    def __init__(self, agent_id: str="email_summary_agent"):
        super().__init__(agent_id)
        self.email_stream = get_stream(self, "all_email")
        self.summary_stream = get_stream(self, "summary_by_sender")
        self.llm = get_model(["text"])

    def start(self) -> None:
        def filter_advertisements(email):
            print("filter_advertisements", email)
            if "advertisement" not in email['Content'].lower():
                print("not an advertisement", email)
                return email
    
        def summarize_emails(email_batch):
            print("summarize_emails", email_batch)
            buffer = Buffer()
            for email in email_batch['item_list']:
                buffer.append({'sender': email['sender'], 'content': email['Content']})
            
            prompt = make_prompt(buffer, "Provide a summary for each sender's emails.")
            summary = self.llm.query(prompt)
            
            self.summary_stream.add_item({'sender': email['sender'], 'summary': summary})
        
        self.email_stream.for_each(filter_advertisements)\
                          .batch(by_count=5)\
                          .for_each(summarize_emails)
        
    def stop(self) -> None:
        self.email_stream.unregister_all(self)
    '''
    config = Config()
    oj = ChainStreamSandBox(config, agent_file, save_result=True, only_init_agent=False)

    res = oj.start_test_agent(return_report_path=True)
    print(res)

    # if res['start_agent'] != "[OK]":
    #     print("\n\nError while starting agent:", res['start_agent']['error_message'])
    #     for line in res['start_agent']['traceback'].split('\n'):
    #         print(line)
