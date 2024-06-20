import logging
from .stream_manager import StreamManager
from .agent_manager import AgentManager
from .llm_manager import LLMManager


class RuntimeCoreOp:
    def __init__(self):
        super(RuntimeCoreOp, self).__init__()
        self.logger = logging.getLogger(name='RuntimeCore')
        self.verbose = False
        self.output_dir = None
        self.default_sql_name = 'chainstream'

        self.agent_manager = AgentManager()
        self.stream_manager = StreamManager()
        self.llm_manager = LLMManager()

    def config(self, *args, **kwargs):
        self.verbose = kwargs.get('verbose', False)
        self.output_dir = kwargs.get('output_dir', None)

    def register_agent(self, agent) -> None:
        self.agent_manager.register_agent(agent)

    def unregister_agent(self, agent) -> None:
        self.agent_manager.unregister_agent(agent)

    def scan_predefined_agents(self) -> list:
        return self.agent_manager.scan_predefined_agents()

    def start_agent_by_id(self, agent_id) -> bool:
        return self.agent_manager.start_agent_by_id(agent_id)

    def stop_agent_by_id(self, agent_id) -> bool:
        return self.agent_manager.stop_agent_by_id(agent_id)

    def remove_agent_by_id(self, agent_id) -> None:
        self.agent_manager.remove_agent_by_id(agent_id)

    def start_agent_by_path(self, agent_path) -> None:
        self.agent_manager.start_agent_by_path(agent_path)

    def scan_predefined_agents_tree(self) -> list:
        return self.agent_manager.scan_predefined_agents_tree()

    def get_running_agents_info_list(self) -> list:
        return self.agent_manager.get_running_agents_info_list()

    def register_stream(self, stream) -> None:
        self.stream_manager.register_stream(stream)

    def unregister_stream(self, stream) -> None:
        self.stream_manager.unregister_stream(stream)

    def get_stream_list(self) -> list:
        return self.stream_manager.get_stream_list()


class RuntimeCoreAnalysisOp(RuntimeCoreOp):
    def __init__(self):
        super().__init__()

    def get_graph_statistics(self):
        agent_file_path_to_agent_id = self.agent_manager.get_agent_file_path_to_agent_id()
        return self.stream_manager.get_graph_statistics(agent_file_path_to_agent_id)


class RuntimeCore(RuntimeCoreAnalysisOp):
    def __init__(self):
        super(RuntimeCore, self).__init__()

