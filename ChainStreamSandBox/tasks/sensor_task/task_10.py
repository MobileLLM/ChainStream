from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class HealthTask3(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=40):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None
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
                "description": "A list of reminders to take some exercise when the BMI is 'Overweight' or 'Obese'",
                "fields": {
                    "BMI": "the BMI category of the body check,string",
                    "reminder": "Exercise yourself!"
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
        self.sensor_output = cs.get_stream(self, "remind_exercise")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_abnormal(health):
            BMI = health['BMI Category']
            if BMI == "Overweight" or "Obese":
                return health
        def reminder(health_list):
            for health in health_list['item_list']:
                BMI = health['BMI Category']
                self.sensor_output.add_item({
                    "BMI": BMI,
                    "reminder": "Exercise yourself!"
                })
        self.sensor_input.for_each(filter_abnormal).batch(by_count=2).for_each(reminder)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_health')
        self.output_sensor_stream = cs.stream.create_stream(self, 'remind_exercise')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.sensor_data:
            sent_messages.append(message)
            self.input_sensor_stream.add_item(message)
        return sent_messages
