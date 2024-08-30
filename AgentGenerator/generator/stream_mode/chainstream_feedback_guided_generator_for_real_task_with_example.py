from AgentGenerator.generator.generator_base import FeedbackGuidedAgentGeneratorWithTask
from AgentGenerator.prompt import FilterErrorWithExampleFeedbackProcessor
from AgentGenerator.prompt import get_base_prompt
from AgentGenerator.io_model import StreamListDescription


class ChainstreamFeedbackGuidedGeneratorForRealTaskWithExample(FeedbackGuidedAgentGeneratorWithTask):
    """
        React with sandbox starting error ability
    """

    def __init__(self, task_name_now, max_loop=20, sandbox_type='chainstream', only_print_last=False, framework_example_number=0, feedback_example_number=3):
        super().__init__(max_loop=max_loop, sandbox_type=sandbox_type, only_print_last=only_print_last)

        self.task_name_now = task_name_now

        self.feedback_processor = FilterErrorWithExampleFeedbackProcessor(self.task_name_now, feedback_example_num=feedback_example_number)

        self.framework_example_number = framework_example_number

        self.selected_example_name = []


    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(output_stream, input_stream,
                               framework_name='chainstream',
                               example_number=self.framework_example_number,
                               mission_name="stream",
                               command_name="feedback_guided_with_real_task",
                               need_feedback_example=True,
                               task_now=self.task.__class__.__name__
                               )

    def process_sandbox_feedback(self, sandbox_feedback, has_input=None):
        feedback, example_name = self.feedback_processor(sandbox_feedback, self.last_agent_code)
        if has_input is not None:
            self.selected_example_name.append(example_name)
        return feedback

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
    from ChainStreamSandBox.tasks import get_task_with_data_batch
    all_tasks = get_task_with_data_batch()
    task = all_tasks["MultiTask1"]()
    generator = ChainstreamFeedbackGuidedGeneratorForRealTaskWithExample(task.__class__.__name__, framework_example_number=0)
    haha = generator.generate_agent(
        task.output_stream_description
        ,
        input_description=task.input_stream_description,
        task=task,
    )

    agent_code, latency, tokens = haha[0], haha[1], haha[2]

    print(agent_code)
    print(latency)
    print(tokens)
