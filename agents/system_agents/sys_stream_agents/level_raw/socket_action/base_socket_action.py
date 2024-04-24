import chainstream as cs


class BaseSocketActions(cs.agent.Agent):
    is_agent = False

    USE_GLOBAL_SOCKET_IP = False
    # SOCKET_IP = "192.168.43.226"
    # SOCKET_IP = "192.168.43.41"
    SOCKET_IP = "47.94.168.126"
    SOCKET_PORT = 6000

    def __init__(self, agent_id='default_socket_actions', cmd='log', stream_name=None, ip='192.168.43.1', port=6666):
        super().__init__(agent_id)
        self.socket_client = None
        self.stream = cs.stream.create_stream(stream_name)

        self.cmd = cmd

        self.ip = ip
        self.port = port

        from chainstream.utils import WebSocketClient
        if self.USE_GLOBAL_SOCKET_IP:
            self.socket_client = WebSocketClient(f"ws://{self.SOCKET_IP}:{self.SOCKET_PORT}")
        else:
            self.socket_client = WebSocketClient(f"ws://{self.ip}:{self.port}")

    def start(self):
        def handel_new_action(log):
            self.socket_client.send_message(f"{self.cmd},{log}")

        self.stream.register_listener(self, handel_new_action)

    def stop(self):
        self.socket_client.close()
