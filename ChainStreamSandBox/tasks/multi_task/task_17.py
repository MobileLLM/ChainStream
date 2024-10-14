from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import DialogData
from ChainStreamSandBox.raw_data import GitHubData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class MultiTask2(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_github_stream = None
        self.input_dialogues_stream = None
        self.input_github_stream = None
        self.is_office_event = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard,
                                domain=str([Domain_Task_tag.Daily_information, Domain_Task_tag.Office]),
                                modality=str([Modality_Task_tag.Text, Modality_Task_tag.Audio]))
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_dialogues",
            "description": "All dialogues record",
            "fields": {
                "dialog": "the dialog information, string"
            }
        }, {
            "stream_id": "all_github",
            "description": "all of the arxiv data",
            "fields": {
                "name": "the name of the github repository, string",
                "created_at": "the created-date the github repository, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "github_search",
                "description": "A stream of github information search based on the repository name mentioned in "
                               "dialogues",
                "fields": {
                    "name": "the name of the github repository, string",
                    "created_at": "the created-date the github repository, string"
                }
            }
        ])
        self.dialog_data = DialogData().get_dialog_batch(number)
        self.github_data = GitHubData().get_github_data(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task_1"):
        super().__init__(agent_id)
        self.dialogues_input = cs.get_stream(self, "all_dialogues")
        self.github_input = cs.get_stream(self, "all_github")
        self.github_output = cs.create_stream(self, "github_search")
        self.github_buffer = Buffer()
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def save_github(github):
            self.github_buffer.append(github)
        self.github_input.for_each(save_github)

        def recommend_github(dialogues):
            github_list = self.github_buffer.get_all()
            for github in github_list:
                if github['name'] in str(dialogues):
                    self.github_output.add_item({
                        'name':github['name'],
                        'created_at':github['created_at']
                        })
            return dialogues

        def extract_dialog(dialogues):
            dialog = dialogues["dialog"]
            return dialog
        self.dialogues_input.for_each(extract_dialog).for_each(recommend_github)
        '''

    def init_environment(self, runtime):
        self.input_dialogues_stream = cs.stream.create_stream(self, 'all_dialogues')
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')
        self.output_github_stream = cs.stream.create_stream(self, 'github_search')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['github_search'].append(data)

        self.output_github_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_dialogues_stream = cs.stream.create_stream(self, 'all_dialogues')
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')

    def init_output_stream(self, runtime):
        self.output_github_stream = cs.stream.get_stream(self, 'github_search')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['github_search'].append(data)

        self.output_github_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        dialogues = [
            {
                'dialog': [
                    {
                        'text': 'Can you help me export the Brook-GUI-For-Linux project?',
                        'act': 'directive',
                        'emotion': 'no emotion'
                    }
                ],
                'topic': 'Work',
                'id': 20001
            },
            {
                'dialog': [
                    {
                        'text': 'We need to integrate tweet-baker into our social media platform.',
                        'act': 'directive',
                        'emotion': 'no emotion'
                    }
                ],
                'topic': 'Work',
                'id': 20004
            },
            {
                'dialog': [
                    {
                        'text': 'Please incorporate dnn-speech for improved voice recognition.',
                        'act': 'directive',
                        'emotion': 'no emotion'
                    }
                ],
                'topic': 'Work',
                'id': 20005
            },
            {
                'dialog': [
                    {
                        'text': 'The flask-webapp-quickstart project is really wonderful!',
                        'act': 'directive',
                        'emotion': 'excited'
                    }
                ],
                'topic': 'Work',
                'id': 20004
            }
        ]

        self.dialog_data.extend(dialogues)
        sent_info = {"all_dialogues": [], "all_github": []}
        for github in self.github_data:
            sent_info["all_github"].append(github)
            self.input_github_stream.add_item(github)
        for dialog in self.dialog_data:
            sent_info["all_dialogues"].append(dialog)
            self.input_dialogues_stream.add_item(dialog)
        return sent_info
