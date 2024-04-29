from abc import abstractmethod, ABC

import chainstream as cs
import threading
import time
from datetime import datetime

from PIL import Image

from io import BytesIO

# TODO: change all sensors class to this way
class BaseSocketSensors:
    is_agent = False

    USE_GLOBAL_SOCKET_IP = True
    # SOCKET_IP = "192.168.43.226"
    # SOCKET_IP = "192.168.43.41"
    SOCKET_IP = "47.94.168.126"
    SOCKET_PORT = 6677

    def __init__(self, ip='192.168.43.1', port=6666, cmd=None):
        self.socket_thread = None
        self.socket_client = None
        self.cmd = cmd

        self.enabled = True

        self.ip = ip
        self.port = port

    def start(self, func):
        from chainstream.utils import WebSocketClient
        if self.USE_GLOBAL_SOCKET_IP:
            self.socket_client = WebSocketClient(f"ws://{self.SOCKET_IP}:{self.SOCKET_PORT}", on_start_message=self.cmd,
                                                 on_message=func)
        else:
            self.socket_client = WebSocketClient(f"ws://{self.ip}:{self.port}", on_start_message=self.cmd,
                                                 on_message=func)

        self.socket_thread = threading.Thread(target=self.start_thread_func)
        self.socket_thread.start()

        return True

    def start_thread_func(self):
        self.socket_client.start()

    def stop(self):
        self.enabled = False
        self.socket_client.close()
