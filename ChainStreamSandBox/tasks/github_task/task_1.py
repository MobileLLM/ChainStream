from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GitHubData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class GithubTask1(SingleAgentTaskConfigBase):
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
                "stars_count": "the number of the stars received in the github repository, int",
                "watchers": "the number of the watchers in the github repository, int",
                "name": "the name of the github repository, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "top_ten_stars_github_repository",
                "description": "Package every three GitHub repositories into a batch before processing. Then, "
                               "select the ten repositories with the most stars and count the number of watchers for "
                               "each repository.",
                "fields": {
                    "stars_count": "the number of the stars received in the github repository, int",
                    "name": "the name of the github repository, string",
                    "watchers": "the number of the watchers in the github repository, int"
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
        self.github_output = cs.create_stream(self, "top_ten_stars_github_repository")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def count_stars(github_dicts):
            github_list = github_dicts['item_list']
            sorted_dicts = sorted(github_list, key=lambda x: x['stars_count'], reverse=True)
            top_10_dicts = sorted_dicts[:10]
            return top_10_dicts
        def count_watchers(github_list):
            stars = github_list.get('stars_count')
            watchers = github_list.get('watchers')
            name = github_list.get('name')
            self.github_output.add_item({
                "stars_count": stars,
                "name": name,
                "watchers": watchers
            })

        self.github_input.batch(by_count=3).for_each(count_stars).for_each(count_watchers)
        '''

    def init_environment(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')
        self.output_github_stream = cs.stream.create_stream(self, 'top_ten_stars_github_repository')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['top_ten_stars_github_repository'].append(data)

        self.output_github_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')

    def init_output_stream(self, runtime):
        self.output_github_stream = cs.stream.get_stream(self, 'top_ten_stars_github_repository')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['top_ten_stars_github_repository'].append(data)

        self.output_github_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_github = {'all_github': []}
        for github in self.github_data:
            sent_github['all_github'].append(github)
            self.input_github_stream.add_item(github)
        return sent_github
