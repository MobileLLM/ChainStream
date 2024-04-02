import chainstream as cs
from funasr import AutoModel
class Audio_To_Text_Agent(cs.agent.Agent):
    is_agent=True

    def __init__(self,agent_id):
        super().__init__(agent_id)
        self._source=cs.get_stream()
        self.text_buffer=cs.context.TextBuffer(max_text_num=1024)
        self.model=AutoModel(model="paraformer-zh", model_revision="v2.0.4",
                  vad_model="fsmn-vad", vad_model_revision="v2.0.4",
                  punc_model="ct-punc-c", punc_model_revision="v2.0.4",
                  )
    def start(self):
        def handle_wav(wav_file):
            res=self.model.generate(input=wav_file,
                           batch_size_s=300,)
            self.text_buffer.save(res)
        try:
            self._source1.register_listener(self, handle_wav)
        except Exception as e:
            print("Error in Audio to Text agent: ", e)
            return False
        return True
    def start(self):
        def pause(self):
            self._source.pause_listener(self)

        def stop(self):
            self._source.remove_listener(self)
