from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SpharData
from ChainStreamSandBox.raw_data import GPSData
from AgentGenerator.io_model import StreamListDescription
random.seed(6666)


class KitchenSafetyTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_warning_stream = None
        self.input_video_stream = None
        self.gps_stream = None
        self.eos_gap = eos_gap
        self.input_stream_description1 = StreamListDescription(streams=[{
            "stream_id": "all_video",
            "description": "video data",
            "fields": {
            }
        },{
            "stream_id": "all_gps",
            "description": "GPS data",
            "fields": {
                "Street Address": "xxx,str"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "alarm_message",
                "description": "Alarm messages when the gas stove is turned on but no one is there(Street "
                               "Address:123 Main St)",
                "fields": {
                    "alarm": "You have not turned off the stove.Please notice!"
                }
            }
        ])
        self.gps_data = GPSData().get_gps(number)
        self.video_data = SpharData().load_for_traffic()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask8(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task8"):
        super().__init__(agent_id)
        self.video_input = cs.get_stream(self, "all_video")
        self.gps_input = cs.get_stream(self, "all_gps")
        self.message_output = cs.get_stream(self, "alarm_message")
        self.video_buffer = Buffer()
        self.llm = cs.llm.get_model("image")

    def start(self):
        def save_video(video_data):
            self.video_buffer.append(video_data)
        self.video_input.for_each(save_video)

        def check_place(gps_data):
            if gps_data["Street Address"] != "123 Main St":
                three_person_data = self.video_buffer.pop_all()
                return three_person_data

        def check_stove(three_person_data):
            data_list = three_person_data["item_list"]
            prompt = "Please check whether the gas stove is turned on or not.Simply answer y or n."
            res = self.llm.query(cs.llm.make_prompt(prompt,three_person_data))
            # print("res", res)
            if res.lower()== "y" :
                self.message_output.add_item({
                    "alarm":"You have not turned off the stove.Please notice!"
                })
            return three_person_data

        self.video_input.for_each(check_place).batch(by_count=2).for_each(check_stove)
        '''

    def init_environment(self, runtime):
        self.gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_video_stream = cs.stream.create_stream(self, 'all_video')
        self.output_warning_stream = cs.stream.create_stream(self, 'alarm_message')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_warning_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.video_data:
            sent_messages.append(message)
            self.input_video_stream.add_item(message)
        for message in self.gps_data:
            sent_messages.append(message)
            self.gps_stream.add_item(message)
        return sent_messages





