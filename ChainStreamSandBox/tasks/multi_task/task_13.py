from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SpharData
from AgentGenerator.io_model import StreamListDescription
import time

random.seed(6666)


class WaitingRoomTask(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.input_outdoor_stream = None
        self.input_indoor_stream = None
        self.patient_trigger = None
        self.output_message_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_third_person_outdoor",
            "description": "third_person perspective data outside the clinic",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL,string"
            }
        }, {
            "stream_id": "all_third_person_indoor",
            "description": "third_person perspective data in the clinic(the data is sent at regular intervals as a "
                           "batch every five seconds)",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL,string"
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
                "description": "A trigger when the patients exceed 5 in the waiting room",
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
        self.outdoor_input = cs.get_stream(self, "all_third_person_outdoor")
        self.indoor_input = cs.get_stream(self, "all_third_person_indoor")
        self.message_output = cs.get_stream(self, "output_messages")
        self.patient_trigger = cs.get_stream(self, "patient_trigger")
        self.llm = cs.llm.get_model("image")

    def start(self):

        def check_doctor(indoor_inputs):
            indoor_input = indoor_inputs["item_list"]
            if self.patient_trigger == "True":
                prompt = "Have the doctor come back?Simply answer y or n."
                res = self.llm.query(cs.llm.make_prompt(prompt,indoor_input["frame"]))
                if res.lower()=="n":
                    self.message_output.add_item({
                    "Notion": "There are patients who are waiting for a period of time."
                })
        self.indoor_input.batch(by_time=5).for_each(check_doctor)

        def check_number(outdoor_input):
            prompt = "Please check how many patients are in the waiting room.Please only tell me the number."
            res = self.llm.query(cs.llm.make_prompt(prompt,outdoor_input["frame"]))
            if res >= "5" :
                self.patient_trigger.add_item({"Status":"True"})
                return indoor_input
            else:
                return None

        self.outdoor_input.for_each(check_number)
        '''

    def init_environment(self, runtime):
        self.input_indoor_stream = cs.stream.create_stream(self, 'all_third_person_indoor')
        self.input_outdoor_stream = cs.stream.create_stream(self, 'all_third_person_outdoor')
        self.output_message_stream = cs.stream.create_stream(self, 'output_messages')
        self.patient_trigger = cs.stream.create_stream(self, 'patient_trigger')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_message_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_info = []
        for frame in self.video_data1:
            sent_info.append(frame)
            self.input_indoor_stream.add_item({"frame": frame})
            time.sleep(1)
        for frame in self.video_data2:
            sent_info.append(frame)
            self.input_outdoor_stream.add_item({"frame": frame})
        return sent_info
