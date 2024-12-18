from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import SpharData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class VideoTask11(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_three_person_stream = None
        self.input_three_person_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Activity,
                                modality=Modality_Task_tag.Video)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "third_person_perspective_video_frame",
            "description": "All third person perspective images from the surveillance camera in the school",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL, PIL.Image"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "analysis_violence",
                "description": "A stream of analysis of whether violence has occurred in the surveillance video",
                "fields": {
                    "analysis_result": "analyze whether there are any violent incidents, bool = True or False"}
            }
        ])
        self.Sphar_data = SpharData().load_for_violence()
        self.agent_example = '''
import chainstream as cs
class AgentExampleForImageTask(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_image_task"):
        super().__init__(agent_id)
        self.surveillance_input = cs.get_stream(self, "third_person_perspective_video_frame")
        self.analysis_output = cs.create_stream(self, "analysis_violence")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def analyze_surveillance(third_person_data):
            prompt = "Determine whether violence has occurred in the surveillance video?Simply answer y or n."
            res = self.llm.query(cs.llm.make_prompt(prompt,third_person_data["frame"]))
            if res.lower() == "y":
                self.analysis_output.add_item({
                    "analysis_result": True
                })
            else:
                self.analysis_output.add_item({
                    "analysis_result": False
                })

        self.surveillance_input.for_each(analyze_surveillance)
        '''

    def init_environment(self, runtime):
        self.input_three_person_stream = cs.stream.create_stream(self, 'third_person_perspective_video_frame')
        self.output_three_person_stream = cs.stream.create_stream(self, 'analysis_violence')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['analysis_violence'].append(data)

        self.output_three_person_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_three_person_stream = cs.stream.create_stream(self, 'third_person_perspective_video_frame')

    def init_output_stream(self, runtime):
        self.output_three_person_stream = cs.stream.get_stream(self, 'analysis_violence')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['analysis_violence'].append(data)

        self.output_three_person_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        processed_results = {'third_person_perspective_video_frame': []}
        for frame in self.Sphar_data:
            processed_results['third_person_perspective_video_frame'].append(frame)
            self.input_three_person_stream.add_item({"frame": frame})
        return processed_results
