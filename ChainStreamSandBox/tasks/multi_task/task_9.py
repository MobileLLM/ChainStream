from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GPSData
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class CloseWindowTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_action_stream = None
        self.input_weather_stream = None
        self.gps_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_gps",
            "description": "all of my gps data",
            "fields": {
                "Street Address": "the street address information from the gps sensor,str"
            }
        }, {
            "stream_id": "all_weather",
            "description": "All weather information",
            "fields": {
                "Location": "the weather location, string",
                "Temperature_C": "temperature in degrees Celsius, float",
                "Weather": "the weather condition,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_close_window",
                "description": "A list of commands of automatically closing the window(every two copies of weather "
                               "data are packaged as a batch after judging the home street address from gps data)",
                "fields": {
                    "action": "Close all the windows!"
                }
            }
        ])
        self.gps_data = GPSData().get_gps(number)
        self.weather_data = WeatherData().get_weather(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask9(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task9"):
        super().__init__(agent_id)
        self.weather_input = cs.get_stream(self, "all_weather")
        self.gps_input = cs.get_stream(self, "all_gps")
        self.action_output = cs.get_stream(self, "auto_close_window")
        self.weather_buffer = Buffer()
        self.llm = cs.llm.get_model("text")

    def start(self):
        def save_weather(weather_data):
            self.weather_buffer.append(weather_data)
        self.weather_input.for_each(save_weather)

        def check_place(gps_data):
            if gps_data["Street Address"] == "123 Main St":
                weather_data = self.weather_buffer.pop_all()
                return weather_data

        def close_window(weather_data):
            data_list = weather_data["item_list"]
            for data in data_list:
                if data['Location'] == "123 Main St" and data['Weather']=="Rainy":
                    self.action_output.add_item({
                        "action":"Close all the windows!"
                    })
            return reminder

        self.weather_input.for_each(check_place).batch(by_count=2).for_each(close_window)
        '''

    def init_environment(self, runtime):
        self.gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_action_stream = cs.stream.create_stream(self, 'auto_close_window')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_action_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_info = []
        for weather in self.weather_data:
            sent_info.append(weather)
            self.input_weather_stream.add_item(weather)
        for gps in self.gps_data:
            sent_info.append(gps)
            self.gps_stream.add_item(gps)
        return sent_info
