from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import GitHubData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class GithubTask6(SingleAgentTaskConfigBase):
    def __init__(self, github_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_github_stream = None
        self.input_github_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Office,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_github",
            "description": "All github information",
            "fields": {
                "name": "the name of the github repository, string",
                "created_at": "the created-date of the github repository, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "filter_github_date",
                "description": "A stream of the created-dates of the github repositories",
                "fields": {
                    "name": "the name of the github repository, string",
                    "created_at": "the created-date the github repository, string"
                }
            }
        ])

        self.github_data = GitHubData().get_github_data(github_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForGithubTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_github_task_1"):
        super().__init__(agent_id)
        self.github_input = cs.get_stream(self, "all_github")
        self.github_output = cs.create_stream(self, "filter_github_date")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def github_date_extraction(github_dict):
            created_date = github_dict['created_at']
            name = github_dict['name']
            self.github_output.add_item({
                "name": name,
                "created_at": created_date
            })

        self.github_input.for_each(github_date_extraction)
        '''

    def init_environment(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')
        self.output_github_stream = cs.stream.create_stream(self, 'filter_github_date')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['filter_github_date'].append(data)

        self.output_github_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')

    def init_output_stream(self, runtime):
        self.output_github_stream = cs.stream.get_stream(self, 'filter_github_date')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['filter_github_date'].append(data)

        self.output_github_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_github = {'all_github': []}
        for github in self.github_data:
            sent_github['all_github'].append(github)
            self.input_github_stream.add_item(github)
        return sent_github
