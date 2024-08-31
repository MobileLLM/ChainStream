from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import DialogData
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class TravelTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_message_stream = None
        self.input_weather_stream = None
        self.input_dialogue_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard,
                                domain=str([Domain_Task_tag.Interpersonal_relationship, Domain_Task_tag.Weather]),
                                modality=str([Modality_Task_tag.Weather_Sensor, Modality_Task_tag.Audio]))
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_weather",
            "description": "All weather information",
            "fields": {
                "Location": "the location, string",
                "Temperature_C": "temperature in degrees Celsius, float"
            }
        }, {
            "stream_id": "all_dialogue",
            "description": "All dialogues recorder (every two pieces of dialogues are packaged as a batch)",
            "fields": {
                "dialog": "the dialogues information, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "weather_report",
                "description": "A stream of the places extracted from the dialogues with the temperature, with every "
                               "two pieces of dialogues packaged as a batch after filtering the topic of trip from "
                               "the dialogues",
                "fields": {
                    "place": "the place extracted from the dialogue, string",
                    "temperature": "the temperature of the place extracted from the dialogue, float"
                }
            }
        ])
        self.dialogue_data = DialogData().get_dialog_batch(number)
        self.weather_data = WeatherData().get_weather(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask5(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task_4"):
        super().__init__(agent_id)
        self.weather_input = cs.get_stream(self, "all_weather")
        self.dialogue_input = cs.get_stream(self, "all_dialogue")
        self.message_output = cs.create_stream(self, "weather_report")
        self.weather_buffer = Buffer()
        self.llm = cs.llm.get_model("Text")
        
    def start(self):
        def save_weather(weather):
            self.weather_buffer.append(weather)
        self.weather_input.for_each(save_weather)

        def check_weather(dialogs_list):
            dialogs = dialogs_list["item_list"]
            weather_information = self.weather_buffer.pop_all()
            for dialog in dialogs:
                prompt = "Extract the place in the dialog.Simply tell me the place."
                res = self.llm.query(cs.llm.make_prompt(dialog, prompt))
                for weather in weather_information:
                    if weather['Location'] == res:
                        self.message_output.add_item({
                            "place": res,
                            "temperature": weather['Temperature_C']
                            })

            return dialogs

        def analysis_dialogues(dialogues_list):
            dialogues =  dialogues_list["item_list"]
            for dialogue in dialogues:
                dialog = dialogue["dialog"]
                prompt = "Are the people talking about the trip or travel?Simply answer y or n"
                res = self.llm.query(cs.llm.make_prompt(dialog, prompt))
                if res.lower() == 'y':
                    return dialog

        self.dialogue_input.batch(by_count=2).for_each(analysis_dialogues).batch(by_count=2).for_each(check_weather)
        '''

    def init_environment(self, runtime):
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')
        self.input_dialogue_stream = cs.stream.create_stream(self, 'all_dialogue')
        self.output_message_stream = cs.stream.create_stream(self, 'weather_report')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['weather_report'].append(data)

        self.output_message_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')
        self.input_dialogue_stream = cs.stream.create_stream(self, 'all_dialogue')

    def init_output_stream(self, runtime):
        self.output_message_stream = cs.stream.get_stream(self, 'weather_report')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['weather_report'].append(data)

        self.output_message_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_info = {'all_weather': [], 'all_dialogue': []}
        for dialogue in self.dialogue_data:
            sent_info['all_dialogue'].append(dialogue)
            self.input_dialogue_stream.add_item(dialogue)
        for weather in self.weather_data:
            sent_info['all_weather'].append(weather)
            self.input_weather_stream.add_item(weather)
        return sent_info
