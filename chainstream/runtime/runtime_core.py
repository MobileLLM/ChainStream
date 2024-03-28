import logging
from .stream_manager import StreamManager
# from .agent_manager import AgentManager


class RuntimeCore(StreamManager):
    def __init__(self):
        super(RuntimeCore, self).__init__()
        self.logger = logging.getLogger(name='RuntimeCore')
        self.verbose = False
        self.output_dir = None


class ChainStreamServerBase(object):
    def __init__(self):
        self.chainstream_core = RuntimeCore()

    def start(self):
        pass

    def config(self, *args, **kwargs):
        pass

    def get_chainstream_core(self):
        return self.chainstream_core
