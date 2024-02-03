import chainstream as cs
import threading
from datetime import datetime

from base_socket_sensor import BaseSocketSensors

from PIL import Image

from io import BytesIO


class VideoSocketSensors(BaseSocketSensors):
    def __init__(self, agent_id='sys_socket_video_sensors', video_fps=1, ip='192.168.43.1', port=6666):
        super().__init__(agent_id, stream_name="socket_front_camera_video", ip=ip, port=port)
        self.video_fps = video_fps

        self.cmd = f"video,{int(1000 / float(self.video_fps))}"

    def get_on_message(self):
        def on_message(ws, frame):
            self.stream.send_item({'timestamp': datetime.now(), 'frame': frame})
            image = Image.open(BytesIO(frame))
            image.show()
            # self.logger.info()

        return on_message


class AudioSocketSensors(BaseSocketSensors):
    def __init__(self, agent_id='sys_socket_audio_sensors', audio_duration=1, audio_interval=1, ip='192.168.43.1', port=6666):
        super().__init__(agent_id, stream_name="socket_microphone_audio", ip=ip, port=port)
        self.audio_duration = int(audio_duration) * 1000
        self.audio_interval = int(audio_interval) * 1000

        self.cmd = f"audio,{self.audio_duration},{self.audio_interval}"

    def get_on_message(self):
        def on_message(ws, amr_file):
            # TODO: convert ame file to other format
            self.stream.send_item({'timestamp': datetime.now(), 'data': amr_file})

            # self.logger.info()

        return on_message

class SensorSocketSensors(BaseSocketSensors):
    def __init__(self, agent_id='sys_socket_sensor_sensors', ip='192.168.43.1', port=6666):
        super().__init__(agent_id, stream_name="socket_sensor", ip=ip, port=port)

        # TODO: add sensor data type
        self.cmd = f"sensor,"

        pass

    def get_on_message(self):
        def on_message(ws, sensor_data):
            # TODO: convert sensor_data
            self.stream.send_item({'timestamp': datetime.now(), 'data': sensor_data})

            # self.logger.info()

        return on_message


if __name__ == '__main__':
    default_sensors_agent = VideoSocketSensors()
    default_sensors_agent.start()
    # while True:
    #     cmd = input('> ')
    #     if cmd == 'q':
    #         default_sensors_agent.stop()
    #         break
