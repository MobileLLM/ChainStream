from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import WifiData
from AgentGenerator.io_model import StreamListDescription


class OldWifiTask2(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_wifi_stream = None
        self.input_wifi_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_wifi",
            "description": "A list of the wifi information",
            "fields": {
                "MAC.Address": "The mac address of the wifi signal,string",
                "Vendor": "The vendor of the wifi signal,string",
                "SSID": "The SSID of the wifi signal,string",
                "Signal": "The signal strength of the wifi signal,int",
                "Channel": "The channel of the wifi signal,int"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "wifi_address",
                "description": "A list of the wifi mac address statistics",
                "fields": {
                    "MAC_Address": "The mac address of the wifi signal,string"
                }
            }
        ])
        self.wifi_data = WifiData().get_wifi(10)
        self.agent_example = '''
import chainstream as cs
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_wifi_agent")
        self.input_stream = cs.get_stream(self,"all_wifi")
        self.output_stream = cs.get_stream(self,"wifi_address")
    def start(self):
        def process_wifi(wifi):
            MAC_Address = wifi["MAC.Address"]        
            self.output_stream.add_item({
                "MAC_Address":MAC_Address
            })
        self.input_stream.for_each(process_wifi)
        '''

    def init_environment(self, runtime):
        self.input_wifi_stream = cs.stream.create_stream(self, 'all_wifi')
        self.output_wifi_stream = cs.stream.create_stream(self, 'wifi_address')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['wifi_address'].append(data)

        self.output_wifi_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        wifi_dict = {'all_wifi': []}
        for info in self.wifi_data:
            self.input_wifi_stream.add_item(info)
            wifi_dict['all_wifi'].append(info)
        return wifi_dict

