import logging
from .stream_manager import StreamManager
from .agent_manager import AgentManager


class RuntimeCoreOp:
    def __init__(self):
        super(RuntimeCoreOp, self).__init__()
        self.logger = logging.getLogger(name='RuntimeCore')
        self.verbose = False
        self.output_dir = None

        self.agent_manager = AgentManager()
        self.stream_manager = StreamManager()

    def register_agent(self, agent):
        self.agent_manager.register_agent(agent)

    def unregister_agent(self, agent):
        self.agent_manager.unregister_agent(agent)

    def scan_predefined_agents(self):
        self.agent_manager.scan_predefined_agents()

    def start_agent_by_id(self, agent_id):
        self.agent_manager.start_agent_by_id(agent_id)

    def stop_agent_by_id(self, agent_id):
        self.agent_manager.stop_agent_by_id(agent_id)

    def remove_agent_by_id(self, agent_id):
        self.agent_manager.remove_agent_by_id(agent_id)

    def start_agent_by_path(self, agent_path):
        self.agent_manager.start_agent_by_path(agent_path)

    def scan_predefined_agents_tree(self):
        self.agent_manager.scan_predefined_agents_tree()

    def get_running_agents_info_list(self):
        return self.agent_manager.get_running_agents_info_list()

    def register_stream(self, stream):
        self.stream_manager.register_stream(stream)

    def unregister_stream(self, stream):
        self.stream_manager.unregister_stream(stream)

    def get_stream_list(self):
        return self.stream_manager.get_stream_list()


class RuntimeCoreAnalysisOp(RuntimeCoreOp):
    def __init__(self):
        super().__init__()


class RuntimeCore(RuntimeCoreAnalysisOp):
    def __init__(self):
        super(RuntimeCore, self).__init__()


class ChainStreamServerBase(object):
    def __init__(self):
        self.chainstream_core = RuntimeCore()

    def start(self):
        pass

    def config(self, *args, **kwargs):
        pass

    def get_chainstream_core(self):
        return self.chainstream_core
