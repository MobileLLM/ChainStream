class ChainStreamServerWeb():
    def __init__(self, core):
        self.ip = None
        self.port = None
        self.chainstream_core = core

        from .web.backend.core import set_core
        set_core(self.chainstream_core)
        from .web.backend.app import app
        self.app = app


    def config(self, *args, **kwargs):
        self.ip = kwargs.get('ip', '127.0.0.1')
        self.port = kwargs.get('port', 6677)

    def start(self):
        print(self.ip, self.port)
        self.app.run(host=self.ip, port=self.port)
        pass
