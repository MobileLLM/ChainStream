from AgentGenerator.generator.generator_base import FeedbackGuidedAgentGeneratorWithTask
from AgentGenerator.prompt import get_base_prompt


class StreamNativePythonFeedbackWithRealTask(FeedbackGuidedAgentGeneratorWithTask):
    def __init__(self, max_loop=20, sandbox_type='stream_interface'):
        super().__init__(max_loop=max_loop, sandbox_type=sandbox_type)

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(output_stream, input_stream,
                               framework_name="stream_native_python",
                               example_number=0,
                               mission_name="stream",
                               command_name="feedback_guided_with_real_task",
                               need_feedback_example=True)

    def process_sandbox_feedback(self, sandbox_feedback, has_input=None):
        if sandbox_feedback['start_agent'] != "[OK]":
            return f"After executing the code, the sandbox reported: {sandbox_feedback['start_agent']}"
        else:
            return f"Your code can run without any error. The output of the code is: {sandbox_feedback['output_stream_items']}"

    def step(self, code) -> (str, bool):
        done = False

        try:
            entity = code.strip()
            if entity.startswith("```python") and entity.endswith("```"):
                entity = entity[len("```python"):-3].strip()
            obs = self.sandbox_exec(entity, use_real_task=True)

        except Exception as e:
            obs = f"[SandboxError] {e}"

        return obs, done


if __name__ == '__main__':
    from ChainStreamSandBox.tasks.email_task.task_1 import EmailTask1

    generator = StreamNativePythonFeedbackWithRealTask()
    task = EmailTask1()
    agent_code, latency, tokens = generator.generate_agent(
        task.output_stream_description,
        input_description=task.input_stream_description,
        task=task,
    )

    print(agent_code)
    print(latency)
    print(tokens)
