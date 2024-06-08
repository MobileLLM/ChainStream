from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import chainstream as cs

class OCRAgent(cs.agent.Agent):
    """
    A simple agent that performs OCR recognition on images or URLs
    """

    is_agent = True

    def __init__(self, agent_id="ocr_agent"):
        super().__init__(agent_id)
        self.model_id = 'damo/cv_convnextTiny_ocr-recognition-general_damo'
        self._source = cs.get_stream()  # instance of Stream
        self.result_buffer = cs.context.TextBuffer(max_text_num=1024)

    def start(self):
        def handle_input(url):
            ocr_pipeline = pipeline(Tasks.ocr_recognition, model=self.model_id)
            result = ocr_pipeline(url)
            self.result_buffer.save(result)

        try:
            self._source.register_listener(self, handle_input)
            return True
        except Exception as e:
            print("Error in OCR Agent: ", e)
            return False

    def pause(self):
        self._source.pause_listener(self)

    def stop(self):
        self._source.remove_listener(self)
