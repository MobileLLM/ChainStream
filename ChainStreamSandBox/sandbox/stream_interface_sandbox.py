from ChainStreamSandBox.sandbox.sandbox_base import *
import threading
from threading import Event
import time


class StreamInterfaceSandBox(SandboxBase):
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

        self.code_thread = None

        self.all_input_stream_ids = [stream_description.stream_id for stream_description in
                                     self.task.input_stream_description.streams]
        self.input_recorder = None

        self.stop_event = Event()

    # def prepare_environment(self):
    #     self.task.init_environment(self.runtime)
    #     self.input_recorder = TmpInputRecordAgent(self.all_input_stream_ids)

    def prepare_input_environment(self):
        self.task.init_environment(self.runtime)
        self.input_recorder = TmpInputRecordAgent(self.all_input_stream_ids)

    def prepare_output_environment(self):
        pass

        # env_vars = {
        #     "OPENAI_BASE_URL": "https://tbnx.plus7.plus/v1",
        #     "OPENAI_API_KEY": "sk-Eau4dcC9o9Bo1N3ID4EcD394F15b4c029bBaEfA9D06b219b"
        # }
        #
        # os.environ.update(env_vars)

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
                self.stop_event.clear()
                self.code_thread = threading.Thread(target=func_object, args=(self.stop_event,))
                self.code_thread.start()
            except Exception as e:
                traceback.print_exc()
                raise InitializeError(traceback.format_exc())
        self.input_recorder.start()

    def start_task(self) -> list:
        return self.task.start_task(self.runtime)

    def wait_task_finish(self):
        time.sleep(2)
        self.runtime.wait_all_stream_clear()
        print("all streams cleared")
        self.stop_event.set()
        print("stop event set")
        self.code_thread.join()
        print("code thread joined")

    def get_output_list(self) -> dict:
        return self.task.record_output()

    def get_runtime_report(self) -> dict:
        return {"Note": "This mode does not support runtime report"}

    def get_error_msg(self) -> dict:
        return {"Note": "This mode does not support error message"}

    def stop_runtime(self):
        self.runtime.shutdown()
        reset_chainstream_server()


if __name__ == "__main__":
    from ChainStreamSandBox.tasks import ALL_TASKS

    Config = ALL_TASKS['ArxivTask5']

    agent_file = '''
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import threading
from chainstream.stream import get_stream_interface


def process_data(is_stop: threading.Event) -> None:
    input_stream_id = 'all_arxiv'
    output_stream_id = 'tag_algorithm'
    input_stream = get_stream_interface(input_stream_id)
    output_stream = get_stream_interface(output_stream_id)
    
    # Initialize the OpenAI LLM through LangChain
    llm = OpenAI(api_key=os.environ['OPENAI_API_KEY'], base_url=os.environ['OPENAI_BASE_URL'])
    
    # Define the prompt template
    prompt_template = PromptTemplate(
        input_variables=["abstract", "algorithms_tags"],
        template="Give you an abstract of a paper: {abstract}. What tag would you like to add to this paper? Choose from the following: {algorithms_tags}"
    )
    
    # Initialize the LLMChain with the LLM and the prompt template
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    algorithms_tags = ['Deep Learning', 'Machine Learning', 'Classical', 'Heuristic', 'Evolutionary', 'Other']
    
    while not is_stop.is_set():
        item = input_stream.get(timeout=1)
        if item is None:
            continue
            
        title = item.get('title')
        abstract = item.get('abstract')
        
        # Run the LLMChain
        response = chain.run(abstract=abstract, algorithms_tags=', '.join(algorithms_tags))
        
        output_stream.put({
            "title": title,
            "algorithm": response,
        })
    '''
    config = Config()
    oj = StreamInterfaceSandBox(config, agent_file, save_result=True, only_init_agent=False)

    res = oj.start_test_agent(return_report_path=True)
    print(res)
