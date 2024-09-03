from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import WifiData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class WifiTask1(SingleAgentTaskConfigBase):
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
                "Channel": "The channel of the wifi signal, int"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "wifi_ssid_same_channel",
                "description": "A stream of wifi SSID information grouped by the same wifi channel statistics,"
                               "with every two copies of data grouped into a batch",
                "fields": {
                    "Channel": "The channel of the wifi stream, int",
                    "SSID": "A group of SSIDs from wifi stream that share the same channel, list of int",
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
        self.output_stream = cs.create_stream(self,"wifi_ssid_same_channel")
    def start(self):
        def group_by_wifi_channel(wifi):
            wifi_list = wifi['item_list']
            channel_group = {}
            for wifi in wifi_list:
                if wifi['Channel'] not in channel_group:
                    channel_group[wifi['Channel']] = [wifi['SSID']]
                else:
                    channel_group[wifi['Channel']].append(wifi['SSID'])
            self.output_stream.add_item({
                'Channel': wifi['Channel'],
                'SSID': list(channel_group.values())
            })
            return list(channel_group.values())
        self.input_stream.batch(by_count=2).for_each(group_by_wifi_channel)
        '''

    def init_environment(self, runtime):
        self.input_wifi_stream = cs.stream.create_stream(self, 'all_wifi')
        self.output_wifi_stream = cs.stream.create_stream(self, 'wifi_ssid_same_channel')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['wifi_ssid_same_channel'].append(data)

        self.output_wifi_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_wifi_stream = cs.stream.create_stream(self, 'all_wifi')

    def init_output_stream(self, runtime):
        self.output_wifi_stream = cs.stream.get_stream(self, 'wifi_ssid_same_channel')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['wifi_ssid_same_channel'].append(data)

        self.output_wifi_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        wifi_dict = {'all_wifi': []}
        for info in self.wifi_data:
            self.input_wifi_stream.add_item(info)
            wifi_dict['all_wifi'].append(info)
        return wifi_dict
