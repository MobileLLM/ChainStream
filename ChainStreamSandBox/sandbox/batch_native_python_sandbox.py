if __name__ == '__main__':
    from sandbox_base import BatchSandbox
else:
    from .sandbox_base import BatchSandbox
import os
import ast


class NativePythonBatchSandbox(BatchSandbox):
    def __init__(self, task, agent_code, save_result=True, save_path=os.path.join(os.path.dirname(__file__), 'results'),
                 raise_exception=True, only_init_agent=False):
        super().__init__(task, agent_code, save_result=save_result, save_path=save_path,
                         raise_exception=raise_exception, only_init_agent=only_init_agent, sandbox_type="native_python")

    def run_func(self, all_input_data) -> dict:
        original_env = os.environ.copy()

        try:
            env_vars = {
                    "OPENAI_BASE_URL": "https://tbnx.plus7.plus/v1",
                    "OPENAI_API_KEY": "sk-Eau4dcC9o9Bo1N3ID4EcD394F15b4c029bBaEfA9D06b219b"
            }
            # env_vars = {
            #     "OPENAI_BASE_URL": "https://api.openai-proxy.org/v1",
            #     "OPENAI_API_KEY": "sk-43Kn6GuGNxD0KwGB1XgiEyQ8htVDan44XXdnQqXA7VkZ7sMI"
            # }

            os.environ.update(env_vars)

            output_dict = self.code_instance(self.all_input_data)

            print(f"output_dict: {output_dict}")
        except Exception as e:
            raise e
        finally:
            os.environ.clear()
            os.environ.update(original_env)
        tmp_output_dict = output_dict
        if tmp_output_dict.startswith("```json") and tmp_output_dict.endswith("```"):
            tmp_output_dict = tmp_output_dict[7:-3]
            tmp_output_dict = ast.literal_eval(tmp_output_dict)

        return tmp_output_dict


if __name__ == "__main__":
    from ChainStreamSandBox.tasks import ALL_TASKS

    Config = ALL_TASKS['ArxivTask5']

    agent_file = '''
from openai import OpenAI
import os
import threading
from chainstream.stream import get_stream_interface

    
def process_data(is_stop: threading.Event) -> None:
    input_stream_id = 'all_arxiv'
    output_stream_id = 'tag_algorithm'
    input_stream = get_stream_interface(input_stream_id)
    output_stream = get_stream_interface(output_stream_id)
    
    llm = OpenAI(api_key=os.environ['OPENAI_API_KEY'], base_url=os.environ['OPENAI_BASE_URL'])
    
    while not is_stop.is_set():
        item = input_stream.get(timeout=1)
        if item is None:
            continue
            
        title = item.get('title')
        abstract = item.get('abstract')
        algorithms_tags = ['Deep Learning', 'Machine Learning', 'Classical', 'Heuristic', 'Evolutionary', 'Other']
        prompt = "Give you an abstract of a paper: {}. What tag would you like to add to this paper? Choose from the following: {}".format(paper_content, ', '.join(algorithms_tags))
        response = llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
            ]
        )
        output_stream.put({
            "title": title,
            "algorithm": response,
        })
        
    '''
    config = Config()
    oj = NativePythonBatchSandbox(config, agent_file, save_result=True, only_init_agent=False)

    res = oj.start_test_agent(return_report_path=True)
    print(res)

    # if res['start_agent'] != "[OK]":
    #     print("\n\nError while starting agent:", res['start_agent']['error_message'])
    #     for line in res['start_agent']['traceback'].split('\n'):
    #         print(line)
