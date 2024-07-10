from sandbox_batch_interface import SandboxBatchInterface


class EvalExampleAgent(SandboxBatchInterface):
    def __init__(self, task_list, output_path, repeat_time=5, result_path='./result', task_log_path=None):
        super().__init__(task_list, output_path, repeat_time, result_path, task_log_path)

    def get_agent_for_specific_task(self, task) -> str:
        return task.agent_example


if __name__ == '__main__':
    pass
