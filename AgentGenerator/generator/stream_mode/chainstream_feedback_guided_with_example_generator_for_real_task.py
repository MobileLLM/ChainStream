from AgentGenerator.generator.generator_base import FeedbackGuidedAgentGeneratorWithTask
from AgentGenerator.prompt import FilterErrorWithExampleFeedbackProcessor
from AgentGenerator.prompt import get_base_prompt
from AgentGenerator.io_model import StreamListDescription


class ChainStreamFeedbackGuidedWithExampleAgentGeneratorWithRealTask(FeedbackGuidedAgentGeneratorWithTask):
    """
        React with sandbox starting error ability
    """

    def __init__(self, max_loop=20, sandbox_type='chainstream', only_print_last=False, framework_example_number=0):
        super().__init__(max_loop=max_loop, sandbox_type=sandbox_type, only_print_last=only_print_last)

        self.feedback_processor = FilterErrorWithExampleFeedbackProcessor()

        self.framework_example_number = framework_example_number

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(output_stream, input_stream,
                               framework_name='chainstream',
                               example_number=self.framework_example_number,
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
    generator = ChainStreamFeedbackGuidedWithExampleAgentGeneratorWithRealTask(framework_example_number=0)
    task = ALL_TASKS["HealthTask4"]()
    haha = generator.generate_agent(
        StreamListDescription(streams=[
            {
                "stream_id": "remind_rest",
                "description": "A stream of reminders to take a rest when the heart rate is over 75 in every 2 seconds.",
                "fields": {
                    "Heart Rate": "the heart rate data from the health sensor, float",
                    "reminder": "Heart rate is too high!Remember to rest yourself!"
                }
            }
        ])
        ,
        input_description=task.input_stream_description,
        task=task,
    )

    agent_code, latency, tokens = haha[0], haha[1], haha[2]

    print(agent_code)
    print(latency)
    print(tokens)
