import logging
from .stream_manager import StreamManager
from .agent_manager import AgentManager
from .error_manager import ErrorManager
from .device_manager import DeviceManager
from ..user import UserManager, User
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
        self.user_manager = UserManager()

    def config(self, *args, **kwargs):
        self.verbose = kwargs.get('verbose', False)
        self.output_dir = kwargs.get('output_dir', None)
        
    def login(self, username, password):
        res = self.user_manager.login(username, password)
        
        if not isinstance(res, User):
            raise RuntimeError('login failed')
        
        return res

    def register_agent(self, agent, user) -> None:
        self.agent_manager.register_agent(agent, user)

    def unregister_agent(self, agent, user) -> None:
        self.agent_manager.unregister_agent(agent, user)

    def scan_predefined_agents(self) -> list:
        return self.agent_manager.scan_predefined_agents()

    def start_agent_by_id(self, agent_id, user) -> bool:
        return self.agent_manager.start_agent_by_id(agent_id, user)

    def stop_agent_by_id(self, agent_id, user) -> bool:
        return self.agent_manager.stop_agent_by_id(agent_id, user)

    def remove_agent_by_id(self, agent_id, user) -> None:
        self.agent_manager.remove_agent_by_id(agent_id, user)

    def start_agent_by_path(self, agent_path, user) -> None:
        self.agent_manager.start_agent_by_path(agent_path, user)

    def scan_predefined_agents_tree(self) -> list:
        return self.agent_manager.scan_predefined_agents_tree()

    def get_running_agents_info_list(self, user) -> list:
        return self.agent_manager.get_running_agents_info_list(user)

    def register_stream(self, stream, user) -> None:
        self.stream_manager.register_stream(stream, user)

    def unregister_stream(self, stream, user) -> None:
        self.stream_manager.unregister_stream(stream, user)

    def get_stream_list(self, user) -> list:
        return self.stream_manager.get_stream_list(user)

    def wait_all_stream_clear(self, user) -> bool:
        return self.stream_manager.wait_all_stream_clear(user)

    def record_error(self, error_type, error_message, error_traceback, user) -> None:
        self.error_manager.record_error(error_type, error_message, user, error_traceback)

    def get_error_history(self, user) -> list:
        return self.error_manager.get_error_history(user)

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

    def get_graph_statistics(self, user):
        agent_file_path_to_agent_id = self.agent_manager.get_agent_file_path_to_agent_id()
        return self.stream_manager.get_graph_statistics(agent_file_path_to_agent_id, user)

    def get_agent_report(self, agent_id):
        pass


class RuntimeCore(RuntimeCoreAnalysisOp):
    def __init__(self):
        super(RuntimeCore, self).__init__()
