import chainstream as cs
import threading


class BaseSocketActions:
    is_agent = False

    USE_GLOBAL_SOCKET_IP = False
    # SOCKET_IP = "192.168.43.226"
    # SOCKET_IP = "192.168.43.41"
    SOCKET_IP = "47.94.168.126"
    SOCKET_PORT = 6000

    def __init__(self, cmd='log', stream_name=None, ip='192.168.43.41', port=6666):
        self.socket_client = None
        if stream_name is not None:
            self.stream = cs.stream.create_stream(stream_name)
        else:
            raise RuntimeError("Stream name not provided")

        self.cmd = cmd
        self.ip = ip
        self.port = port

        from chainstream.utils import WebSocketClient
        if self.USE_GLOBAL_SOCKET_IP:
            self.socket_client = WebSocketClient(f"ws://{self.SOCKET_IP}:{self.SOCKET_PORT}")
        else:
            self.socket_client = WebSocketClient(f"ws://{self.ip}:{self.port}")
        self.socket_thread = threading.Thread(target=lambda: self.socket_client.start())
        self.socket_thread.start()

    def register_func(self, agent):
        def handel_new_action(log):
            # print(f"{self.cmd},{log}")
            self.socket_client.send_message(f"{self.cmd},{log}")

        self.stream.register_listener(agent, handel_new_action)

    def stop(self):
        if self.socket_client is not None:
            self.socket_client.close()
