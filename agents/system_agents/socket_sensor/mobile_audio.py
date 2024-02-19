import chainstream as cs
import threading
from datetime import datetime

from agents.system_agents.socket_sensor.base_socket_sensor import BaseSocketSensors

from pydub import AudioSegment
from io import BytesIO
import pygame

from PIL import Image

from io import BytesIO

class AudioSocketSensors(BaseSocketSensors):
    is_agent = True
    def __init__(self, agent_id='sys_socket_audio_sensors', audio_duration=1, audio_interval=1, ip='192.168.43.41', port=6666):
        super().__init__(agent_id, stream_name="socket_microphone_audio", ip=ip, port=port)
        self.audio_duration = int(audio_duration) * 1000
        self.audio_interval = int(audio_interval) * 1000

        self.cmd = f"audio,{self.audio_duration},{self.audio_interval}"

    def get_on_message(self):
        def on_message(ws, amr_file):
            # print("Received audio file from socket server", len(amr_file))
            amr_file = BytesIO(amr_file)
            amr_audio = AudioSegment.from_file(amr_file, format="amr")

            wav_file = BytesIO()
            amr_audio.export(wav_file, format="wav")

            from pydub.playback import play
            play(amr_audio)

            self.stream.send_item({'timestamp': datetime.now(), 'data': wav_file})

            # self.logger.info()

        return on_message


if __name__ == '__main__':
    ip = '192.168.43.41'
    # default_sensors_agent = VideoSocketSensors(ip=ip)
    default_sensors_agent = AudioSocketSensors(ip=ip)
    # default_sensors_agent = SensorSocketSensors(ip=ip)
    default_sensors_agent.start()
    # while True:
    #     cmd = input('> ')
    #     if cmd == 'q':
    #         default_sensors_agent.stop()
    #         break
