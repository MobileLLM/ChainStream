from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import DesktopData
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class WorkReminderTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_message_stream = None
        self.input_ui_stream = None
        self.input_gps_stream = None
        self.is_office_event = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard, domain=Domain_Task_tag.Work,
                                scene=Scene_Task_tag.Office, modality=[Modality_Task_tag.Text, Modality_Task_tag.Image])
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_gps",
            "description": "all of my gps information",
            "fields": {
                "Street Address": "the street address information from the gps sensor,str"
            }
        }, {
            "stream_id": "all_ui",
            "description": "all of my ui snapshots",
            "fields": {
                "image_file": "image file in the Jpeg format processed using PIL,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_reminder",
                "description": "A list of reminder messages when I slack off in the office.(Office street address:3127 "
                               "Edgemont Boulevard)",
                "fields": {
                    "reminder": "Go back to work!"
                }
            }, {
                "stream_id": "is_office_event",
                "description": "A check for whether the person is in the office",
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
            if is_office_event is not None:
                uis = self.ui_buffer.pop_all()
                for ui in uis:
                    prompt = "Is the person slacking off in the office?Simply answer y or n,if you're not sure,answer y"
                    res = self.llm.query(cs.llm.make_prompt(ui['image_file'], prompt))
                    if res.lower() == 'y':
                        self.message_output.add_item({
                            "reminder":"Go back to work!"
                        })
                return uis

        def analysis_gps(gps):
            address = gps["Street Address"]
            if address == "3127 Edgemont Boulevard":
                self.is_office_event.add_item({"Status":"True"})
                return gps
            else:
                return None
        self.gps_input.for_each(analysis_gps).for_each(check_lazy)
        '''

    def init_environment(self, runtime):
        self.input_ui_stream = cs.stream.create_stream(self, 'all_ui')
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.output_message_stream = cs.stream.create_stream(self, 'auto_reminder')
        self.is_office_event = cs.stream.create_stream(self, 'is_office_event')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['auto_reminder'].append(data)
            self.output_record['is_office_event'].append(data)

        self.output_message_stream.for_each(record_output)
        self.is_office_event.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_info = {'all_ui': [], 'all_gps': []}
        for frame in self.ui_data:
            sent_info['all_ui'].append(frame)
            self.input_ui_stream.add_item(frame)
        for gps in self.gps_data:
            sent_info['all_gps'].append(gps)
            self.input_gps_stream.add_item(gps)
        return sent_info
