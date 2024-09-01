from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class WeatherTask8(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_weather_stream = None
        self.input_weather_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Weather,
                                modality=Modality_Task_tag.Weather_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_weather",
            "description": "A stream of the weather information",
            "fields": {
                "Location": "The location of the zone, string",
                "Temperature_C": "The temperature of the zone, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "temperatures_grouped_by_specific_location",
                "description": "A stream of the temperatures grouped by the same location with each six items "
                               "grouped as a batch.",
                "fields": {
                    "location": "The location of the zone, string",
                    "temperatures_list": "The list of the temperatures grouped by the specific location, list"
                }
            }
        ])
        self.weather_data = WeatherData().get_weather(10)
        self.agent_example = '''
import chainstream as cs
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_weather_agent")
        self.input_stream = cs.get_stream(self,"all_weather")
        self.output_stream = cs.create_stream(self,"temperatures_grouped_by_specific_location")
    def start(self):
        def grouped_location(weather_data):
            weather_list = weather_data['item_list']
            location_group = {}
            for weather in weather_list:
                if weather['Location'] not in location_group:
                    location_group[weather['Location']] = [weather['Temperature_C']]
                else:
                    location_group[weather['Location']].append(weather['Temperature_C'])
                self.output_stream.add_item({
                    'location': weather['Location'],
                    'temperatures_list': list(location_group.values())
                })
            return list(location_group.values())
        self.input_stream.batch(by_count = 6).for_each(grouped_location)
        '''

    def init_environment(self, runtime):
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_weather_stream = cs.stream.create_stream(self, 'temperatures_grouped_by_specific_location')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['temperatures_grouped_by_specific_location'].append(data)

        self.output_weather_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')

    def init_output_stream(self, runtime):
        self.output_weather_stream = cs.stream.get_stream(self, 'temperatures_grouped_by_specific_location')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['temperatures_grouped_by_specific_location'].append(data)

        self.output_weather_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        weather_dict = {'all_weather': []}
        for info in self.weather_data:
            self.input_weather_stream.add_item(info)
            weather_dict['all_weather'].append(info)
        return weather_dict
