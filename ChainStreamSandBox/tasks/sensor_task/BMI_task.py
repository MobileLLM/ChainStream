from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class HealthTask8(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_health_stream = None
        self.input_health_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Health,
                                modality=Modality_Task_tag.Health_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_health",
            "description": "A stream of health information",
            "fields": {
                "BMI Category": "The checked BMI category, string",
                "RiskLevel": "The risk level of the BMI category, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "Overweight_BMI_category",
                "description": "A stream of the risk level of the 'Overweight' BMI category data in every three seconds",
                "fields": {
                    "risk_level": "The risk level of the checked 'Overweight' BMI category data, string"}
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
        self.output_stream = cs.create_stream(self,"Overweight_BMI_category")
        self.llm = get_model("Text")
    def start(self):
        def process_health(health):
            health_list = health['item_list']
            for health in health_list:
                BMI_Category = health["BMI Category"]
                print(BMI_Category)
                if BMI_Category == "Overweight":  
                    self.output_stream.add_item({
                        "risk_level": health["RiskLevel"]
                        })
        self.input_stream.batch(by_time=3).for_each(process_health)
        '''

    def init_environment(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')
        self.output_health_stream = cs.stream.create_stream(self, 'Overweight_BMI_category')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['Overweight_BMI_category'].append(data)

        self.output_health_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')

    def init_output_stream(self, runtime):
        self.output_health_stream = cs.stream.get_stream(self, 'Overweight_BMI_category')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['Overweight_BMI_category'].append(data)

        self.output_health_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        import time
        data_list = [
            {
                "Gender": "Male",
                "Age": "35",
                "Occupation": "Doctor",
                "Sleep Duration": "6.0",
                "Quality of Sleep": "6.0",
                "Physical Activity Level": "30",
                "Stress Level": "8",
                "BMI Category": "Overweight",
                "Daily Steps": "5000",
                "Sleep Disorder": "None",
                "SystolicBP": "100.0",
                "DiastolicBP": "70.0",
                "BS": "7.0",
                "BodyTemp": "98.0",
                "HeartRate": "60.0",
                "RiskLevel": "low risk"
            },
            {
                "Gender": "Female",
                "Age": "42",
                "Occupation": "Teacher",
                "Sleep Duration": "7.0",
                "Quality of Sleep": "7.0",
                "Physical Activity Level": "25",
                "Stress Level": "6",
                "BMI Category": "Overweight",
                "Daily Steps": "4000",
                "Sleep Disorder": "None",
                "SystolicBP": "110.0",
                "DiastolicBP": "75.0",
                "BS": "6.5",
                "BodyTemp": "98.2",
                "HeartRate": "65.0",
                "RiskLevel": "low risk"
            },
            {
                "Gender": "Male",
                "Age": "50",
                "Occupation": "Engineer",
                "Sleep Duration": "5.5",
                "Quality of Sleep": "5.5",
                "Physical Activity Level": "20",
                "Stress Level": "7",
                "BMI Category": "Overweight",
                "Daily Steps": "4500",
                "Sleep Disorder": "None",
                "SystolicBP": "120.0",
                "DiastolicBP": "80.0",
                "BS": "7.2",
                "BodyTemp": "98.4",
                "HeartRate": "70.0",
                "RiskLevel": "low risk"
            },
            {
                "Gender": "Female",
                "Age": "29",
                "Occupation": "Nurse",
                "Sleep Duration": "8.0",
                "Quality of Sleep": "8.0",
                "Physical Activity Level": "35",
                "Stress Level": "5",
                "BMI Category": "Normal",
                "Daily Steps": "6000",
                "Sleep Disorder": "None",
                "SystolicBP": "95.0",
                "DiastolicBP": "65.0",
                "BS": "6.0",
                "BodyTemp": "98.6",
                "HeartRate": "58.0",
                "RiskLevel": "low risk"
            },
            {
                "Gender": "Male",
                "Age": "45",
                "Occupation": "Accountant",
                "Sleep Duration": "7.0",
                "Quality of Sleep": "7.5",
                "Physical Activity Level": "28",
                "Stress Level": "6",
                "BMI Category": "Normal",
                "Daily Steps": "5500",
                "Sleep Disorder": "None",
                "SystolicBP": "105.0",
                "DiastolicBP": "72.0",
                "BS": "6.8",
                "BodyTemp": "98.1",
                "HeartRate": "62.0",
                "RiskLevel": "low risk"
            }
        ]
        self.health_data.extend(data_list)
        health_dict = {'all_health': []}
        for info in self.health_data:
            self.input_health_stream.add_item(info)
            health_dict['all_health'].append(info)
            time.sleep(1)
        return health_dict
