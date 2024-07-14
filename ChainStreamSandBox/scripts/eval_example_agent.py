from ChainStreamSandBox.sandbox_batch_interface import SandboxBatchInterface
from ChainStreamSandBox.tasks import get_task_batch
import os


class EvalExampleAgent(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=5, result_path=os.path.normpath(os.path.join(os.path.dirname(__file__), "result")), task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path)

    def get_agent_for_specific_task(self, task) -> str:
        return task.agent_example


if __name__ == '__main__':
    task_list = get_task_batch()
    eval_agent = EvalExampleAgent(task_list, repeat_time=1, task_log_path=r"C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result\2024-07-14_18-28-26\test_log.json")
    eval_agent.start()
