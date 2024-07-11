from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import chainstream as cs

class GestureRecognitionAgent(cs.agent.Agent):
    """
    A simple agent that performs gesture recognition based on image input
    """

    is_agent = True

    def __init__(self, agent_id="gesture_recognition_agent"):
        super().__init__(agent_id)
        self.model_id = 'damo/cv_mobileface_hand-static'
        self._source = cs.get_stream()  # instance of Stream
        self.result_buffer = cs.context.TextBuffer(max_text_num=1024)

    def start(self):
        def handle_input(image_path):
            gesture_recognition_pipeline = pipeline(Tasks.hand_static, model=self.model_id)
            result_status = gesture_recognition_pipeline(image_path)
            result = result_status[OutputKeys.OUTPUT]
            self.result_buffer.save(result)

        try:
            self._source.for_each(self, handle_input)
            return True
        except Exception as e:
            print("Error in Gesture Recognition Agent: ", e)
            return False

    def pause(self):
        self._source.pause_listener(self)

    def stop(self):
        self._source.remove_listener(self)
