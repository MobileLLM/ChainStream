from ChainStreamSandBox import ChainStreamSandBox
from AgentGenerator.io_model import StreamListDescription
from AgentGenerator.stream_selector import StreamSelectorBase
from AgentGenerator.prompt.chainstream_doc import chainstream_chinese_doc, chainstream_english_doc, chainstream_english_doc_with_1_example, chainstream_english_doc_with_2_example
from AgentGenerator.prompt import REACT_PROMPT_ONLY_START


class AgentGeneratorBase:
    """
    Three mode of generator:
    1. work as a part of a running Runtime, serve for a real system, select input stream and agents and other information from the Runtime.
    2. work alone with stream and agent information, usually for sandbox testing or other purposes, need to provide input stream and other information manually.
    3. [Default] work alone without any information, need to provide input stream and agent information in the generate_dsl function manually.
    """
    def __init__(self, runtime=None):
        self.runtime = runtime
        self.stream_selector = StreamSelectorBase()

        self.output_description = None
        self.input_description = None

    def generate_agent(self, output_description, input_description=None, use_selector=False) -> str:
        self.output_description = output_description
        self.input_description = input_description

        self.stream_selector.set_all_stream_list(input_description)

        # Do not specify input_description, let llm make up the input stream
        if input_description is None:
            input_and_output_prompt = self.stream_selector.select_stream(output_description, select_policy='none')
            # return self.generate_agent_impl(None, output_description)
        else:
            if not use_selector:
                # Specify input_description, use all input streams
                input_and_output_prompt = self.stream_selector.select_stream(output_description, select_policy='all')
                # return self.generate_agent_impl(input_description, output_description)
            else:
                # Specify input_description, use llm to select input streams
                input_and_output_prompt = self.stream_selector.select_stream(output_description, select_policy='llm')

        # basic_prompt = f"{chainstream_chinese_doc}\n{input_and_output_prompt}"

        return self.generate_agent_impl(chainstream_english_doc, input_and_output_prompt)

    # def generate_agent_impl(self, input_description: [StreamListDescription, None], output_description:
    # StreamListDescription) -> str: raise NotImplementedError("Agent generator must implement generate_agent_impl
    # function.")

    def generate_agent_impl(self, chainstream_doc: str, input_and_output_prompt: str) -> str:
        raise NotImplementedError("Agent generator must implement generate_agent_impl function.")

    def generate_agent_for_runtime(self, output_description: StreamListDescription):
        if self.runtime is None or self.stream_selector is None:
            raise ValueError("Runtime and stream selector must be provided for agent generation in runtime mode.")

        # TODO: this API is still under development
        stream_list = self.runtime.get_stream_description_list()

        agent = self.generate_agent(output_description, input_description=stream_list, use_selector=True)

        return agent


class ReactAgentGenerator(AgentGeneratorBase):
    def __init__(self, runtime=None):
        super().__init__(runtime)
        self.sandbox_class = ChainStreamSandBox


