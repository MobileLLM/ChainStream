from .server import ChainStreamServer

cs_server = ChainStreamServer()
cs_server_core = cs_server.get_chainstream_core()


# def config_chainstream_server(*args, **kwargs):
#     global cs_server, cs_server_core
#     monitor_mode = kwargs.get('monitor_mode', 'web')
#     if monitor_mode == 'web':
#         cs_server = ChainStreamServerWeb(*args, **kwargs)
#         cs_server_core = cs_server.get_chainstream_core()
#     elif monitor_mode == 'shell':
#         cs_server = ChainStreamServerShell(*args, **kwargs)
#         cs_server_core = cs_server.get_chainstream_core()


def reset_chainstream_server():
    global cs_server, cs_server_core
    del cs_server, cs_server_core
    cs_server = ChainStreamServer()
    cs_server_core = cs_server.get_chainstream_core()
    print('ChainStream server reset')


def platform():
    return 'cuda'
