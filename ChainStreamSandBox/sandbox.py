import os.path
import time
import traceback
import tempfile
import importlib.util

from chainstream.runtime import cs_server
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


class SandBox:
    def __init__(self, task, agent_code, save_result=True, save_path=os.path.join(os.path.dirname(__file__), 'results'),
                 raise_exception=True):
        cs_server.init(server_type='core')
        cs_server.start()

        self.raise_exception = raise_exception

        self.runtime = cs_server.get_chainstream_core()
        self.task = task
        self.agent_code = agent_code
        self.agent_instance = None

        self.result = {'sandbox_info': {
            'sandbox_init_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'task_name': self.task.task_id,
            'agent_code': self.agent_code
        }}

        if save_result:
            self.save_path = save_path
        else:
            self.save_path = None

    def start_test_agent(self, return_report_path=False):
        try:
            self.result['sandbox_info']['sandbox_start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.task.init_environment(self.runtime)

            res = self._start_agent()

            if res is not None:
                self.result['start_agent'] = res
                raise StartError(res)

            try:
                sent_item = self.task.start_task(self.runtime)
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
                self.result['sent_item'] = sent_item

            # we delete this line because we want decouple the evaluation process from the sandbox. In sandbox,
            # we only want to init the task environment and start the agent, then start the stream and record all output
            # into a file. self.task.evaluate_task(self.runtime)

            self.runtime.wait_all_stream_clear()

            self.result['task_output'] = self.task.record_output()

            self.result['sandbox_info']['sandbox_end_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.result['runtime_report'] = self.runtime.get_agent_report(self.agent_instance.agent_id)

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

            report_path = self._save_result(self.result)
            # print("Sandbox result saved to " + self.save_path)
            self.runtime.shutdown()

            if return_report_path:
                return report_path
            return self.result

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
                if isinstance(obj, type):
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
        self.result['start_agent'] = "[OK]"
        return None

    def get_agent(self):
        return self.agent_instance

    def _save_result(self, result):
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


if __name__ == "__main__":
    from tasks import ALL_TASKS_OLD

    Config = ALL_TASKS_OLD['ArxivAbstractTask']

    agent_file = '''
import chainstream as cs
from chainstream.llm import get_model

class TestAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_arxiv_agent")
        self.input_stream = cs.get_stream("all_arxiv")
        self.output_stream = cs.get_stream("cs_arxiv")
        self.llm = get_model(["text"])

    def start(self):
        def process_paper(paper):
            if "abstract" in paper:
                paper_title = paper["title"]
                paper_content = paper["abstract"]
                paper_versions = paper["versions"]
                stage_tags = ['Conceptual', 'Development', 'Testing', 'Deployment', 'Maintenance','Other']
                prompt = "Give you an abstract of a paper: {} and the version of this paper:{}. What tag would you like to add to this paper? Choose from the following: {}".format(paper_content,paper_versions, ', '.join(stage_tags))
                prompt_message = [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
                response = self.llm.query(prompt_message)
                print(paper_title+" : "+response)
                self.output_stream.add_item(paper_title+" : "+response)

        self.input_stream.for_each(self, process_paper)

    def stop(self):
        self.input_stream.unregister_all(self)
    '''
    config = Config()
    oj = SandBox(config, agent_file)
    res = oj.start_test_agent()
    print(res)
