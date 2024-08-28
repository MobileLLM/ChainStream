from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import DialogData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class DialogueTask6(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_dialogue_stream = None
        self.input_dialogue_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium,
                                domain=Domain_Task_tag.Interpersonal_relationship,
                                modality=Modality_Task_tag.Audio)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_dialogues",
            "description": "A series of dialogues record",
            "fields": {
                "topic": "The id of the speaker, string",
                "dialog": "The dialogues dict with the keys: 'text', 'act', 'emotion', dict",
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "work_dialogues",
                "description": "A stream of the work-related dialogues extracted from the key 'text', with each batch "
                               "containing two items.",
                "fields": {
                    "dialog": "The work-related dialogues, string"}
            }
        ])
        self.dialogue_data = DialogData().get_dialog_batch(batch_size=10, topic=None)
        self.agent_example = '''
import chainstream as cs

class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_news_agent")
        self.input_stream = cs.get_stream(self,"all_dialogues")
        self.output_stream = cs.get_stream(self,"work_dialogues")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def process_dialogues(dialogues):
            topic_group = {}
            for dialog in dialogues:
                if dialog['topic'] == "Work":
                    if dialog['topic'] not in topic_group:
                        topic_group[dialog['topic']] = [dialog['dialog']['text']]
                    else:
                        sender_group[dialog['topic']].append([dialog['dialog']['text']])
            self.output_stream.add_item({
            'dialog':sender_group.values()
            })
            return list(topic_group.values())
        self.input_stream.batch(by_count=2).for_each(process_dialogues)
        '''

    def init_environment(self, runtime):
        self.input_dialogue_stream = cs.stream.create_stream(self, 'all_dialogues')
        self.output_dialogue_stream = cs.stream.create_stream(self, 'work_dialogues')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['work_dialogues'].append(data)

        self.output_dialogue_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_dialogue_stream = cs.stream.create_stream(self, 'all_dialogues')

    def init_output_stream(self, runtime):
        self.output_dialogue_stream = cs.stream.get_stream(self, 'work_dialogues')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['work_dialogues'].append(data)

        self.output_dialogue_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        dialogue_dict = {'all_dialogues': []}
        for dialogue in self.dialogue_data:
            self.input_dialogue_stream.add_item(dialogue)
            dialogue_dict['all_dialogues'].append(dialogue)
        return dialogue_dict
