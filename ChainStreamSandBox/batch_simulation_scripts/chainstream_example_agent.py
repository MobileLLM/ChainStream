from sandbox_interface import SandboxBatchInterface
from ChainStreamSandBox.tasks import get_task_batch
import os


class EvalExampleAgent(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=1, result_path=os.path.normpath(os.path.join(os.path.dirname(__file__), "result")), task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path, sandbox_type='chainstream')

    def get_agent_for_specific_task(self, task):
        return task.agent_example, None, None


if __name__ == '__main__':
    task_list = get_task_batch()
    eval_agent = EvalExampleAgent(task_list, repeat_time=1)
    eval_agent.start()
