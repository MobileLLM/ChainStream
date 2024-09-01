from sandbox_interface import SandboxBatchInterface
from AgentGenerator import StreamLangchainZeroshotGenerator
from ChainStreamSandBox.tasks import get_task_with_data_batch


class StreamLangchainZeroshotBatchGenerator(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=5, result_path='./result', task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path, sandbox_type="stream_interface")

    def get_agent_for_specific_task(self, task) -> object:
        generator = StreamLangchainZeroshotGenerator()

        agent, latency, tokens = generator.generate_agent(task.output_stream_description, task.input_stream_description)
        return agent, latency, tokens


if __name__ == '__main__':
    task_list = get_task_with_data_batch()
    evaluator = StreamLangchainZeroshotBatchGenerator(task_list, task_log_path=r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-09-01_01-46-22_langchain_zero_shot\test_log.json')
    evaluator.start()
