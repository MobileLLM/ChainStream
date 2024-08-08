from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import Ego4DData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class VideoTask2(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_ui_stream = None
        self.input_ui_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "one_person_perspective_data",
            "description": "All one person perspective images",
            "fields": {
                "images": "image file in the Jpeg format processed using PIL,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "analysis_kitchen_risk",
                "description": "A sequence that alerts that detect whether there is fire risk in the kitchen",
                "fields": {
                    "analysis_result": "the alert that detect whether there is fire risk in the kitchen, string"}
            }
        ])
        self.ego_4d_data = Ego4DData().load_for_indoor_and_outdoor()
        self.agent_example = '''
import chainstream as cs
class AgentExampleForImageTask(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_image_task"):
        super().__init__(agent_id)
        self.ego_input = cs.get_stream(self, "one_person_perspective_data")
        self.analysis_output = cs.get_stream(self, "analysis_kitchen_risk")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def analysis_risk(ego_data):
            prompt = "Detect whether I am in kitchen,just tell me y or n.If the answer if y,tell me whether there is "
            "potential risk of fire in the kitchen"
            res = self.llm.query(cs.llm.make_prompt(prompt,ego_data))
            self.analysis_output.add_item({
                "analysis_result": res
            })
        self.ego_input.for_each(analysis_risk)
        '''

    def init_environment(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'one_person_perspective_data')
        self.output_ui_stream = cs.stream.create_stream(self, 'analysis_kitchen_risk')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_ui_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        processed_results = []
        for frame in self.ego_4d_data:
            processed_results.append({"images": frame})
            self.input_ui_stream.add_item(frame)
        return processed_results

    def stop_task(self, runtime):
        pass
