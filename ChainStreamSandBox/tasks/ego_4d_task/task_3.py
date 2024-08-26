from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import Ego4DData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class VideoTask3(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_ui_stream = None
        self.input_ui_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Activity,
                                modality=Modality_Task_tag.Video)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "first_person_perspective_data",
            "description": "All first person perspective images",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "analysis_topic",
                "description": "A sequence that automatically records meeting topics",
                "fields": {
                    "analysis_result": "the topic of the meeting, string"
                }
            }
        ])
        self.ego_4d_data = Ego4DData().load_for_person_detection()
        self.agent_example = '''
import chainstream as cs
class AgentExampleForImageTask(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_image_task"):
        super().__init__(agent_id)
        self.first_person_input = cs.get_stream(self, "first_person_perspective_data")
        self.analysis_output = cs.get_stream(self, "analysis_topic")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def detect_scenario(first_person_data):
            prompt = "Detect whether I am in a meeting,just tell me y or n."
            res = self.llm.query(cs.llm.make_prompt(prompt,first_person_data["frame"]))
            if res.lower()=="y":
                return first_person_data
        def analysis_topic(first_person_data):
            prompt = "Tell me what topic we are talking about based on the image."
            res = self.llm.query(cs.llm.make_prompt(prompt,first_person_data["frame"]))
            self.analysis_output.add_item({
                "analysis_result": res
            })
        self.first_person_input.for_each(detect_scenario).for_each(analysis_topic)
        '''

    def init_environment(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'first_person_perspective_data')
        self.output_ui_stream = cs.stream.create_stream(self, 'analysis_topic')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['analysis_topic'].append(data)

        self.output_ui_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        processed_results = {'first_person_perspective_data': []}
        for frame in self.ego_4d_data:
            processed_results['first_person_perspective_data'].append(frame)
            self.input_ui_stream.add_item({"frame": frame})
        return processed_results

