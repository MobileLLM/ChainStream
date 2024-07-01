from ..task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import LandmarkData


class LandmarkNameConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_landmark_stream = None
        self.input_landmark_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_landmarks' and process the values corresponding to the 'PropertyName' key in the landmark dictionary: "
            "Add the landmark name to the output stream 'cs_landmarks'."
        )
        self.landmark_data = LandmarkData().get_landmarks(10)
        self.agent_example = '''
        import chainstream as cs
        from chainstream.llm import get_model
        class testAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("test_landmark_agent")
                self.input_stream = cs.get_stream("all_landmarks")
                self.output_stream = cs.get_stream("cs_landmarks")
                self.llm = get_model(["text"])
            def start(self):
                def process_landmark(landmark):
                    PropertyName = landmark["PropertyName"]        
                    self.output_stream.add_item(PropertyName)
                self.input_stream.register_listener(self, process_landmark)

            def stop(self):
                self.input_stream.unregister_listener(self)
        '''

    def init_environment(self, runtime):
        self.input_landmark_stream = cs.stream.create_stream('all_landmarks')
        self.output_landmark_stream = cs.stream.create_stream('cs_landmarks')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_landmark_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for info in self.landmark_data:
            self.input_landmark_stream.add_item(info)


if __name__ == '__main__':
    config = LandmarkNameConfig()
