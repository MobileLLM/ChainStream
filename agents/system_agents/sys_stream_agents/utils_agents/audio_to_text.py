import chainstream as cs
#from funasr import AutoModel
from faster_whisper import WhisperModel
import numpy as np
import pyaudio
import threading
import wave
import datetime

class Audio_To_Text_Agent(cs.agent.Agent):
    is_agent=True

    def __init__(self,agent_id):
        super().__init__(agent_id)
        self._source=cs.get_stream('audio_data')
        self.text_buffer=cs.context.TextBuffer(max_text_num=1024)
        self.model=WhisperModel("base", device="cpu", compute_type="int8")
    def start(self):
        def handle_wav(item):
            #data = np.frombuffer(buffer=item['data'], dtype=np.float32)
            segments,info=self.model.transcribe(item['data'],beam_size=5,vad_filter=True,vad_parameters=dict(min_silence_duration_ms=1000),)
            for segment in segments:
                    self.text_buffer.save(segment.text)
                    print(f'text:{segment.text}')
        try:
            self._source.register_listener(self, handle_wav)
        except Exception as e:
            print("Error in Audio to Text agent: ", e)
            return False
        return True

    def pause(self):
        self._source.pause_listener(self)

    def stop(self):
        self._source.remove_listener(self)
def record_from_microphone():
    CHANNELS = 1
    RATE = 16000
    chunk_size = 60 * 10 / 10
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=8000)
    source=cs.get_stream("audio_data")
    while True:
        data = stream.read(3*16000,exception_on_overflow = False)
        data=np.frombuffer(buffer=data, dtype=np.float32)
        source.add_item({'timestamp': datetime.datetime.now(), 'data':data})


if __name__ == '__main__':
    source=cs.create_stream('audio_data')
    thread = threading.Thread(target=record_from_microphone)
    thread.start()
    agent=Audio_To_Text_Agent('audio_agent')
    agent.start()


