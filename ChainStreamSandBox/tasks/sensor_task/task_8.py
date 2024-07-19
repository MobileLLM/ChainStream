from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class HealthTask1(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=40, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None

        self.eos_gap = eos_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "health_stream1",
                "description": "Remind me to take some medicine when my blood pressure is above normal",
                "fields": {
                    "SystolicBP":"xxx,string",
                    "DiastolicBP":"xxx,string",
                    "Reminder":"Remember to take your medicine!"
                }
            }
        ])

        self.sensor_data = HealthData().get_health_data(sensor_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForSensorTask8(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_health_task_1"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_health")
        self.sensor_output = cs.get_stream(self, "remind_medicine")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_abnormal(health):
            SystolicBP = health['SystolicBP']
            DiastolicBP = health['DiastolicBP']
            if SystolicBP >= 120 and DiastolicBP >= 70:
                return health

        def reminder(health_list):
            for health in health_list['item_list']:
                SystolicBP = health['SystolicBP']
                DiastolicBP = health['DiastolicBP']
                self.sensor_output.add_item({
                    "SystolicBP": str(SystolicBP) + "mmHg",
                    "DiastolicBP": str(DiastolicBP) + "mmHg",
                    "remind": "Remember to take your medicine!"
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






