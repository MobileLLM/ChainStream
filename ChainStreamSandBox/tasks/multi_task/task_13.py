from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SpharData
from ChainStreamSandBox.raw_data import Ego4DData
from AgentGenerator.io_model import StreamListDescription
import time
from ..task_tag import *

random.seed(6666)


class TrafficTask(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.third_person_stream = None
        self.first_person_stream = None
        self.driving_state = None
        self.output_message_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Health,
                                modality=Modality_Task_tag.Video)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_third_person",
            "description": "all third person perspective traffic data",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL, PIL.Image"
            }
        }, {
            "stream_id": "all_first_person",
            "description": "all first person perspective data in the car",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL, PIL.Image"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "output_messages",
                "description": "A prompt message when a traffic accident is detected ahead from the all_third_person "
                               "data and I am driving detected from the all_first_person data",
                "fields": {
                    "Reminder": "A notification reminding the driver to pay attention to the road conditions ahead if "
                                "there is an accident ahead.string = 'Accident ahead! Pay attention to the road'",
                }
            },
            {
                "stream_id": "driving_state",
                "description": "Trigger to determine if I am driving",
                "fields": {
                    "Status": "True or False, bool"
                }
            }
        ])
        self.third_person_data = SpharData().load_for_traffic()
        self.first_person_data = Ego4DData().load_for_traffic()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask13(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task13"):
        super().__init__(agent_id)
        self.third_person_input = cs.get_stream(self, "all_third_person")
        self.first_person_input = cs.get_stream(self, "all_first_person")
        self.message_output = cs.get_stream(self, "output_messages")
        self.driving_state = cs.get_stream(self, "driving_state")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def check_accident(third_person_inputs):
            print(third_person_inputs)
            if self.driving_state is not None:
                for frame in third_person_inputs["frame"]:
                    prompt = "Is there a traffic accident ahead?Simply tell me y or n"
                    res = self.llm.query(cs.llm.make_prompt(prompt,frame))
                    print(res)
                    if res.lower()=="y":
                        self.message_output.add_item({
                        "Reminder": "Accident ahead! Pay attention to the road"
                    })
        self.third_person_input.for_each(check_accident)

        def check_behaviour(first_person_input):
            prompt = "Please check if I am driving a car.Simply tell me y or n."
            res = self.llm.query(cs.llm.make_prompt(prompt,first_person_input['frame']))
            if res.lower() == 'y' :
                self.driving_state.add_item({
                "Status":True
                })
                return first_person_input
            else:
                return None

        self.first_person_input.for_each(check_behaviour)
        '''

    def init_environment(self, runtime):
        self.third_person_stream = cs.stream.create_stream(self, 'all_third_person')
        self.first_person_stream = cs.stream.create_stream(self, 'all_first_person')
        self.output_message_stream = cs.stream.create_stream(self, 'output_messages')
        self.driving_state = cs.stream.create_stream(self, 'driving_state')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['output_messages'].append(data)

        self.output_message_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.third_person_stream = cs.stream.create_stream(self, 'all_third_person')
        self.first_person_stream = cs.stream.create_stream(self, 'all_first_person')

    def init_output_stream(self, runtime):
        self.output_message_stream = cs.stream.get_stream(self, 'output_messages')
        self.driving_state = cs.stream.get_stream(self, 'driving_state')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['output_messages'].append(data)

        self.output_message_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_info = {'all_third_person': [], 'all_first_person': []}
        for frame in self.first_person_data:
            sent_info['all_first_person'].append(frame)
            self.first_person_stream.add_item({"frame": frame})
        for frame in self.third_person_data:
            sent_info['all_third_person'].append(frame)
            self.third_person_stream.add_item({"frame": frame})
        return sent_info
