from .sandbox_base import SandboxBase
import os

class NativePythonSandbox(SandboxBase):
    def __init__(self, task, agent_code, save_result=True, save_path=os.path.join(os.path.dirname(__file__), 'results'),
                 raise_exception=True, only_init_agent=False):
        super().__init__(task, agent_code, save_result=save_result, save_path=save_path,
                         raise_exception=raise_exception, only_init_agent=only_init_agent, sandbox_type="native_python")

    def prepare_environment(self):
        raise NotImplementedError("Subclasses must implement prepare_environment")

    def start_agent(self) -> object:
        raise NotImplementedError("Subclasses must implement start_agent")

    def start_task(self) -> list:
        raise NotImplementedError("Subclasses must implement start_task")

    def wait_task_finish(self):
        raise NotImplementedError("Subclasses must implement wait_task_finish")

    def get_output_list(self) -> list:
        raise NotImplementedError("Subclasses must implement get_output_list")

    def get_runtime_report(self) -> dict:
        raise NotImplementedError("Subclasses must implement get_runtime_report")

    def get_error_msg(self) -> dict:
        raise NotImplementedError("Subclasses must implement get_error_msg")

    def stop_runtime(self):
        raise NotImplementedError("Subclasses must implement stop_runtime")

