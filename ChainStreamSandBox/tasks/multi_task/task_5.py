from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import DialogData
from ChainStreamSandBox.raw_data import LandmarkData
from  ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class TravelTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_message_stream = None
        self.input_weather_stream = None
        self.input_dialogue_stream = None
        self.input_gps_stream = None

        self.eos_gap = eos_gap
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_email",
            "description": "All email messages",
            "fields": {
                "sender": "name xxx, string",
                "Content": "text xxx, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_reply_in_office",
                "description": "Replied list of emails,excluding ads when I am in the office",
                "fields": {
                    "content": "xxx, string",
                    "tag": "Received, string"
                }
            }
        ])
        self.gps_data = LandmarkData().get_landmarks(number)
        self.dialogue_data = DialogData().get_dialog_batch(number)
        self.weather_data = WeatherData().get_weather(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForEmailTask4(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_email_task_4"):
        super().__init__(agent_id)
        self.weather_input = cs.get_stream(self, "all_weather")
        self.gps_input = cs.get_stream(self, "all_gps")
        self.dialogue_input = cs.get_stream(self, "all_dialogue")
        self.message_output = cs.get_stream(self, "weather_and_location")
        self.weather_buffer = Buffer()
        self.gps_buffer = Buffer()
        self.llm = cs.llm.get_model("Text")
        
    def start(self):
        def save_weather(weather):
            self.weather_buffer.append(weather)
        self.weather_input.for_each(save_weather)
        
        def save_gps(gps):
            self.gps_buffer.append(gps)
        self.gps_input.for_each(save_gps)

        def check_weather(dialogs_list):
            dialogs = dialogs_list["item_list"]
            # print(dialogs)
            weather_information = self.weather_buffer.pop_all()
            # print(weather_information)
            gps_information = self.gps_buffer.pop_all()
            for dialog in dialogs:
                print(dialog)
                prompt = "Extract the place in the dialog.Simply tell me the place."
                print(prompt)
                res = self.llm.query(cs.llm.make_prompt(dialog, prompt))
                print(res)
                for weather in weather_information:
                    print(weather)
                    if weather['Location'] == res:
                        self.message_output.add_item({
                            "res":res,
                            "weather":weather['Temperature_C']
                            })

            return dialogs

        def analysis_dialogues(dialogues_list):
            dialogues =  dialogues_list["item_list"]
            # print(dialogues)
            for dialogue in dialogues:
                dialog = dialogue["dialog"]
                # print(dialog)
                prompt = "Are the people talking about the trip or travel?Simply answer y or n"
                res = self.llm.query(cs.llm.make_prompt(dialog, prompt))
                # print(res)
                if res.lower() == 'y':
                    # print(dialog)
                    return dialog

        self.dialogue_input.batch(by_count=2).for_each(analysis_dialogues).batch(by_count=2).for_each(check_weather)
        '''

    def init_environment(self, runtime):
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_dialogue_stream = cs.stream.create_stream(self, 'all_dialogue')
        self.output_message_stream = cs.stream.create_stream(self, 'weather_and_location')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_message_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.dialogue_data:
            sent_messages.append(message)
            self.input_dialogue_stream.add_item(message)
        for gps in self.gps_data:
            sent_messages.append(gps)
            self.input_gps_stream.add_item(gps)
        for weather in self.weather_data:
            sent_messages.append(weather)
            self.input_weather_stream.add_item(weather)
        return sent_messages





