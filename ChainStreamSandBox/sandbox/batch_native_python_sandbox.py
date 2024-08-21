if __name__ == '__main__':
    from sandbox_base import BatchSandbox
else:
    from .sandbox_base import BatchSandbox
import os


class NativePythonBatchSandbox(BatchSandbox):
    def __init__(self, task, agent_code, save_result=True, save_path=os.path.join(os.path.dirname(__file__), 'results'),
                 raise_exception=True, only_init_agent=False):
        super().__init__(task, agent_code, save_result=save_result, save_path=save_path,
                         raise_exception=raise_exception, only_init_agent=only_init_agent, sandbox_type="native_python")

    def run_func(self, all_input_data) -> dict:
        original_env = os.environ.copy()

        try:
            env_vars = {
                "OPENAI_API_KEY": "sk-qnAcq9g0VKZt3I49s99JLWPRBXzmxyT0aWYJh0cqGJPeKzx9",
                "OPENAI_BASE_URL": "https://api.openai-proxy.org/v1"
            }

            os.environ.update(env_vars)

            output_dict = self.code_instance(self.all_input_data)
        finally:
            os.environ.clear()
            os.environ.update(original_env)

        return output_dict


if __name__ == "__main__":
    from ChainStreamSandBox.tasks import ALL_TASKS

    Config = ALL_TASKS['EmailTask1']

    agent_file = '''
def process_data(input_dict):
    print(input_dict)
    output_dict = {
        "summary_by_sender" : input_dict["all_email"]
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
