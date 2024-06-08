from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import chainstream as cs
import numpy as np

class EmotionRecognitionAgent(cs.agent.Agent):
    """
    A simple agent that performs facial expression recognition based on image input
    """

    is_agent = True

    def __init__(self, agent_id="emotion_recognition_agent"):
        super().__init__(agent_id)
        self.model_id = 'damo/cv_vgg19_facial-expression-recognition_fer'
        self._source = cs.get_stream()  # instance of Stream
        self.result_buffer = cs.context.TextBuffer(max_text_num=1024)
    def start(self):
        def handle_input(image_url):
            facial_expression_pipeline = pipeline(Tasks.facial_expression_recognition, model=self.model_id)
            result = facial_expression_pipeline(image_url)
            label_idx = np.array(result['scores']).argmax()
            label = result['labels'][label_idx]
            self.result_buffer.save(label)

        try:
            self._source.register_listener(self, handle_input)
            return True
        except Exception as e:
            print("Error in Emotion Recognition Agent: ", e)
            return False

    def pause(self):

        self._source.pause_listener(self)

    def stop(self):

        self._source.remove_listener(self)

