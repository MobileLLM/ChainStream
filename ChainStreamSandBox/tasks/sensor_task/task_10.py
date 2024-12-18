from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class HealthTask3(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=40):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard, domain=Domain_Task_tag.Health,
                                modality=Modality_Task_tag.Health_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_health",
            "description": "All health information",
            "fields": {
                "BMI Category": "the BMI category of the body check, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "remind_exercise",
                "description": "A stream of reminders to take some exercise when the BMI is 'Overweight' or 'Obese',"
                               "with every two copies of health sensor data packaged as a batch after filtering the "
                               "BMI which is 'Overweight' or 'Obese'",
                "fields": {
                    "BMI Category": "the BMI category of the body check, string",
                    "reminder": "An auto reminder, string = Exercise yourself!"
                }
            }
        ])

        self.sensor_data = HealthData().get_health_data(sensor_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForSensorTask9(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_health_task_3"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_health")
        self.sensor_output = cs.create_stream(self, "remind_exercise")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_abnormal(health):
            BMI = health['BMI Category']
            if BMI == "Overweight" or BMI == "Obese":
                print(BMI)
                return health
            else:
                return None
        def reminder(health_list):
            for health in health_list['item_list']:
                BMI = health['BMI Category']
                self.sensor_output.add_item({
                    "BMI Category": BMI,
                    "reminder": "Exercise yourself!"
                })
        self.sensor_input.for_each(filter_abnormal).batch(by_count=2).for_each(reminder)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_health')
        self.output_sensor_stream = cs.stream.create_stream(self, 'remind_exercise')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['remind_exercise'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_health')

    def init_output_stream(self, runtime):
        self.output_sensor_stream = cs.stream.get_stream(self, 'remind_exercise')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['remind_exercise'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_health = {'all_health': []}
        for health in self.sensor_data:
            sent_health['all_health'].append(health)
            self.input_sensor_stream.add_item(health)
        return sent_health
