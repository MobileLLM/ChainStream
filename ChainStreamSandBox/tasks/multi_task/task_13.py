from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SpharData
from AgentGenerator.io_model import StreamListDescription
import time
random.seed(6666)


class WaitingRoomTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.input_outdoor_stream = None
        self.input_indoor_stream = None
        self.patient_trigger = None
        self.output_message_stream = None
        self.eos_gap = eos_gap
        self.input_stream_description1 = StreamListDescription(streams=[{
            "stream_id": "all_one_person_outdoor",
            "description": "one_person perspective data",
            "fields": {
            }
        },{
            "stream_id": "all_one_person_indoor",
            "description": "one_person perspective data",
            "fields": {
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "output_messages",
                "description": "A message that reminds the doctor to come back",
                "fields": {
                    "Notion": "There are patients who are waiting for a period of time",
                }
            },
            {
                "stream_id": "patient_trigger",
                "description": "A trigger when the patient exceeds a certain number",
                "fields": {
                    "Status": "True or False"
                }
            }
        ])
        self.video_data1 = SpharData().load_for_traffic()
        self.video_data2 = SpharData().load_for_traffic()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask13(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task13"):
        super().__init__(agent_id)
        self.outdoor_input = cs.get_stream(self, "all_one_person_outdoor")
        self.indoor_input = cs.get_stream(self, "all_one_person_indoor")
        self.message_output = cs.get_stream(self, "output_messages")
        self.patient_trigger = cs.get_stream(self, "patient_trigger")
        self.llm = cs.llm.get_model("image")

    def start(self):

        def check_doctor(indoor_inputs):
            indoor_input = indoor_inputs["item_list"]
            if self.patient_trigger == "True":
                prompt = "Have the doctor come back?Simply answer y or n."
                res = self.llm.query(cs.llm.make_prompt(prompt,indoor_input))
                if res.lower()=="n":
                    self.message_output.add_item({
                    "Notion": "There are patients who are waiting for a period of time."
                })
        self.indoor_input.batch(by_time=5).for_each(check_doctor)

        def check_number(outdoor_input):
            prompt = "Please check how many patients are in the waiting room.Please only tell me the number."
            res = self.llm.query(cs.llm.make_prompt(prompt,outdoor_input))
            if res >= "5" :
                self.patient_trigger.add_item("True")
                return indoor_input
            else:
                return None

        self.outdoor_input.for_each(check_number)
        '''

    def init_environment(self, runtime):
        self.input_indoor_stream = cs.stream.create_stream(self, 'all_one_person_indoor')
        self.input_outdoor_stream = cs.stream.create_stream(self, 'all_one_person_outdoor')
        self.output_message_stream = cs.stream.create_stream(self, 'output_messages')
        self.patient_trigger = cs.stream.create_stream(self, 'patient_trigger')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_message_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.video_data1:
            sent_messages.append(message)
            self.input_indoor_stream.add_item(message)
            time.sleep(1)
        for message in self.video_data2:
            sent_messages.append(message)
            self.input_outdoor_stream.add_item(message)
        return sent_messages





