from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
from modelscope.utils.cv.image_utils import show_video_tracking_result
import chainstream as cs

class VideoTrackingAgent(cs.agent.Agent):
    """
    A simple agent that performs object tracking in a video stream
    """

    is_agent = True

    def __init__(self, agent_id="video_tracking_agent", init_bbox=None):
        super().__init__(agent_id)
        self.model_id = 'damo/cv_vitb_video-single-object-tracking_ostrack'
        self.init_bbox = init_bbox
        self._source1 = cs.get_stream()  # instance of Stream
        self.detection_buffer = cs.context.AudioBuffer(max_text_num=1024)
        self.init_bbox=init_bbox#第一帧object

    def track_object(self, frame):#frame为视频地址
        video_single_object_tracking = pipeline(Tasks.video_single_object_tracking, model=self.model_id)
        result = video_single_object_tracking((frame, self.init_bbox))
        return result

    def start(self):
        def handle_new_frame(frame):
            result = self.track_object(frame)
            self.detection_buffer.save(show_video_tracking_result(frame, result[OutputKeys.BOXES], "./tracking_result.avi"))
        try:
            self._source1.register_listener(self, handle_new_frame)
            return True
        except Exception as e:
            print("Error in Video Tracking Agent: ", e)
            return False

    def pause(self):
        cs.get_stream().pause_listener(self)

    def stop(self):
        cs.get_stream().remove_listener(self)
