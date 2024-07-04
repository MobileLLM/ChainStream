from ChainStreamSandBox import SandBox


class AgentGeneratorBase:
    def generate_dsl(self, task_description, input_description, output_description):
        raise NotImplementedError


class ReactAgentGenerator(AgentGeneratorBase):
    def __init__(self):
        self.sandbox_class = SandBox
