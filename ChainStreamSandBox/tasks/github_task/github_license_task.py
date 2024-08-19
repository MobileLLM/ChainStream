from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GitHubData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class OldGithubTask6(SingleAgentTaskConfigBase):
    def __init__(self, github_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_github_stream = None
        self.input_github_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Work,
                                scene=Scene_Task_tag.Office, modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_github",
            "description": "All github information(every three github repositories are packaged as a batch)",
            "fields": {
                "stars_count": "the number of the stars received in the github repository, int",
                "watchers": "the number of the watchers in the github repository, int",
                "name": "the name of the github repository, string",
                "primary_language": "the primary programming language of the github repository, string",
                "licence": "the licence of the github repository, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "github_licence",
                "description": "A list of the licences of the github repositories",
                "fields": {
                    "name": "the name of the github repository, string",
                    "licence": "the licence of the github repository, string"
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
        self.github_output = cs.get_stream(self, "github_licence")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def github_licence_extraction(github_dict):
            licence = github_dict['licence']
            name = github_dict['name']
            self.github_output.add_item({
                "name": name,
                "licence": licence
            })

        self.github_input.for_each(github_licence_extraction)
        '''

    def init_environment(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')
        self.output_github_stream = cs.stream.create_stream(self, 'github_licence')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['github_licence'].append(data)

        self.output_github_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_github = {'all_github': []}
        for github in self.github_data:
            sent_github['all_github'].append(github)
            self.input_github_stream.add_item(github)
        return sent_github
