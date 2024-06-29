import os.path
import time
from chainstream.runtime import cs_server
import json
import datetime


class ExecError(Exception):
    def __init__(self, message):
        super().__init__(message)


class StartError(Exception):
    def __init__(self, message):
        super().__init__(message)


class RunningError(Exception):
    def __init__(self, message):
        super().__init__(message)


class FindAgentError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InitializeError(Exception):
    def __init__(self, message):
        super().__init__(message)


class SandBox:
    def __init__(self, task, agent_code, save_path=os.path.join(os.path.dirname(__file__), 'results')):
        cs_server.init(server_type='core')
        cs_server.start()
        self.runtime = cs_server.get_chainstream_core()
        self.task = task
        self.agent_code = agent_code
        self.agent_instance = None

        self.result = {'sandbox_info': {
            'sandbox_init_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'task_name': self.task.__class__.__name__,
            'agent_code': self.agent_code
        }}

        self.save_path = save_path

    def start_test_agent(self):
        self.result['sandbox_info']['sandbox_start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.task.init_environment(self.runtime)

        res = self._start_agent()

        if res is not None:
            self.result['start_agent'] = res
            raise RunningError("Error while starting agent: " + str(res))

        try:
            self.task.start_task(self.runtime)
        except Exception as e:
            self.result['start_stream'] = str(e)
            raise RunningError("Error while starting stream: " + str(e))

        # we delete this line because we want decouple the evaluation process from the sandbox. In sandbox,
        # we only want to init the task environment and start the agent, then start the stream and record all output
        # into a file. self.task.evaluate_task(self.runtime)

        self.runtime.wait_all_stream_clear()

        self.result['task_output'] = self.task.record_output()

        self.result['sandbox_info']['sandbox_end_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.result['runtime_report'] = self.runtime.get_agent_report(self.agent_instance.agent_id)

        self._save_result(self.result)
        # print("Sandbox result saved to " + self.save_path)
        self.runtime.shutdown()

        return self.result

    def _start_agent(self):
        try:
            namespace = {}
            try:
                exec(self.agent_code, globals(), namespace)
            except Exception as e:
                raise ExecError("Error while executing agent file: " + str(e))

            class_object = None
            globals().update(namespace)
            for name, obj in namespace.items():
                if isinstance(obj, type):
                    class_object = obj
                    break

            if class_object is not None:
                try:
                    self.agent_instance = class_object()
                except Exception as e:
                    raise InitializeError("Error while initializing agent: " + str(e))
            else:
                raise FindAgentError("Agent class not found in agent file")
            try:
                self.agent_instance.start()
            except Exception as e:
                raise StartError("Error while starting agent: " + str(e))

        except Exception as e:
            self.result['start_agent'] = "[ERROR]" + str(e)
            return str(e)
        self.result['start_agent'] = "[OK]"
        return None

    def get_agent(self):
        return self.agent_instance

    def _save_result(self, result):
        if self.save_path is not None:
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
            file_path = os.path.join(
                self.save_path,
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + self.task.__class__.__name__ + "_" +
                self.agent_instance.agent_id + ".json"
            )
            with open(file_path, 'w') as f:
                json.dump(result, f, indent=4)


if __name__ == "__main__":
    from tasks import ALL_TASKS

    ArxivTaskConfig = ALL_TASKS['ArxivTask']

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
                # print(paper_title+" : "+response)
                self.output_stream.add_item(paper_title+" : "+response)

        self.input_stream.register_listener(self, process_paper)

    def stop(self):
        self.input_stream.unregister_listener(self)
    '''
    oj = SandBox(ArxivTaskConfig(), agent_file)
    res = oj.start_test_agent()
    print(res)
