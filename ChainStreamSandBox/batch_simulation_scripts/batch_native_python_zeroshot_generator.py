from sandbox_interface import SandboxBatchInterface
from AgentGenerator import NativePythonZeroShotGenerator
from ChainStreamSandBox.tasks import get_task_with_data_batch
import os


class NativePythonBatchZeroshotEvaluator(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=1, result_path='./result', task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path, sandbox_type="native_python")

    def get_agent_for_specific_task(self, task):
        generator = NativePythonZeroShotGenerator()
        # TODO: fix this para with a new output description
        agent, latency, tokens = generator.generate_agent(task.output_stream_description, task.input_stream_description)
        return agent, latency, tokens


if __name__ == '__main__':
    task_list = get_task_with_data_batch()
    evaluator = NativePythonBatchZeroshotEvaluator(task_list)
    evaluator.start()
