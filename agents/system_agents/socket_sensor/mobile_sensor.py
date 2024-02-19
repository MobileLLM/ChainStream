import chainstream as cs
import threading
from datetime import datetime

from base_socket_sensor import BaseSocketSensors

from PIL import Image

from io import BytesIO



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
    ip = '192.168.43.41'
    default_sensors_agent = SensorSocketSensors(ip=ip)
    default_sensors_agent.start()
    # while True:
    #     cmd = input('> ')
    #     if cmd == 'q':
    #         default_sensors_agent.stop()
    #         break
