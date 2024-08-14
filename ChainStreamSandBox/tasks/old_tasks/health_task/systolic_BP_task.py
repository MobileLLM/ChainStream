from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData


class OldHealthTask15(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_health_stream = None
        self.input_health_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_health' and process the values corresponding to the "
            "'SystolicBP' key in the health dictionary: "
            "Add the diastolic blood pressure level to the output stream 'cs_health'."
        )
        self.health_data = HealthData().get_health_data(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_health_agent")
        self.input_stream = cs.get_stream(self,"all_health")
        self.output_stream = cs.get_stream(self,"cs_health")
        self.llm = get_model("Text")
    def start(self):
        def process_health(health):
            SystolicBP = health["SystolicBP"]        
            self.output_stream.add_item(str(SystolicBP))
        self.input_stream.for_each(process_health)
        '''

    def init_environment(self, runtime):
        self.input_health_stream = cs.stream.create_stream(self, 'all_health')
        self.output_health_stream = cs.stream.create_stream(self, 'cs_health')
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

