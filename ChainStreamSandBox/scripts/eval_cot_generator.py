from sandbox_batch_interface import SandboxBatchInterface
from AgentGenerator import CoTGenerator


class EvalCoTGenerator(SandboxBatchInterface):
    def __init__(self, task_list, output_path, repeat_time=5, result_path='./result', task_log_path=None):
        super().__init__(task_list, output_path, repeat_time, result_path, task_log_path)

    def get_agent_for_specific_task(self, task) -> str:
        generator = CoTGenerator()
        # TODO: fix this para with a new output description
        agent = generator.generate_agent(task, task)
        return agent
