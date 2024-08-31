from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import DesktopData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class ImageTask1(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_ui_stream = None
        self.input_ui_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Office,
                                modality=Modality_Task_tag.Video)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "desktop_screenshot",
            "description": "All desktop ui images",
            "fields": {
                "image_file": "image file in the Jpeg format processed using PIL, PIL.Image"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "analysis_software",
                "description": "Analysis of a stream of software names for work",
                "fields": {
                    "analysis_result": "A stream of the software name currently used for work."
                }
            }
        ])
        self.screenshot_data = DesktopData().get_random_sample()
        self.agent_example = '''
import chainstream as cs
class AgentExampleForImageTask(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_image_task"):
        super().__init__(agent_id)
        self.screenshot_input = cs.get_stream(self, "desktop_screenshot")
        self.analysis_output = cs.get_stream(self, "analysis_software")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def analyze_screenshot(screenshot):
            prompt = "Analyze the software I am using for work right now, just tell me the name of the software."
            res = self.llm.query(cs.llm.make_prompt(prompt,screenshot['image_file']))
            self.analysis_output.add_item({
                "analysis_result": res
            })

        self.screenshot_input.for_each(analyze_screenshot)
        '''

    def init_environment(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'desktop_screenshot')
        self.output_ui_stream = cs.stream.create_stream(self, 'analysis_software')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['analysis_software'].append(data)

        self.output_ui_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'desktop_screenshot')

    def init_output_stream(self, runtime):
        self.output_ui_stream = cs.stream.get_stream(self, 'analysis_software')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['analysis_software'].append(data)

        self.output_ui_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        processed_results = {'desktop_screenshot': []}
        for screenshot in self.screenshot_data:
            processed_results['desktop_screenshot'].append(screenshot)
            self.input_ui_stream.add_item(screenshot)
        return processed_results
