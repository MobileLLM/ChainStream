from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class HealthTask2(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=40, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None

        self.eos_gap = eos_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "health_stream2",
                "description": "Remind me to hospital when my blood sugar is above normal",
                "fields": {
                    "Blood_sugar":"xxx,string",
                    "Reminder":"High blood sugar！You'd better go to the hospital to check your body!"
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
        self.sensor_output = cs.get_stream(self, "remind_medicine")
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
                    "remind": "High blood sugar！You'd better go to the hospital to check your body!"
                })
        self.sensor_input.for_each(filter_abnormal).batch(by_count=2).for_each(reminder)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_health')
        self.output_sensor_stream = cs.stream.create_stream(self, 'remind_medicine')

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






