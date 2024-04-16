from .runtime_core import ChainStreamServerBase


class ChainStreamServerWeb(ChainStreamServerBase):
    def __init__(self):
        super().__init__()
        self.ip = None
        self.port = None

        from .web.backend.core import set_core
        set_core(self.chainstream_core)
        from .web.backend.app import app
        self.app = app

    def config(self, *args, **kwargs):
        self.ip = kwargs.get('ip', '127.0.0.1')
        self.port = kwargs.get('port', 6677)
        self.config(args, kwargs)

    def start(self):
        print(self.ip, self.port)
        self.app.run(host=self.ip, port=self.port)
        pass
