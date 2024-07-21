from ..task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import WifiData


class WifiVendorConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_wifi_stream = None
        self.input_wifi_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_wifi' and process the values corresponding to the "
            "'Vendor' key in the wifi dictionary: Add the vendor information to the output stream "
            "'cs_wifi'. "
        )
        self.wifi_data = WifiData().get_wifi(10)
        self.agent_example = '''
        import chainstream as cs
        class testAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("test_wifi_agent")
                self.input_stream = cs.get_stream("all_wifi")
                self.output_stream = cs.get_stream("cs_wifi")
            def start(self):
                def process_wifi(wifi):
                    Vendor = wifi["Vendor"]        
                    self.output_stream.add_item(Vendor)
                self.input_stream.register_listener(self, process_wifi)

            def stop(self):
                self.input_stream.unregister_listener(self)
        '''

    def init_environment(self, runtime):
        self.input_wifi_stream = cs.stream.create_stream('all_wifi')
        self.output_wifi_stream = cs.stream.create_stream('cs_wifi')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_wifi_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for info in self.wifi_data:
            self.input_wifi_stream.add_item(info)


if __name__ == '__main__':
    config = WifiVendorConfig()
