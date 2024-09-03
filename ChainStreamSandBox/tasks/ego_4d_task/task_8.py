from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import Ego4DData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class VideoTask8(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_ui_stream = None
        self.input_ui_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Activity,
                                modality=Modality_Task_tag.Video)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "first_person_perspective_video_frame",
            "description": "All first person perspective images from the portable camera presenting what I see",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL, PIL.Image"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "analysis_scenario",
                "description": "A series of judgments on whether I am cooking in the kitchen",
                "fields": {
                    "cooking": "An indication of whether I am cooking in the kitchen, bool"
                }
            }
        ])
        self.ego_4d_data = Ego4DData().load_for_indoor_and_outdoor()
        self.agent_example = '''
import chainstream as cs
class AgentExampleForImageTask(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_image_task"):
        super().__init__(agent_id)
        self.first_person_input = cs.get_stream(self, "first_person_perspective_video_frame")
        self.analysis_output = cs.create_stream(self, "analysis_scenario")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def detect_scenario(first_person_data):
            prompt = "Detect whether I am in the kitchen, just tell me y or n."
            res = self.llm.query(cs.llm.make_prompt(prompt,first_person_data["frame"]))
            if res.lower()=="y":
                self.analysis_output.add_item({
                    "cooking": True
                })
            else:
                self.analysis_output.add_item({
                    "cooking": False
                })
        self.first_person_input.for_each(detect_scenario)
        '''

    def init_environment(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'first_person_perspective_video_frame')
        self.output_ui_stream = cs.stream.create_stream(self, 'analysis_scenario')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['analysis_scenario'].append(data)

        self.output_ui_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'first_person_perspective_video_frame')

    def init_output_stream(self, runtime):
        self.output_ui_stream = cs.stream.get_stream(self, 'analysis_scenario')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['analysis_scenario'].append(data)

        self.output_ui_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        processed_results = {'first_person_perspective_video_frame': []}
        for frame in self.ego_4d_data:
            processed_results['first_person_perspective_video_frame'].append(frame)
            self.input_ui_stream.add_item({"frame": frame})
        return processed_results
