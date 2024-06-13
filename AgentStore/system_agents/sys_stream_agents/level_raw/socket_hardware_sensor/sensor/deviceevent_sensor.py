# from datetime import datetime
#
# from agents.system_agents.socket_sensor.sensor.base_socket_sensor import BaseSocketSensors
#
#
# class DeviceEventSocketSensors(BaseSocketSensors):
#     is_agent = True
#
#     def __init__(self, agent_id='sys_socket_sensor_sensors_deviceevent', ip='192.168.43.1', port=6666):
#         super().__init__(agent_id, stream_name="socket_sensor_deviceevent", ip=ip, port=port)
#         # TODO: add sensor data type
#         self.cmd = f"sensors,deviceevent"
#         pass
#
#     def get_on_message(self):
#         def on_message(ws, sensor_data):
#             # TODO: convert sensor_data
#             self.stream.send_item({'timestamp': datetime.now(), 'data': sensor_data})
#             print(sensor_data)
#             # self.logger.info()
#
#         return on_message
#
#
# if __name__ == '__main__':
#     ip = '192.168.43.41'
#     default_sensors_agent = DeviceEventSocketSensors(ip=ip)
#     default_sensors_agent.start()
#     # while True:
#     #     cmd = input('> ')
#     #     if cmd == 'q':
#     #         default_sensors_agent.stop()
#     #         break