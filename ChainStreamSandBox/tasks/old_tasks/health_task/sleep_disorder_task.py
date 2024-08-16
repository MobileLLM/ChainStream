from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData
from AgentGenerator.io_model import StreamListDescription


class OldHealthTask11(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_health_stream = None
        self.input_health_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_health",
            "description": "A list of health information",
            "fields": {
                "Physical Activity Level": "The level of the physical activity,int",
                "BS": "The blood sugar check,float",
                "BMI Category": "The checked BMI category,string",
                "BodyTemp": "The checked body temperature,float",
                "Daily Steps": "The steps calculated daily,int",
                "DiastolicBP": "The diastolic blood pressure detected,float",
                "SystolicBP": "The systolic blood pressure detected,float",
                "HeartRate": "The heart rate detected,int",
                "Sleep Disorder": "The type of the sleep disorder,string",
                "Sleep Duration": "The duration the sleeping time,float",
                "Quality of Sleep": "The evaluation of the quality of sleep,int",
                "Stress Level": "The level of stress detected,int"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "sleep_disorder_evaluation",
                "description": "A list of the evaluation on the sleep disorder problem",
                "fields": {
                    "sleep_disorder_type": "The type of the sleep disorder,string"}
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
        self.output_stream = cs.get_stream(self,"sleep_disorder_evaluation")
        self.llm = get_model("Text")
    def start(self):
        def process_health(health):
            Sleep_Disorder = health["Sleep Disorder"]        
            self.output_stream.add_item({
                "sleep_disorder_type":Sleep_Disorder
                })
        self.input_stream.for_each(process_health)
        '''

    def init_environment(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')
        self.output_health_stream = cs.stream.create_stream(self, 'sleep_disorder_evaluation')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_health_stream.for_each(record_output)

    def start_task(self, runtime):
        health_list = []
        for info in self.health_data:
            self.input_health_stream.add_item(info)
            health_list.append(info)
        return health_list
