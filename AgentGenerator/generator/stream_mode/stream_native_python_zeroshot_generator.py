from AgentGenerator.prompt import get_base_prompt
from AgentGenerator.generator.generator_base import DirectAgentGenerator


class StreamNativePythonZeroshotGenerator(DirectAgentGenerator):
    def __init__(self, example_number=0):
        super().__init__()

        self.example_number = example_number

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(output_stream, input_stream,
                               framework_name="stream_native_python",
                               example_number=self.example_number,
                               mission_name="stream",
                               command_name="few_shot",
                               need_feedback_example=False)

    def process_response(self, response) -> str:
        return response.replace("'''", " ").replace("```", " ").replace("python", "")


if __name__ == '__main__':
    from ChainStreamSandBox.tasks import ALL_TASKS
    task = ALL_TASKS['EmailTask1']()
    agent_generator = StreamNativePythonZeroshotGenerator()
    agent_code, latency, tokens = agent_generator.generate_agent(
        task.output_stream_description,
        task.input_stream_description,
    )

    print(agent_code)
    print(latency)
    print(tokens)

