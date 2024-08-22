from AgentGenerator.generator.generator_base import FeedbackGuidedAgentGeneratorWithTask
from AgentGenerator.prompt import FilterErrorFeedbackProcessor
from AgentGenerator.prompt import get_base_prompt


class ChainstreamFeedbackGuidedGeneratorForRealTask(FeedbackGuidedAgentGeneratorWithTask):
    """
        React with sandbox starting error ability
    """

    def __init__(self, max_loop=20, sandbox_type='chainstream', only_print_last=False):
        super().__init__(max_loop=max_loop, sandbox_type=sandbox_type, only_print_last=only_print_last)

        self.feedback_processor = FilterErrorFeedbackProcessor()

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(output_stream, input_stream,
                               framework_name='chainstream',
                               example_number=0,
                               mission_name="stream",
                               command_name="feedback_guided_with_real_task",
                               need_feedback_example=True
                               )

    def process_sandbox_feedback(self, sandbox_feedback, has_input=None):
        return self.feedback_processor(sandbox_feedback)

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
    from ChainStreamSandBox.tasks import ALL_TASKS
    generator = ChainstreamFeedbackGuidedGeneratorForRealTask()
    task = ALL_TASKS["EmailTask2"]()
    haha = generator.generate_agent(
        task.output_stream_description,
        input_description=task.input_stream_description,
        task=task,
    )

    agent_code, latency, tokens = haha[0], haha[1], haha[2]

    print(agent_code)
    print(latency)
    print(tokens)
