from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class WeatherTask4(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=40):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard, domain=Domain_Task_tag.Weather,
                                modality=Modality_Task_tag.Weather_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_weather",
            "description": "All weather information",
            "fields": {
                "Wind_Speed_kmh": "the wind speed sensor in kmh, float",
                "Date_Time": "The time of the zone with the format of '%Y/%m/%d %H:%M', datetime"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "take_clothes_down",
                "description": "A stream of reminders to take down clothes in the balcony if the wind speed is over 20 "
                               "kmh,with every two copies of weather data packaged as a batch after filtering the "
                               "wind speed which is over 20 kmh",
                "fields": {
                    "Date_Time": "The time of the zone with the format of '%Y/%m/%d %H:%M', datetime",
                    "Wind_Speed_kmh": "the wind speed sensor in kmh, float",
                    "reminder": "An auto reminder, string = Collect the clothes in the balcony!"
                }
            }
        ])

        self.sensor_data = WeatherData().get_weather(sensor_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForSensorTask7(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_weather_task_6"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_weather")
        self.sensor_output = cs.create_stream(self, "take_clothes_down")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_precipitation(weather):
            wind_speed = weather['Wind_Speed_kmh']
            if wind_speed >= 20:
                return weather

        def reminder(weather_list):
            for weather in weather_list['item_list']:
                wind_speed = weather.get('Wind_Speed_kmh')
                date_time = weather.get('Date_Time')
                self.sensor_output.add_item({
                    "Date_Time": date_time,
                    "Wind_Speed_kmh": str(wind_speed),
                    "reminder": "Collect the clothes in the balcony!"
                })
        self.sensor_input.for_each(filter_precipitation).batch(by_count=2).for_each(reminder)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_sensor_stream = cs.stream.create_stream(self, 'take_clothes_down')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['take_clothes_down'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_weather')

    def init_output_stream(self, runtime):
        self.output_sensor_stream = cs.stream.get_stream(self, 'take_clothes_down')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['take_clothes_down'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_weather = {'all_weather': []}
        for weather in self.sensor_data:
            sent_weather['all_weather'].append(weather)
            self.input_sensor_stream.add_item(weather)
        return sent_weather
