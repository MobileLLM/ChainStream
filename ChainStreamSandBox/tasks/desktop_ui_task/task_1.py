from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import DesktopData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)

class ImageTask1(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_ui_stream = None
        self.input_ui_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "desktop_screenshot",
            "description": "All desktop ui images",
            "fields": {
                "image_file": " xxx, PIL",
                "xml_file": " xxx, xml"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "analysis_software",
                "description": "Analyze the software I am using for work right now",
                "fields": {
                    "screenshot_xml": "screenshot xml file, string",
                    "analysis_result": "result of the analysis, string"
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
            prompt = "Analyze the software I am using for work right now,just tell me the name of the software"
            res = self.llm.query(cs.llm.make_prompt(prompt,screenshot['image_file']))
            print("analyze_screenshot", res)
            self.analysis_output.add_item({
                "screenshot_xml": screenshot['xml_file'], 
                "analysis_result": res
            })

        self.screenshot_input.for_each(analyze_screenshot)
        '''

    def init_environment(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'desktop_screenshot')
        self.output_ui_stream = cs.stream.create_stream(self, 'analysis_software')

        self.output_record = []

        def record_output(data):
            print("output task",data)
            self.output_record.append(data)

        self.output_ui_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        processed_results = []
        for screenshot in self.screenshot_data:
            processed_results.append(screenshot)
            self.input_ui_stream.add_item(screenshot)
        return processed_results

    def stop_task(self, runtime):
        pass
