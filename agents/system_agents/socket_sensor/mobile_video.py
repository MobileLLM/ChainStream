from datetime import datetime

from agents.system_agents.socket_sensor.sensor.base_socket_sensor import BaseSocketSensors

from PIL import Image

from io import BytesIO


class VideoSocketSensors(BaseSocketSensors):
    is_agent = True
    def __init__(self, agent_id='sys_socket_video_sensors', video_fps=0.1, ip='192.168.43.41', port=6666):
        super().__init__(agent_id, stream_name="socket_front_camera_video", ip=ip, port=port)
        self.video_fps = video_fps

        self.cmd = f"video,{int(1000 / float(self.video_fps))}"

    def get_on_message(self):
        def on_message(ws, frame):
            self.stream.send_item({'timestamp': datetime.now(), 'frame': Image.open(BytesIO(frame))})
            image = Image.open(BytesIO(frame))
            image.show()
            # self.logger.info()

        return on_message




if __name__ == '__main__':
    ip = '192.168.43.226'
    default_sensors_agent = VideoSocketSensors(ip=ip)
    default_sensors_agent.start()
    # while True:
    #     cmd = input('> ')
    #     if cmd == 'q':
    #         default_sensors_agent.stop()
    #         break
