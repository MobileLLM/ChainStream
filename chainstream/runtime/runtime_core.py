import logging
from .stream_manager import StreamManager
from .agent_manager import AgentManager
from .error_manager import ErrorManager
from .device_manager import DeviceManager
from chainstream.llm import reset_model_instances


class RuntimeCoreOp:
    def __init__(self):
        super(RuntimeCoreOp, self).__init__()
        self.logger = logging.getLogger(name='RuntimeCore')
        self.verbose = False
        self.output_dir = None
        self.default_sql_name = 'chainstream'

        self.agent_manager = AgentManager()
        self.stream_manager = StreamManager()
        self.error_manager = ErrorManager()
        self.device_manager = DeviceManager()

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

    def wait_all_stream_clear(self) -> bool:
        return self.stream_manager.wait_all_stream_clear()

    def record_error(self, error_type, error_message, error_traceback) -> None:
        self.error_manager.record_error(error_type, error_message, error_traceback)

    def get_error_history(self) -> list:
        return self.error_manager.get_error_history()

    def shutdown(self) -> None:
        # print('Shutting down runtime core...')
        self.agent_manager.shutdown()
        # print('Runtime core shutdown complete.')
        self.stream_manager.shutdown()
        # print('Stream manager shutdown complete.')

        reset_model_instances()


class RuntimeCoreAnalysisOp(RuntimeCoreOp):
    def __init__(self):
        super().__init__()

    def get_graph_statistics(self):
        agent_file_path_to_agent_id = self.agent_manager.get_agent_file_path_to_agent_id()
        return self.stream_manager.get_graph_statistics(agent_file_path_to_agent_id)

    def get_agent_report(self, agent_id):
        pass


class RuntimeCore(RuntimeCoreAnalysisOp):
    def __init__(self):
        super(RuntimeCore, self).__init__()
