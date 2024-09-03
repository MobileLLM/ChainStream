from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class HealthTask5(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=20):
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
                "Occupation": "The occupation information of the patients, string",
                "Sleep Duration": "the average sleep duration information per day of the patients, float",
                "Age": "the age information of the patients, int"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "health_advice_for_engineers",
                "description": "A stream of the reasonable advice for the company's engineer according to their ages "
                               "and sleeping time information, with every two copies of health sensor data packaged "
                               "as a batch after filtering the occupation which is 'Engineer' in the 'Occupation' "
                               "field.",
                "fields": {
                    "Age": "the age of the engineer, int",
                    "Sleep Duration": "the average sleep duration of the engineer, float",
                    "advice": "the reasonable advice for every engineer, string"
                }
            }
        ])

        self.sensor_data = HealthData().get_health_data(sensor_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForSensorTask10(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_health_task_5"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_health")
        self.sensor_output = cs.create_stream(self, "health_advice_for_engineers")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_engineer(health):
            occupation = health['Occupation']
            if occupation == "Engineer":
                return health

        def reminder(health_list):
            for health in health_list['item_list']:
                sleep_time = health['Sleep Duration']
                age = health['Age']
                prompt = "These are the ages and the sleep duration of all the software engineers in our company.Please provide personalized health advice for each engineer."
                res = self.llm.query(cs.llm.make_prompt(f"Age: {age}, Sleep Duration: {sleep_time} hours", prompt))
                self.sensor_output.add_item({
                    "Age": age,
                    "Sleep Duration": str(sleep_time),
                    "advice": res
                })

        self.sensor_input.for_each(filter_engineer).batch(by_count=2).for_each(reminder)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_health')
        self.output_sensor_stream = cs.stream.create_stream(self, 'health_advice_for_engineers')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['health_advice_for_engineers'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_health')

    def init_output_stream(self, runtime):
        self.output_sensor_stream = cs.stream.get_stream(self, 'health_advice_for_engineers')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['health_advice_for_engineers'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_health = {'all_health': []}
        for health in self.sensor_data:
            sent_health['all_health'].append(health)
            self.input_sensor_stream.add_item(health)
        return sent_health
