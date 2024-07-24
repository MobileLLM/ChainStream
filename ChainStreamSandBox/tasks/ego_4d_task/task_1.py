from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import Ego4DData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)

class VideoTask1(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_ego_stream = None
        self.input_ego_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "ego_4D",
            "description": "All first person perspective images",
            "fields": {
                # "Occupation": " xxx, string",
                # "Sleep Duration": " xxx, float",
                # "Age": " xxx, int"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "analysis_actions",
                "description": "Detect what I am doing right now",
                "fields": {
                    "analysis_result": " result xxx, string"}
            }
        ])
        self.ego_4d_data = Ego4DData().load_for_action()
        self.agent_example = '''
import chainstream as cs
class AgentExampleForImageTask(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_image_task"):
        super().__init__(agent_id)
        self.screenshot_input = cs.get_stream(self, "ego_4D")
        self.analysis_output = cs.get_stream(self, "analysis_actions")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def analyze_screenshot(ego_data):
            print(type(ego_data))
            prompt = "Detect what am I doing now?Choose from several tags:['driving','jumping roll','walking','swimming','climbing','skating'],and just tell me what kind"
            res = self.llm.query(cs.llm.make_prompt(prompt,ego_data))
            print("analyze_screenshot", res)
            self.analysis_output.add_item({
                "analysis_result": res
            })

        self.screenshot_input.for_each(analyze_screenshot)
        '''

    def init_environment(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'ego_4D')
        self.output_ui_stream = cs.stream.create_stream(self, 'analysis_actions')

        self.output_record = []

        def record_output(data):
            print("output task",data)
            self.output_record.append(data)

        self.output_ui_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        processed_results = []
        for screenshot in self.ego_4d_data:
            processed_results.append(screenshot)
            self.input_ui_stream.add_item(screenshot)
        return processed_results

    def stop_task(self, runtime):
        pass
