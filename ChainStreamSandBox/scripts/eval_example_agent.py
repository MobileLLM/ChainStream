from sandbox_batch_interface import SandboxBatchInterface
from ChainStreamSandBox.tasks import get_task_batch


class EvalExampleAgent(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=5, result_path='./result', task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path)

    def get_agent_for_specific_task(self, task) -> str:
        return task.agent_example


if __name__ == '__main__':
    task_list = get_task_batch()
    eval_agent = EvalExampleAgent(task_list, repeat_time=1)
    eval_agent.start()
