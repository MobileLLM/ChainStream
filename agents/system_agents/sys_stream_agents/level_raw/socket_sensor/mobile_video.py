from datetime import datetime
import chainstream as cs
from agents.system_agents.sys_stream_agents.level_raw.socket_sensor.base_socket_sensor import BaseSocketSensors

from PIL import Image

from io import BytesIO


class VideoSocketSensors(cs.agent.Agent):
    is_agent = True

    def __init__(self, agent_id='sys_socket_video_sensors', video_fps=1, ip='192.168.43.41', port=6666, cameraID=1):
        super().__init__(agent_id)
        self.video_fps = video_fps
        self.cmd = f"video,{int(1000 / float(self.video_fps))},{cameraID}"
        self.stream = cs.stream.create_stream("socket_front_camera_video")
        self.base_socket = BaseSocketSensors(ip=ip, port=port, cmd=self.cmd)

    def start(self):
        def on_message(ws, frame):
            self.stream.send_item({'timestamp': datetime.now(), 'frame': Image.open(BytesIO(frame))})
            # image = Image.open(BytesIO(frame))
            # image.show()
            # self.logger.info()
        self.base_socket.start(on_message)

        return True

    def stop(self):
        self.base_socket.stop()


if __name__ == '__main__':
    ip = '192.168.20.134'
    default_sensors_agent = VideoSocketSensors(ip=ip)
    default_sensors_agent.start()
    # while True:
    #     cmd = input('> ')
    #     if cmd == 'q':
    #         default_sensors_agent.stop()
    #         break
