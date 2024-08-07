from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SpharData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class VideoTask6(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_ui_stream = None
        self.input_ui_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "three_person",
            "description": "All third person perspective images",
            "fields": {
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "detect_person",
                "description": "A list of analysis of whether the secret base has been invaded by person",
                "fields": {
                    "analysis_result": "the detection of whether a person is in the secret base, string"}
            }
        ])
        self.Sphar_data = SpharData().load_for_person_detection()
        self.agent_example = '''
import chainstream as cs
class AgentExampleForImageTask(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_image_task"):
        super().__init__(agent_id)
        self.surveillance_input = cs.get_stream(self, "three_person")
        self.analysis_output = cs.get_stream(self, "detect_person")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def analyze_surveillance(three_person_data):
            prompt = "The following images were captured by a surveillance camera at a secret base.Judge if there is "
            "personnel in the secret base?simply answer y or n"
            res = self.llm.query(cs.llm.make_prompt(prompt,three_person_data))
            self.analysis_output.add_item({
                "analysis_result": res
            })

        self.surveillance_input.for_each(analyze_surveillance)
        '''

    def init_environment(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'three_person')
        self.output_ui_stream = cs.stream.create_stream(self, 'detect_person')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_ui_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        processed_results = []
        for shot in self.Sphar_data:
            processed_results.append({"images": shot})
            self.input_ui_stream.add_item(shot)
        return processed_results

    def stop_task(self, runtime):
        pass
