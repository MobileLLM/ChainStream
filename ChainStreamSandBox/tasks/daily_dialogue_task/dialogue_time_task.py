from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import DialogData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class DialogueTask4(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_dialogue_stream = None
        self.input_dialogue_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Interpersonal_relationship,
                                modality=Modality_Task_tag.Audio)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_dialogues",
            "description": "A stream of dialogues record",
            "fields": {
                "id": "The id of the speaker, string",
                "dialog": "The dialogues contents, string",
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "dialogues_part_of_the_day",
                "description": "A stream of dialogues record with the analysis of part of the day when the "
                               "conversation happened chosen from morning, afternoon,and evening based on the "
                               "'dialog' field",
                "fields": {
                    "id": "The id of the speaker, string",
                    "time": "The part of the day when the conversation happened chosen from ['morning','afternoon',"
                            "'evening','not clear'] based on the dialog field, string"}
            }
        ])
        self.dialogue_data = DialogData().get_dialog_batch(batch_size=10, topic=None)
        self.agent_example = '''
import chainstream as cs

class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_news_agent")
        self.input_stream = cs.get_stream(self,"all_dialogues")
        self.output_stream = cs.create_stream(self,"dialogues_part_of_the_day")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def process_dialogues(dialogues):
            dialogues_id = dialogues["id"]
            dialogues_text = dialogues["dialog"]
            prompt = "Examine the dialogue below and determine the time of day during which the conversation takes place: 'morning', 'afternoon', 'evening' or 'not sure'.Only tell me the choice."
            response = self.llm.query(cs.llm.make_prompt(prompt,str(dialogues_text)))
            self.output_stream.add_item({
            "id": dialogues_id,
            "time": response
            })

        self.input_stream.for_each(process_dialogues)

        '''

    def init_environment(self, runtime):
        self.input_dialogue_stream = cs.stream.create_stream(self, 'all_dialogues')
        self.output_dialogue_stream = cs.stream.create_stream(self, 'dialogues_part_of_the_day')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['dialogues_part_of_the_day'].append(data)

        self.output_dialogue_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_dialogue_stream = cs.stream.create_stream(self, 'all_dialogues')

    def init_output_stream(self, runtime):
        self.output_dialogue_stream = cs.stream.get_stream(self, 'dialogues_part_of_the_day')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['dialogues_part_of_the_day'].append(data)

        self.output_dialogue_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        dialogue_dict = {'all_dialogues': []}
        for dialogue in self.dialogue_data:
            self.input_dialogue_stream.add_item(dialogue)
            dialogue_dict['all_dialogues'].append(dialogue)
        return dialogue_dict
