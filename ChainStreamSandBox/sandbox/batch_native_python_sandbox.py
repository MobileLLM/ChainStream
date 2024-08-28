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

            os.environ.update(env_vars)

            output_dict = self.code_instance(self.all_input_data)
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

    Config = ALL_TASKS['EmailTask1']

    agent_file = '''
from openai import OpenAI
import os

def process_data(input_dict):
    print(input_dict)
    # print(os.environ['OPENAI_API_KEY'])
    # print(os.environ['OPENAI_BASE_URL'])
    llm = OpenAI(api_key=os.environ['OPENAI_API_KEY'], base_url=os.environ['OPENAI_BASE_URL'])
    response = llm.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    )
    print(response)
    output_dict = {
        "summary_by_sender" : response.choices[0].message.content,
    }
    return output_dict
    '''
    config = Config()
    oj = NativePythonBatchSandbox(config, agent_file, save_result=True, only_init_agent=False)

    res = oj.start_test_agent(return_report_path=True)
    print(res)

    # if res['start_agent'] != "[OK]":
    #     print("\n\nError while starting agent:", res['start_agent']['error_message'])
    #     for line in res['start_agent']['traceback'].split('\n'):
    #         print(line)
