import chainstream as cs
from datetime import datetime
from io import BytesIO
import time
import threading


class DebugVideoSocketSensors(cs.agent.Agent):
    is_agent = True

    def __init__(self, agent_id='sys_socket_video_sensors'):
        super().__init__(agent_id)
        self.stream = cs.stream.create_stream("socket_front_camera_video")
        self.enable = True

        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.send_empty())
        self.thread.start()

        return True

    def send_empty(self):
        while self.enable:
            self.stream.send_item({'timestamp': datetime.now(), 'frame': BytesIO()})
            time.sleep(10)

    def stop(self):
        self.enable = False
