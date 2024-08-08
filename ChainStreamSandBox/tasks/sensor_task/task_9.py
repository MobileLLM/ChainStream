from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class HealthTask2(SingleAgentTaskConfigBase):
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
                "BS": "the blood sugar data from the health sensor, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "remind_check",
                "description": "A list of reminders to go to the hospital for a check when the blood sugar is over "
                               "8.4(every two copies of health sensor data are packaged as a batch after filtering "
                               "the blood sugar which is over 8.4)",
                "fields": {
                    "Blood_sugar": "the blood sugar data from the health sensor, float",
                    "reminder": "High blood sugar！You'd better go to the hospital to check your body!"
                }
            }
        ])

        self.sensor_data = HealthData().get_health_data(sensor_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForSensorTask9(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_health_task_2"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_health")
        self.sensor_output = cs.get_stream(self, "remind_check")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_abnormal(health):
            Blood_sugar = health['BS']
            if Blood_sugar >= 8.4:
                return health

        def reminder(health_list):
            for health in health_list['item_list']:
                Blood_sugar = health['BS']
                self.sensor_output.add_item({
                    "Blood_sugar": str(Blood_sugar)+"mmol/L",
                    "reminder": "High blood sugar！You'd better go to the hospital to check your body!"
                })
        self.sensor_input.for_each(filter_abnormal).batch(by_count=2).for_each(reminder)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_health')
        self.output_sensor_stream = cs.stream.create_stream(self, 'remind_check')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_health = []
        for health in self.sensor_data:
            sent_health.append(health)
            self.input_sensor_stream.add_item(health)
        return sent_health
