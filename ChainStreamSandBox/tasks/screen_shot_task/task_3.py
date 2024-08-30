from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import AndroidUIData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class ScreenshotTask3(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_screenshot_stream = None
        self.input_screenshot_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Daily_information,
                                modality=Modality_Task_tag.Video)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_screenshot",
            "description": "A stream of screenshot information",
            "fields": {
                "info": "The details information on the screenshot data, dict with the key 'activity'"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "screenshot_details",
                "description": "The analysis of the screenshot properties on whether the root view is clickable",
                "fields": {
                    "clickable": "The analysis of the screenshot properties on whether the root view is clickable, "
                                 "extracted within the field 'info' -> 'activity' -> 'root' -> 'clickable' structure,"
                                 " bool "
                }
            }
        ])

        self.screenshot_data = AndroidUIData().get_random_data()
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_news_agent")
        self.input_stream = cs.get_stream(self,"all_screenshot")
        self.output_stream = cs.get_stream(self,"screenshot_details")
        self.llm = get_model("image")
    def start(self):
        def process_screenshot(screenshot):
            root_info = screenshot['info']['activity']['root']
            clickable = root_info.get('clickable')
            self.output_stream.add_item({
            "clickable": clickable})
        self.input_stream.for_each(process_screenshot)
        '''

    def init_environment(self, runtime):
        self.input_screenshot_stream = cs.stream.create_stream(self, 'all_screenshot')
        self.output_screenshot_stream = cs.stream.create_stream(self, 'screenshot_details')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['screenshot_details'].append(data)

        self.output_screenshot_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_screenshot_stream = cs.stream.create_stream(self, 'all_screenshot')

    def init_output_stream(self, runtime):
        self.output_screenshot_stream = cs.stream.get_stream(self, 'screenshot_details')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['screenshot_details'].append(data)

        self.output_screenshot_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        screenshot_dict = {'all_screenshot': []}
        for image in self.screenshot_data:
            self.input_screenshot_stream.add_item(image)
            screenshot_dict['all_screenshot'].append(image)
        return screenshot_dict
