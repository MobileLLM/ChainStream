from chainstream.runtime.runtime_core import RuntimeCore
from .server_shell import ChainStreamServerShell
from .server_web import ChainStreamServerWeb


class ChainStreamServer(object):

    def __init__(self) -> None:
        self.instance = None
        self.runtime_core = RuntimeCore()

    def init(self, server_type='web'):
        if server_type == 'web':
            self.instance = ChainStreamServerWeb(self.runtime_core)
        elif server_type == 'core':
            self.instance = None
        else:
            self.instance = ChainStreamServerShell(self.runtime_core)

    def get_inst(self):
        if not self.instance:
            print('ChainStreamServer not initialized')
            exit(-1)
        return self.instance

    def start(self):
        if self.instance:
            self.get_inst().start()

    def config(self, *args, **kwargs):
        self.get_inst().config(args, kwargs)

    def get_chainstream_core(self):
        return self.runtime_core
