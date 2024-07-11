from ChainStreamSandBox import SandBox
from ..io_model import StreamListDescription


class AgentGeneratorBase:
    """
    Three mode of generator:
    1. work as a part of a running Runtime, serve for a real system, select input stream and agents and other information from the Runtime.
    2. work alone with stream and agent information, usually for sandbox testing or other purposes, need to provide input stream and other information manually.
    3. [Default] work alone without any information, need to provide input stream and agent information in the generate_dsl function manually.
    """
    def __init__(self, runtime=None, stream_selector=None):
        self.runtime = runtime
        self.stream_selector = stream_selector

    def generate_agent(self, output_description, input_description=None, use_selector=False) -> str:
        if input_description is None:
            return self.generate_agent_impl(None, output_description)
        if not use_selector:
            return self.generate_agent_impl(input_description, output_description)

        if self.stream_selector is None:
            raise ValueError("Stream selector must be provided for agent generation with stream selector.")

        selected_streams = self.stream_selector.select_streams(input_description)

        return self.generate_agent_impl(selected_streams, output_description)

    def generate_agent_impl(self, input_description: [StreamListDescription, None], agent_description: StreamListDescription) -> str:
        raise NotImplementedError("Agent generator must implement generate_agent_impl function.")

    def generate_agent_for_runtime(self, output_description: StreamListDescription):
        if self.runtime is None or self.stream_selector is None:
            raise ValueError("Runtime and stream selector must be provided for agent generation in runtime mode.")

        # TODO: this API is still under development
        stream_list = self.runtime.get_stream_description_list()

        agent = self.generate_agent(stream_list, output_description, use_selector=True)

        return agent


class ReactAgentGenerator(AgentGeneratorBase):
    def __init__(self, runtime=None, stream_selector=None):
        super().__init__(runtime, stream_selector)
        self.sandbox_class = SandBox
