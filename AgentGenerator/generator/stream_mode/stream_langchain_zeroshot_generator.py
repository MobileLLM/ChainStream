from AgentGenerator.prompt import get_base_prompt
from AgentGenerator.generator.generator_base import DirectAgentGenerator


class StreamLangchainZeroshotGenerator(DirectAgentGenerator):
    def __init__(self):
        super().__init__()

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(output_stream, input_stream,
                               framework_name="stream_langchain",
                               example_number=0,
                               mission_name="stream",
                               command_name="few_shot",
                               need_feedback_example=False)

    def process_response(self, response) -> str:
        return response.replace("'''", " ").replace("```", " ").replace("python", "")


if __name__ == '__main__':
    from ChainStreamSandBox.tasks import ALL_TASKS
    task = ALL_TASKS['EmailTask1']()
    agent_generator = StreamLangchainZeroshotGenerator()
    agent_code, latency, tokens = agent_generator.generate_agent(
        task.output_stream_description,
        task.input_stream_description,
    )

    print(agent_code)
    print(latency)
    print(tokens)
