from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import chainstream as cs
import numpy as np

class ActionRecognitionAgent(cs.agent.Agent):
    """
    A simple agent that performs action sensing recognition based on image input
    """

    is_agent = True

    def __init__(self, agent_id="action_recognition_agent"):
        super().__init__(agent_id)
        self.model_id = 'damo/cv_ResNetC3D_action-detection_detection2d'
        self._source = cs.get_stream()  # instance of Stream
        self.result_buffer = cs.context.TextBuffer(max_text_num=1024)
    def start(self):
        def handle_input(image_url):
            action_detection_pipeline = pipeline(Tasks.action_detection, model=self.model_id)
            result = action_detection_pipeline(image_url)
            label_idx = np.array(result['scores']).argmax()
            label = result['labels'][label_idx]
            self.result_buffer.save(label)

        try:
            self._source.register_listener(self, handle_input)
            return True
        except Exception as e:
            print("Error in Action Recognition Agent: ", e)
            return False

    def pause(self):

        self._source.pause_listener(self)

    def stop(self):

        self._source.remove_listener(self)

