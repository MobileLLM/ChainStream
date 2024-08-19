from chainstream.stream import create_stream
from ChainStreamSandBox.sandbox.sandbox_base import *


class ChainStreamSandBox(SandboxBase):
    def __init__(self, task, agent_code, save_result=True, save_path=os.path.join(os.path.dirname(__file__), 'results'),
                 raise_exception=True, only_init_agent=False):
        super().__init__(task, agent_code, save_result=save_result, save_path=save_path, raise_exception=raise_exception, only_init_agent=only_init_agent, sandbox_type="chainstream")
        from chainstream.runtime import cs_server
        cs_server.init(server_type='core')
        cs_server.start()

        start_sandbox_recording()

        self.runtime = cs_server.get_chainstream_core()

        self.agent_instance = None

    def prepare_environment(self):
        self.task.init_environment(self.runtime)

    def import_and_init(self, module):
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

    def start_task(self) -> dict:
        return self.task.start_task(self.runtime)

    def wait_task_finish(self):
        self.runtime.wait_all_stream_clear()

    def get_output_list(self) -> dict:
        return self.task.record_output()

    def get_runtime_report(self) -> dict:
        from chainstream.sandbox_recorder import SANDBOX_RECORDER
        report = SANDBOX_RECORDER.get_event_recordings()
        return report

    def get_error_msg(self) -> dict:
        return self.runtime.get_error_history()

    def stop_runtime(self):
        self.runtime.shutdown()
        reset_chainstream_server()

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
