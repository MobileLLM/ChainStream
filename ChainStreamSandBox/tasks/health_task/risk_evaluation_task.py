from ..task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import HealthData


class RiskEvaluationConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_health_stream = None
        self.input_health_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_health' and judge the risk level of the person according to the "
            "data.Categorize the risk level into 'high risk', 'low risk', or 'mid risk' using LLM.Add the health text "
            "and the response to the output stream 'cs_health'. "
        )
        self.health_data = HealthData().get_health_data(10)
        self.agent_example = '''
        import chainstream as cs
        from chainstream.llm import get_model
        class testAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("test_health_agent")
                self.input_stream = cs.get_stream("all_health")
                self.output_stream = cs.get_stream("cs_health")
                self.llm = get_model(["text"])
            def start(self):
                def process_health(health):
                    health_text = health
                    prompt = "Based on the following health indicators, determine the person's health risk level. Categorize into 'high risk', 'low risk', or 'mid risk'."
                    prompt = [
                        {
                            "role": "user",
                            "content": prompt+health_text
                        }
                    ]
                    response = self.llm.query(prompt)
                    print(health_text+" : "+response)
                    self.output_stream.add_item(health_text+" : "+response)
                self.input_stream.register_listener(self, process_health)
        
            def stop(self):
                self.input_stream.unregister_listener(self)
        '''

    def init_environment(self, runtime):
        self.input_health_stream = cs.stream.create_stream('all_health')
        self.output_health_stream = cs.stream.create_stream('cs_health')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_health_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for info in self.health_data:
            self.input_health_stream.add_item(info)


if __name__ == '__main__':
    config = RiskEvaluationConfig()
