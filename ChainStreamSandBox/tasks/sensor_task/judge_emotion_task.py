from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class HealthTask13(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_health_stream = None
        self.input_health_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Health,
                                modality=Modality_Task_tag.Health_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_health",
            "description": "A series of health information",
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
                "stream_id": "emotion_estimation",
                "description": "A series of the analysis of the mood chosen from ['Happy', 'Sad', 'Angry', 'Excited', "
                               "'Anxious', 'Relaxed', 'Not sure'] based on the health data",
                "fields": {
                    "mood_estimation": "The estimation of the mood chosen from['Happy', 'Sad', 'Angry', 'Excited', "
                                       "'Anxious', 'Relaxed', 'Not sure'], string"}
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
        self.output_stream = cs.get_stream(self,"emotion_estimation")
        self.llm = get_model("Text")
    def start(self):
        def process_health(health):
            health_text = f"SystolicBP: {health['SystolicBP']}, DiastolicBP: {health['DiastolicBP']}, BS: {health['BS']}, BodyTemp: {health['BodyTemp']}, HeartRate: {health['HeartRate']}"
            prompt = f"Based on the following health indicators: {health_text}, judge the person's current mood chosen from ['Happy', 'Sad', 'Angry', 'Excited', 'Anxious', 'Relaxed', 'Not sure']. Please only give me the choice."
            response = self.llm.query(cs.llm.make_prompt(prompt))
            self.output_stream.add_item({
                "mood_estimation": response
                })
        self.input_stream.for_each(process_health)
        '''

    def init_environment(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')
        self.output_health_stream = cs.stream.create_stream(self, 'emotion_estimation')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['emotion_estimation'].append(data)

        self.output_health_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')

    def init_output_stream(self, runtime):
        self.output_health_stream = cs.stream.get_stream(self, 'emotion_estimation')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['emotion_estimation'].append(data)

        self.output_health_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        health_dict = {'all_health': []}
        for info in self.health_data:
            self.input_health_stream.add_item(info)
            health_dict['all_health'].append(info)
        return health_dict
