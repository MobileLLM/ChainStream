from sandbox_interface import SandboxBatchInterface
from AgentGenerator import NativeGPTGenerator
from ChainStreamSandBox.tasks import get_task_with_data_batch


class NativeGPTBatchInterface(SandboxBatchInterface):
    def __init__(self, task_list, model_name, repeat_time=1, result_path='./result', task_log_path=None):
        self.model_name = model_name

        super().__init__(task_list, repeat_time, result_path, task_log_path, sandbox_type="native_python_batch")

    def get_agent_for_specific_task(self, task) -> object:
        generator = NativeGPTGenerator(model_name=self.model_name)
        agent, _, _ = generator.generate_agent(task.output_stream_description, task.input_stream_description)

        for i, line in enumerate(agent.split('\n')):
            print(f"{i + 1}. {line}")

        return agent, None, None


if __name__ == '__main__':
    task_list = get_task_with_data_batch()
    gpt = NativeGPTBatchInterface(task_list, "gpt-4o")
    gpt.start()
