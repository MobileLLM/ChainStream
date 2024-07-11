import chainstream as cs
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.utils.cv.image_utils import draw_face_detection_result
from modelscope.preprocessors.image import LoadImage


class FaceDetectionAgent(cs.agent.Agent):
    """
    A simple agent that performs face detection based on image input
    """

    def __init__(self, agent_id="face_detection_agent"):
        super().__init__(agent_id)
        self.face_detection_pipeline = pipeline(Tasks.face_detection, 'damo/cv_manual_face-detection_mtcnn')
        self._source = cs.get_stream()  # instance of Stream
        self.result_buffer = cs.context.ImageBuffer(max_image_num=1024)

    def start(self):
        def handle_input(image_path):
            img = LoadImage.convert_to_ndarray(image_path)
            result = self.face_detection_pipeline(img)
            img_draw = draw_face_detection_result(image_path, result)
            self.result_buffer.save(img_draw)
        try:
            self._source.for_each(self, handle_input)
            return True
        except Exception as e:
            print("Error in Face Detection Agent: ", e)
            return False

    def pause(self):
        self._source.pause_listener(self)

    def stop(self):
        self._source.remove_listener(self)
