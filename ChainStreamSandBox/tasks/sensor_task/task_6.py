from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class WeatherTask3(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=40, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None

        self.eos_gap = eos_gap
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_weather",
            "description": "All weather information",
            "fields": {
                "Precipitation_mm": "date xxx, float",
                "Date_Time": "date xxx, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "remind_rainfall",
                "description": "If the current precipitation is over 5,remind me to wear rain boots if I go out",
                "fields": {
                    "date_time":"xxx,string",
                    "precipitation":"xxx,string",
                    "reminder":"Rain boots are recommended for walking outside!"
                }
            }
        ])

        self.sensor_data = WeatherData().get_weather(sensor_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForSensorTask6(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_weather_task_6"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_weather")
        self.sensor_output = cs.get_stream(self, "remind_rainfall")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_precipitation(weather):
            humidity = weather['Precipitation_mm']
            if humidity >= 5:
                return weather

        def reminder(weather_list):
            for weather in weather_list['item_list']:
                precipitation = weather.get('Precipitation_mm')
                date_time = weather.get('Date_Time')
                self.sensor_output.add_item({
                    "date_time": date_time,
                    "precipitation": str(precipitation)+"mm",
                    "reminder": "Rain boots are recommended for walking outside!"
                })
        self.sensor_input.for_each(filter_precipitation).batch(by_count=2).for_each(reminder)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_sensor_stream = cs.stream.create_stream(self, 'remind_rainfall')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.sensor_data:
            sent_messages.append(message)
            self.input_sensor_stream.add_item(message)
        return sent_messages






