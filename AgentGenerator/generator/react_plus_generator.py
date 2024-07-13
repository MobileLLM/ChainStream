from .generator_base import ReactAgentGenerator
from ..io_model import StreamListDescription

class ReactPlusGenerator(ReactAgentGenerator):
    def __init__(self):
        super().__init__()

    def generate_agent_impl(self, input_description: [StreamListDescription, None], agent_description: StreamListDescription) -> str:
        pass
