import logging
from .stream_manager import StreamManager


class ChainStreamCore(StreamManager):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(name='ChainStreamCore')
        self.verbose = False
        self.output_dir = None


class ChainStreamServerBase(object):
    def __init__(self):
        self.chainstream_core = ChainStreamCore()

    def start(self):
        pass

    def config(self, *args, **kwargs):
        pass

    def get_chainstream_core(self):
        return self.chainstream_core
