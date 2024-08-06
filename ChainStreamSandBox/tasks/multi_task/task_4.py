from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import DesktopData
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription
random.seed(6666)


class WorkReminderTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_message_stream = None
        self.input_ui_stream = None
        self.input_gps_stream = None
        self.is_office_event = None

        self.eos_gap = eos_gap
        self.input_stream_description1 = StreamListDescription(streams=[{
            "stream_id": "all_gps",
            "description": "GPS data",
            "fields": {
                "Street Address": "xxx,str"
            }
        },{
            "stream_id": "all_ui",
            "description": "All ui snapshots",
            "fields": {
                "image_file": "name xxx, string"
            }
        }])
        # self.input_stream_description3 = StreamListDescription(streams=[{
        #     "stream_id": "is_office_event",
        #     "description": "whether I am in office or not",
        #     "fields": {"Status":"True or False,bool"}
        # }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_reminder",
                "description": "Reminder from the messages when I slack off in the office.(Street Address:3127 "
                               "Edgemont Boulevard)",
                "fields": {
                    "reminder": "Go back to work!"
                }
            },{
                "stream_id": "is_office_event",
                "description": "Check whether the person is in the office",
                "fields": {
                    "Status": "True or False,bool"
                }
            }
        ])
        self.gps_data = LandmarkData().get_landmarks(number)
        self.ui_data = DesktopData().get_random_sample(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask4(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task_4"):
        super().__init__(agent_id)
        self.ui_input = cs.get_stream(self, "all_ui")
        self.gps_input = cs.get_stream(self, "all_gps")
        self.message_output = cs.get_stream(self, "auto_reminder")
        self.ui_buffer = Buffer()
        self.is_office_event = cs.get_stream(self, "is_office_event")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def save_ui(ui):
            self.ui_buffer.append(ui)
        self.ui_input.for_each(save_ui)

        def check_lazy(is_office_event):
            print(is_office_event)
            if is_office_event is not None:
                uis = self.ui_buffer.pop_all()
                print("uis",len(uis))
                for ui in uis:
                    prompt = "Is the person slacking off in the office?Simply answer y or n,if you're not sure,answer y"
                    res = self.llm.query(cs.llm.make_prompt(ui['image_file'], prompt))
                    print("res", res)
                    if res.lower() == 'y':
                        self.message_output.add_item({
                            "reminder":"Go back to work!"
                        })
                return uis

        def analysis_gps(gps):
            address = gps["Street Address"]
            if address == "3127 Edgemont Boulevard":
                print("True")
                self.is_office_event.add_item("True")
                return gps
            else:
                return None
            # else:
            #     print("False")
            #     self.is_office_event.add_item("False")
            # return gps
        self.gps_input.for_each(analysis_gps).for_each(check_lazy)
        '''

    def init_environment(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'all_ui')
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.output_message_stream = cs.stream.create_stream(self, 'auto_reminder')
        self.is_office_event = cs.stream.create_stream(self, 'is_office_event')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_message_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.ui_data:
            sent_messages.append(message)
            self.input_ui_stream.add_item(message)
        for gps in self.gps_data:
            sent_messages.append(gps)
            self.input_gps_stream.add_item(gps)
        return sent_messages





