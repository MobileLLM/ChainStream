from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import WifiData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class WifiTask5(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_wifi_stream = None
        self.input_wifi_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Living,
                                modality=Modality_Task_tag.Wifi_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_wifi",
            "description": "A stream of the wifi information",
            "fields": {
                "Vendor": "The vendor of the wifi signal, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "wifi_vendor_in_French",
                "description": "A stream of the wifi vendor names in French",
                "fields": {
                    "Vendor_Name_in_French": "The vendor name of the wifi signal in French, string"
                }
            }
        ])
        self.wifi_data = WifiData().get_wifi(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_wifi_agent")
        self.input_stream = cs.get_stream(self,"all_wifi")
        self.output_stream = cs.create_stream(self,"wifi_vendor_in_French")
        self.llm = get_model("Text")
    def start(self):
        def wifi_vendor_in_French(wifi):
            Vendor = wifi["Vendor"]
            prompt = 'Please translate the vendor name into French.Only give me the translated name.'
            response = self.llm.query(cs.llm.make_prompt(prompt,Vendor))  
            self.output_stream.add_item({
                "Vendor_Name_in_French": response
            })
        self.input_stream.for_each(wifi_vendor_in_French)
        '''

    def init_environment(self, runtime):
        self.input_wifi_stream = cs.stream.create_stream(self, 'all_wifi')
        self.output_wifi_stream = cs.stream.create_stream(self, 'wifi_vendor_in_French')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['wifi_vendor_in_French'].append(data)

        self.output_wifi_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_wifi_stream = cs.stream.create_stream(self, 'all_wifi')

    def init_output_stream(self, runtime):
        self.output_wifi_stream = cs.stream.get_stream(self, 'wifi_vendor_in_French')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['wifi_vendor_in_French'].append(data)

        self.output_wifi_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        wifi_dict = {'all_wifi': []}
        for info in self.wifi_data:
            self.input_wifi_stream.add_item(info)
            wifi_dict['all_wifi'].append(info)
        return wifi_dict
