from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SpharData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class VideoTask5(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_ui_stream = None
        self.input_ui_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Activity,
                                scene=Scene_Task_tag.Shop, modality=Modality_Task_tag.Video)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "third_person",
            "description": "All third person perspective images",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL, PIL.Image"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "analysis_violence",
                "description": "A list of analysis of whether violence has occurred in the surveillance video",
                "fields": {
                    "analysis_result": "the analysis of the violence incident happened, string"}
            }
        ])
        self.Sphar_data = SpharData().load_for_violence()
        self.agent_example = '''
import chainstream as cs
class AgentExampleForImageTask(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_image_task"):
        super().__init__(agent_id)
        self.surveillance_input = cs.get_stream(self, "third_person")
        self.analysis_output = cs.get_stream(self, "analysis_violence")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def analyze_surveillance(third_person_data):
            prompt = "Determine whether violence has occurred in the surveillance video?simply answer y or n.If the answer is y,Choose from several tags:['fighting','shooting','quarrel','others']"
            res = self.llm.query(cs.llm.make_prompt(prompt,third_person_data["frame"]))
            self.analysis_output.add_item({
                "analysis_result": res
            })

        self.surveillance_input.for_each(analyze_surveillance)
        '''

    def init_environment(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'third_person')
        self.output_ui_stream = cs.stream.create_stream(self, 'analysis_violence')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['analysis_violence'].append(data)

        self.output_ui_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        processed_results = {'third_person': []}
        for frame in self.Sphar_data:
            processed_results['third_person'].append(frame)
            self.input_ui_stream.add_item({"frame": frame})
        return processed_results

