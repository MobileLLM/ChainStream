from ..task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import LandmarkData


class LandmarkFloorsConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_landmark_stream = None
        self.input_landmark_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_landmarks' and process the values corresponding to the 'NumberofFloors' key in the landmark dictionary: "
            "Add the floor number to the output stream 'cs_landmarks'."
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
                    Number_of_Floors = landmark["NumberofFloors"]        
                    self.output_stream.add_item(Number_of_Floors)
                self.input_stream.for_each(self, process_landmark)

            def stop(self):
                self.input_stream.unregister_all(self)
        '''

    def init_environment(self, runtime):
        self.input_landmark_stream = cs.stream.create_stream('all_landmarks')
        self.output_landmark_stream = cs.stream.create_stream('cs_landmarks')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_landmark_stream.for_each(self, record_output)

    def start_task(self, runtime):
        for info in self.landmark_data:
            self.input_landmark_stream.add_item(info)


if __name__ == '__main__':
    config = LandmarkFloorsConfig()
