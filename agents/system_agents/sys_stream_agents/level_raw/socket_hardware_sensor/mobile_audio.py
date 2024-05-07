from datetime import datetime
import chainstream as cs
from agents.system_agents.sys_stream_agents.level_raw.socket_sensor.base_socket_sensor import BaseSocketSensors

from pydub import AudioSegment

from io import BytesIO


class AudioSocketSensors(cs.agent.Agent):
    is_agent = True

    def __init__(self, agent_id='sys_socket_audio_sensors', audio_duration=1, audio_interval=1.5, ip='192.168.20.134',
                 port=6666):
        super().__init__(agent_id)
        self.audio_duration = int(audio_duration) * 1000
        self.audio_interval = int(audio_interval) * 1000
        self.cmd = f"audio,{self.audio_duration},{self.audio_interval}"
        self.stream = cs.stream.create_stream("socket_audio")

        self.base_socket = BaseSocketSensors(ip=ip, port=port, cmd=self.cmd)

    def start(self):
        def on_message(ws, amr_file):
            # print(datetime.now(), ": Received audio file from socket server", len(amr_file))
            amr_file = BytesIO(amr_file)
            amr_audio = AudioSegment.from_file(amr_file, format="amr")

            wav_file = BytesIO()
            amr_audio.export(wav_file, format="wav")

            # from pydub.playback import play
            # play(amr_audio)

            # try:
            #     from chainstream.llm.python_base_openai import AudioGPTModel
            #     tmp = AudioGPTModel()
            #     prompt = "请概括这里说了什么"
            #     print(tmp.query(prompt, wav_file))
            # except Exception as e:
            #     print(e)

            self.stream.send_item({'timestamp': datetime.now(), 'data': wav_file})
        self.base_socket.start(on_message)

    def stop(self):
        self.base_socket.stop()



if __name__ == '__main__':
    ip = '192.168.20.134'
    # default_sensors_agent = VideoSocketSensors(ip=ip)
    default_sensors_agent = AudioSocketSensors(ip=ip)
    # default_sensors_agent = SensorSocketSensors(ip=ip)
    default_sensors_agent.start()
    # while True:
    #     cmd = input('> ')
    #     if cmd == 'q':
    #         default_sensors_agent.stop()
    #         break
