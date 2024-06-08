from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import chainstream as cs

class ImageSegmentationAgent(cs.agent.Agent):
    """
    A simple agent that performs image segmentation based on text input
    """

    is_agent = True

    def __init__(self, agent_id="image_segmentation_agent",target=None):
        super().__init__(agent_id)
        self.model_id = 'damo/cv_vitl16_segmentation_text-driven-seg'
        self._source1 = cs.get_stream()  # instance of Stream
        self.detection_buffer = cs.context.ImageBuffer(max_text_num=1024)
        self.target=target

    def start(self):
        def handle_input(data):#data包含图像地址和分割对象的信息
            test_input = {
                'image': data['image'],
                'text': data['text'],
            }
            segmentation_pipeline = pipeline(Tasks.text_driven_segmentation, model=self.model_id)
            result = segmentation_pipeline(test_input)
            # Save the segmentation result (segmentation mask) as an image
            self.detection_buffer.save(result[OutputKeys.MASKS])
        try:
            self._source1.register_listener(self, handle_input)
            return True
        except Exception as e:
            print("Error in Image Segmentation Agent: ", e)
            return False

    def pause(self):
        cs.get_stream().pause_listener(self)

    def stop(self):
        cs.get_stream().remove_listener(self)
