from .server import ChainStreamServer, ChainStreamServerShell

cs_server = ChainStreamServerShell()
cs_server_core = cs_server.get_chainstream_core()

def platform():
    return 'cuda'

