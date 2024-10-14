from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class HealthTask10(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_health_stream = None
        self.input_health_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Activity,
                                modality=Modality_Task_tag.Health_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_health",
            "description": "A stream of health information",
            "fields": {
                "Daily Steps": "The steps calculated daily, int"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "daily_steps_more_than_5k",
                "description": "A stream of the steps daily which is less than 5000",
                "fields": {
                    "daily_steps_more_than_5k": "The steps calculated daily which is more than 5000, int"}
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
        self.output_stream = cs.create_stream(self,"daily_steps_more_than_5k")
        self.llm = get_model("Text")
    def start(self):
        def process_health(health):
            Daily_Steps = health["Daily Steps"]
            if Daily_Steps > 5000:  
                self.output_stream.add_item({
                    "daily_steps_more_than_5k": Daily_Steps
                    })
        self.input_stream.for_each(process_health)
        '''

    def init_environment(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')
        self.output_health_stream = cs.stream.create_stream(self, 'daily_steps_more_than_5k')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['daily_steps_more_than_5k'].append(data)

        self.output_health_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')

    def init_output_stream(self, runtime):
        self.output_health_stream = cs.stream.get_stream(self, 'daily_steps_more_than_5k')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['daily_steps_more_than_5k'].append(data)

        self.output_health_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        health_dict = {'all_health': []}
        for info in self.health_data:
            self.input_health_stream.add_item(info)
            health_dict['all_health'].append(info)
        return health_dict
