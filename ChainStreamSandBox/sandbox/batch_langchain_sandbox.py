if __name__ == '__main__':
    from sandbox_base import BatchSandbox
    from utils import check_library_installed
else:
    from .sandbox_base import BatchSandbox
    from .utils import check_library_installed
import os


class LangChainBatchSandbox(BatchSandbox):
    def __init__(self, task, agent_code, save_result=True, save_path=os.path.join(os.path.dirname(__file__), 'results'),
                 raise_exception=True, only_init_agent=False):
        super().__init__(task, agent_code, save_result=save_result, save_path=save_path,
                         raise_exception=raise_exception, only_init_agent=only_init_agent, sandbox_type="langchain")

    def run_func(self, all_input_data) -> dict:
        check_library_installed(["langchain"])
        original_env = os.environ.copy()

        try:
            env_vars = {
                "OPENAI_API_KEY": "sk-qnAcq9g0VKZt3I49s99JLWPRBXzmxyT0aWYJh0cqGJPeKzx9",
                "OPENAI_API_BASE": "https://api.openai-proxy.org/v1"
            }

            os.environ.update(env_vars)

            output_dict = self.code_instance(self.all_input_data)
        finally:
            os.environ.clear()
            os.environ.update(original_env)

        return output_dict


def tmp_func():
    import os
    from langchain.llms import OpenAI

    env_vars = {
        "OPENAI_API_KEY": "sk-qnAcq9g0VKZt3I49s99JLWPRBXzmxyT0aWYJh0cqGJPeKzx9",
        "OPENAI_BASE_URL": "https://api.openai-proxy.org/v1"
    }

    os.environ.update(env_vars)

    openai_base_url = os.environ.get('OPENAI_BASE_URL')
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    print(openai_base_url)
    print(openai_api_key)

    def process_data(input_streams: dict[str, list]):
        llm = OpenAI(base_url=openai_base_url, api_key=openai_api_key, model_name="gpt-4")

        target_streams = {
            'all_health': [],
            'remind_check': []
        }

        health_data = input_streams.get('health_sensor_data', [])

        for data in health_data:
            blood_sugar = data.get('BS')
            target_streams['all_health'].append({'BS': blood_sugar})

            if blood_sugar > 8.4:
                target_streams['remind_check'].append({
                    'Blood_sugar': blood_sugar,
                    'reminder': "High blood sugar！You'd better go to the hospital to check your body!"
                })

        return target_streams

    # Example input
    input_streams = {
        'health_sensor_data': [
            {'BS': 7.5},
            {'BS': 8.5},
            {'BS': 9.0},
            {'BS': 5.6}
        ]
    }

    # Process data
    processed_streams = process_data(input_streams)
    print(processed_streams)


if __name__ == "__main__":
    #     from ChainStreamSandBox.tasks import ALL_TASKS
    #
    #     Config = ALL_TASKS['EmailTask1']
    #
    #     agent_file = '''
    # def process_data(input_dict):
    #     import tensorflow
    #     print(input_dict)
    #     output_dict = {
    #         "summary_by_sender" : input_dict["all_email"]
    #     }
    #     return output_dict
    #     '''
    #     config = Config()
    #     oj = LangChainBatchSandbox(config, agent_file, save_result=True, only_init_agent=False)
    #
    #     res = oj.start_test_agent(return_report_path=True)
    #     print(res)

    tmp_func()

    # if res['start_agent'] != "[OK]":
    #     print("\n\nError while starting agent:", res['start_agent']['error_message'])
    #     for line in res['start_agent']['traceback'].split('\n'):
    #         print(line)
