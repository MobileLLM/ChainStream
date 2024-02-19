from abc import abstractmethod, ABC

import chainstream as cs
import threading
import time
from datetime import datetime

from PIL import Image

from io import BytesIO


class BaseSocketSensors(cs.agent.Agent):
    is_agent = False
    def __init__(self, agent_id='default_sensors', stream_name=None, ip='192.168.43.1', port=6666):
        super().__init__(agent_id)
        self.socket_thread = None
        self.socket_client = None
        self.stream = cs.stream.create_stream(stream_name)
        self.enabled = True

        self.ip = ip
        self.port = port

    def start(self):
        from chainstream.utils import WebSocketClient
        self.socket_client = WebSocketClient(f"ws://{self.ip}:{self.port}", on_start_message=self.cmd,
                                             on_message=self.get_on_message())

        self.socket_thread = threading.Thread(target=self.start_thread_func)
        self.socket_thread.start()

        return True

    @abstractmethod
    def get_on_message(self):
        pass

    def start_thread_func(self):
        self.socket_client.start()

    def stop(self):
        self.enabled = False
        self.socket_client.close()
