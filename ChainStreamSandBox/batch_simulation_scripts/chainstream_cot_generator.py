from sandbox_interface import SandboxBatchInterface
from AgentGenerator.generator.stream_mode.chainstream_cot_generator import ChainStreamCoTGenerator
from ChainStreamSandBox.tasks import get_task_with_data_batch


class EvalCoTGenerator(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=5, result_path='./result', task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path, sandbox_type="chainstream")

    def get_agent_for_specific_task(self, task):
        generator = ChainStreamCoTGenerator(example_number=0)
        # TODO: fix this para with a new output description
        agent, latency, tokens = generator.generate_agent(task.output_stream_description, task.input_stream_description)
        return agent, latency, tokens


if __name__ == '__main__':
    task_list = get_task_with_data_batch()
    evaluator = EvalCoTGenerator(task_list)
    evaluator.start()
