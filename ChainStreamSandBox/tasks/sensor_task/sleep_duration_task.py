from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class HealthTask17(SingleAgentTaskConfigBase):
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
                "Sleep Duration": "The duration the sleeping time, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "sleep_duration_less_than_7_hours",
                "description": "A stream of the sleeping duration if less than 7 hours",
                "fields": {
                    "Sleep Duration": "The duration the sleeping time which is less than 7 hours, float"}
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
        self.output_stream = cs.create_stream(self,"sleep_duration_less_than_7_hours")
        self.llm = get_model("Text")
    def start(self):
        def process_health(health):
            Sleep_Duration = health["Sleep Duration"]
            if Sleep_Duration < 7:  
                self.output_stream.add_item({
                    "Sleep Duration": Sleep_Duration
                    })
        self.input_stream.for_each(process_health)
        '''

    def init_environment(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')
        self.output_health_stream = cs.stream.create_stream(self, 'sleep_duration_less_than_7_hours')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['sleep_duration_less_than_7_hours'].append(data)

        self.output_health_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')

    def init_output_stream(self, runtime):
        self.output_health_stream = cs.stream.get_stream(self, 'sleep_duration_less_than_7_hours')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['sleep_duration_less_than_7_hours'].append(data)

        self.output_health_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        health_dict = {'all_health': []}
        for info in self.health_data:
            self.input_health_stream.add_item(info)
            health_dict['all_health'].append(info)
        return health_dict
