from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import DialogData
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class MultiTask3(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_weather_stream = None
        self.input_dialogues_stream = None
        self.input_weather_stream = None
        self.is_office_event = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard,
                                domain=str([Domain_Task_tag.Office, Domain_Task_tag.Location]),
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_dialogues",
            "description": "All dialogues record",
            "fields": {
                "dialog": "the dialog information, string"
            }
        }, {
            "stream_id": "all_weather",
            "description": "all of the weather data",
            "fields": {
                "Temperature_C": "the temperature of the location, float",
                "Wind_Speed_kmh": "the wind speed of the location, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "weather_search",
                "description": "A series of weather information search based on the name mentioned in dialogues",
                "fields": {
                    "Location": "the location mentioned in the travel dialogs, string",
                    "Temperature_C": "the temperature of the location, float",
                    "Wind_Speed_kmh": "the wind speed of the location, float"
                }
            }
        ])
        self.dialog_data = DialogData().get_dialog_batch(number)
        self.weather_data = WeatherData().get_weather(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task_1"):
        super().__init__(agent_id)
        self.dialogues_input = cs.get_stream(self, "all_dialogues")
        self.weather_input = cs.get_stream(self, "all_weather")
        self.weather_output = cs.get_stream(self, "weather_search")
        self.weather_buffer = Buffer()
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def save_weather(weather):
            self.weather_buffer.append(weather)
        self.weather_input.for_each(save_weather)

        def find_weather_info(dialogues):
            weather_list = self.weather_buffer.get_all()
            for weather in weather_list:
                if weather['Location'] in str(dialogues):
                    self.weather_output.add_item({
                        'Location':weather['Location'],
                        'Temperature':weather['Temperature_C'],
                        'Wind_Speed':weather['Wind_Speed_kmh']
                        })
            return dialogues

        def extract_dialog(dialogues):
            dialog = dialogues["dialog"]
            return dialog
        self.dialogues_input.for_each(extract_dialog).for_each(find_weather_info)
        '''

    def init_environment(self, runtime):
        self.input_dialogues_stream = cs.stream.create_stream(self, 'all_dialogues')
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_weather_stream = cs.stream.create_stream(self, 'weather_search')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['weather_search'].append(data)

        self.output_weather_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_dialogues_stream = cs.stream.create_stream(self, 'all_dialogues')
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')

    def init_output_stream(self, runtime):
        self.output_weather_stream = cs.stream.get_stream(self, 'weather_search')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['weather_search'].append(data)

        self.output_weather_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        dialogs = [
            {
                'dialog': [
                    {
                        'text': 'I would love to visit Chicago for its architecture and deep-dish pizza!',
                        'act': 'statement',
                        'emotion': 'excitement'
                    }
                ],
                'topic': 'Travel',
                'id': 20002
            },
            {
                'dialog': [
                    {
                        'text': 'Do you know any good hiking trails in Phoenix?',
                        'act': 'question',
                        'emotion': 'curiosity'
                    }
                ],
                'topic': 'Travel',
                'id': 20003
            },
            {
                'dialog': [
                    {
                        'text': 'San Antonio has such rich history and culture, I can’t wait to explore it!',
                        'act': 'statement',
                        'emotion': 'enthusiasm'
                    }
                ],
                'topic': 'Travel',
                'id': 20004
            }
        ]
        self.dialog_data.extend(dialogs)
        sent_info = {"all_dialogues": [], "all_weather": []}
        for weather in self.weather_data:
            sent_info["all_weather"].append(weather)
            self.input_weather_stream.add_item(weather)
        for dialog in self.dialog_data:
            sent_info["all_dialogues"].append(dialog)
            self.input_dialogues_stream.add_item(dialog)
        return sent_info
