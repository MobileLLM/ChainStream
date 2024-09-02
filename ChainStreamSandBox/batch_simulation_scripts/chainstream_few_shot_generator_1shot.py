from sandbox_interface import SandboxBatchInterface
from AgentGenerator import ChainStreamFewShotGenerator
from ChainStreamSandBox.tasks import get_task_with_data_batch


class FewShotEvaluator(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=5, result_path='./result', task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path, sandbox_type="chainstream")

    def get_agent_for_specific_task(self, task):
        generator = ChainStreamFewShotGenerator(example_number=1)
        generator.set_verbose(True)
        # TODO: fix this para with a new output description
        agent, latency, tokens = generator.generate_agent(task.output_stream_description, task.input_stream_description, task=task)
        return agent, latency, tokens


if __name__ == '__main__':
    task_list = get_task_with_data_batch()
    evaluator = FewShotEvaluator(task_list, task_log_path="/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-01_15-37-55_chainstream_fewshot_1shot/test_log.json")
    evaluator.start()
