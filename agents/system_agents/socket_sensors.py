import chainstream as cs
import threading
import time
from datetime import datetime


from PIL import Image

from io import BytesIO


class SocketSensors(cs.agent.Agent):
    def __init__(self, agent_id='default_sensors', video_fps=1, audio_duration=1, ip='192.168.43.1', port=6666):
        super().__init__(agent_id)
        self.video_fps = video_fps
        self.audio_duration = audio_duration
        self.front_camera_video = cs.stream.create_stream('socket_front_camera_video')
        self.front_camera_thread = None
        # self.microphone_audio = cs.stream.create_stream('socket_microphone_audio')
        # self.microphone_thread = None
        self.enabled = True

        self.ip = ip
        self.port = port

        from chainstream.utils import WebSocketClient
        self.front_camera_video_cli = WebSocketClient(f"ws://{self.ip}:{self.port}", on_start_message="video,1",
                                                      on_message=self._front_camera_video_get_on_message())

    def start(self):
        self.front_camera_thread = threading.Thread(target=self.capture_images)
        self.front_camera_thread.start()
        # self.microphone_thread = threading.Thread(target=self.capture_audio)
        # self.microphone_thread.start()

    def _front_camera_video_get_on_message(self):
        def on_message(ws, frame):
            self.front_camera_video.send_item({'timestamp': datetime.now(), 'frame': frame})
            image = Image.open(BytesIO(frame))
            image.show()
            # self.logger.info()

        return on_message

    def capture_images(self):
        self.front_camera_video_cli.start()

    # def capture_audio(self):
    #     # TODO implement this and other sensors
    #     pass

    def stop(self):
        self.enabled = False
        self.front_camera_video_cli.close()


if __name__ == '__main__':
    default_sensors_agent = SocketSensors()
    default_sensors_agent.start()
    # while True:
    #     cmd = input('> ')
    #     if cmd == 'q':
    #         default_sensors_agent.stop()
    #         break
