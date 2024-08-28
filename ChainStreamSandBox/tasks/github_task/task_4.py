from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GitHubData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class GithubTask4(SingleAgentTaskConfigBase):
    def __init__(self, github_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_github_stream = None
        self.input_github_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard, domain=Domain_Task_tag.Office,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_github",
            "description": "All github information",
            "fields": {
                "pull_requests": "the number of the pull-requests of the github repository, int",
                "languages_used": "The code language used in github, string",
                "name": "the name of the github repository, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "language_from_most_pr",
                "description": "A series of code language used in the github projects with most number of "
                               "pull-requests, with every three github repositories packaged as a batch",
                "fields": {
                    "pull_requests": "the name of the github repository",
                    "name": "the name of the github repository, string",
                    "languages_used": "The code language used in github, string"
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
        self.github_output = cs.get_stream(self, "language_from_most_pr")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def count_pr(github_dicts):
            github_list = github_dicts['item_list']
            sorted_dicts = sorted(github_list, key=lambda x: x['pull_requests'], reverse=True)
            top_10_dicts = sorted_dicts[:10]
            return top_10_dicts
        def find_language(github_list):
            pull_requests = github_list.get('pull_requests')
            languages_used = github_list.get('languages_used')
            name = github_list.get('name')
            self.github_output.add_item({
                "pull_requests": pull_requests,
                "name": name,
                "languages_used": languages_used
            })
        self.github_input.batch(by_count=3).for_each(count_pr).for_each(find_language)
        '''

    def init_environment(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')
        self.output_github_stream = cs.stream.create_stream(self, 'language_from_most_pr')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['language_from_most_pr'].append(data)

        self.output_github_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')

    def init_output_stream(self, runtime):
        self.output_github_stream = cs.stream.get_stream(self, 'language_from_most_pr')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['language_from_most_pr'].append(data)

        self.output_github_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_github = {'all_github': []}
        for github in self.github_data:
            sent_github['all_github'].append(github)
            self.input_github_stream.add_item(github)
        return sent_github
