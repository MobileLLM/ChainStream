from sandbox_interface import SandboxBatchInterface
from AgentGenerator import ChainStreamCoTGenerator
fixfrom ChainStreamSandBox.tasks import get_task_batch


class EvalCoTGenerator(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=5, result_path='./result', task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path, sandbox_type="chainstream")

    def get_agent_for_specific_task(self, task):
        generator = ChainStreamCoTGenerator()
        # TODO: fix this para with a new output description
        agent, latency, tokens = generator.generate_agent(task.output_stream_description, task.input_stream_description)
        return agent, latency, tokens


if __name__ == '__main__':
    task_list = get_task_batch()
    evaluator = EvalCoTGenerator(task_list,task_log_path=r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-21_11-35-00_chainstream-cot\test_log.json')
    evaluator.start()
