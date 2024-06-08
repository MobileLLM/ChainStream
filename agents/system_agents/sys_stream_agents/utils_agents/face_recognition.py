import chainstream as cs
import numpy as np
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

class FaceRecognitionAgent(cs.agent.Agent):
    """
    A simple agent that performs face recognition based on image input
    """

    def __init__(self, agent_id="face_recognition_agent"):
        super().__init__(agent_id)
        self.face_recognition_pipeline = pipeline(Tasks.face_recognition, model='damo/cv_ir101_facerecognition_cfglint')
        self._source = cs.get_stream()  # instance of Stream
        self.result_buffer = cs.context.TextBuffer(max_text_num=1024)

    def start(self):
        def handle_input(img1_path, img2_path):
            emb1 = self.face_recognition_pipeline(img1_path)[OutputKeys.IMG_EMBEDDING]
            emb2 = self.face_recognition_pipeline(img2_path)[OutputKeys.IMG_EMBEDDING]
            sim = np.dot(emb1[0], emb2[0])
            if sim > 0.8:
                feedback = "This is the same person."
            else:
                feedback = "This is not the same person."
            self.result_buffer.save(sim,feedback)

        try:
            self._source.register_listener(self, handle_input)
            return True
        except Exception as e:
            print("Error in Face Recognition Agent: ", e)
            return False

    def pause(self):
        self._source.pause_listener(self)

    def stop(self):
        self._source.remove_listener(self)

