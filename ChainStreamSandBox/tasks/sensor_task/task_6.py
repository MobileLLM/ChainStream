from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class WeatherTask3(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=40):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Weather,
                                modality=Modality_Task_tag.Weather_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_weather",
            "description": "All weather information",
            "fields": {
                "Precipitation_mm": "the precipitation of the city in mm, float",
                "Date_Time": "the '%Y/%m/%d %H:%M:%S' datetime format, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "alarm_rainfall",
                "description": "A series of reminders to wear rain boots outside if the precipitation is over 5 mm,with "
                               "every two copies of weather data packaged as a batch after filtering the "
                               "precipitation which is over 5 mm",
                "fields": {
                    "Date_Time": "the '%Y/%m/%d %H:%M:%S' datetime format, string",
                    "Precipitation_mm": "the precipitation of the city in mm, float",
                    "reminder": "An auto reminder, string = Rain boots are recommended for walking outside!"
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
        self.sensor_output = cs.get_stream(self, "alarm_rainfall")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_precipitation(weather):
            Precipitation = weather['Precipitation_mm']
            if Precipitation >= 5:
                return weather

        def reminder(weather_list):
            for weather in weather_list['item_list']:
                precipitation = weather.get('Precipitation_mm')
                date_time = weather.get('Date_Time')
                self.sensor_output.add_item({
                    "Date_Time": date_time,
                    "Precipitation_mm": str(precipitation)+"mm",
                    "reminder": "Rain boots are recommended for walking outside!"
                })
        self.sensor_input.for_each(filter_precipitation).batch(by_count=2).for_each(reminder)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_sensor_stream = cs.stream.create_stream(self, 'alarm_rainfall')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['alarm_rainfall'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_weather = {'all_weather': []}
        for weather in self.sensor_data:
            sent_weather['all_weather'].append(weather)
            self.input_sensor_stream.add_item(weather)
        return sent_weather
