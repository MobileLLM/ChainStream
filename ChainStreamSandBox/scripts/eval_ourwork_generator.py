from sandbox_batch_interface import SandboxBatchInterface
from AgentGenerator import ReactPlusGenerator


class EvalReactPlusGenerator(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=5, result_path='./result', task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path)

    def get_agent_for_specific_task(self, task) -> str:
        generator = ReactPlusGenerator()
        # TODO: fix this para with a new output description
        agent = generator.generate_agent(task, task)
        return agent
