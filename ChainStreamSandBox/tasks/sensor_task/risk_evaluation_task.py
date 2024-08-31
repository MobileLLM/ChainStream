from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class HealthTask15(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_health_stream = None
        self.input_health_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Health,
                                modality=Modality_Task_tag.Health_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_health",
            "description": "A stream of health information",
            "fields": {
                'SystolicBP': "The systolic blood pressure detected, float",
                'DiastolicBP': "The diastolic blood pressure detected, float",
                'BS': "The blood sugar level detected, float",
                'BodyTemp': "The body temperature detected, float",
                'HeartRate': "The heart rate detected, int"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "risk_level",
                "description": "A stream of the analysis of the risk level of the person based on the health data "
                               "chosen from 'high risk', 'low risk', or 'mid risk'",
                "fields": {
                    "risk_level": "The evaluation of the risk level of the specific person chosen from 'high risk', "
                                  "'low risk', or 'mid risk', string"}
            }
        ])
        self.health_data = HealthData().get_health_data(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_health_agent")
        self.input_stream = cs.get_stream(self,"all_health")
        self.output_stream = cs.get_stream(self,"risk_level")
        self.llm = get_model("Text")
    def start(self):
        def process_health(health):
            health_text = f"SystolicBP: {health['SystolicBP']}, DiastolicBP: {health['DiastolicBP']}, BS: {health['BS']}, BodyTemp: {health['BodyTemp']}, HeartRate: {health['HeartRate']}"
            prompt = "Based on the following health indicators, determine the person's health risk level. Categorize into 'high risk', 'low risk', or 'mid risk'. Just give me the choice."
            response = self.llm.query(cs.llm.make_prompt(prompt,health_text))
            self.output_stream.add_item({
                "risk_level": response
                })
        self.input_stream.for_each(process_health)
        '''

    def init_environment(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')
        self.output_health_stream = cs.stream.create_stream(self, 'risk_level')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['risk_level'].append(data)

        self.output_health_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')

    def init_output_stream(self, runtime):
        self.output_health_stream = cs.stream.get_stream(self, 'risk_level')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['risk_level'].append(data)

        self.output_health_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        health_dict = {'all_health': []}
        for info in self.health_data:
            self.input_health_stream.add_item(info)
            health_dict['all_health'].append(info)
        return health_dict
