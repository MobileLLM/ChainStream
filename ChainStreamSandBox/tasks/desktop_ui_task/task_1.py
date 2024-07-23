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
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "analysis_results",
                "description": "Analysis results from desktop screenshots",
                "fields": {
                    "screenshot_id": "id of the screenshot, string",
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
        self.analysis_output = cs.get_stream(self, "analysis_stuff")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def analyze_screenshot(screenshot):
            prompt = "Analyzing what is the programmer doing"
            res = self.llm.query(cs.llm.make_prompt(prompt,screenshot['image_file']))
            print("analyze_screenshot", res)
            print("output agent", {
                "screenshot_id": screenshot['xml_file'], 
                "analysis_result": res
            })
            self.analysis_output.add_item({
                "screenshot_id": screenshot['xml_file'], 
                "analysis_result": res
            })

        self.screenshot_input.for_each(analyze_screenshot)
        '''

    def init_environment(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'desktop_screenshot')
        self.output_ui_stream = cs.stream.create_stream(self, 'analysis_stuff')

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
