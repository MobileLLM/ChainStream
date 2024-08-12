from sandbox_batch_interface import SandboxBatchInterface
from AgentGenerator import ReactGeneratorForDebugging
from ChainStreamSandBox.tasks import get_task_batch

class EvalReactPlusGenerator(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=5, result_path='./result', task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path, sandbox_type="chainstream")

    def get_agent_for_specific_task(self, task) -> str:
        generator = ReactGeneratorForDebugging()
        # TODO: fix this para with a new output description
        agent = generator.generate_agent(task.output_stream_description, task.input_stream_description)
        return agent


if __name__ == '__main__':
    task_list = get_task_batch()
    evaluator = EvalReactPlusGenerator(task_list)
    evaluator.start()