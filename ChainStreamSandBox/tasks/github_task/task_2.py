from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GitHubData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class GithubTask2(SingleAgentTaskConfigBase):
    def __init__(self, github_number=40):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_github_stream = None
        self.input_github_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Office,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_github",
            "description": "All github information",
            "fields": {
                "commit_count": "the number of the commits in the github repository, int",
                "created_at": "the time that the github repository was created at using ISO 8601 datetime format, "
                              "string",
                "name": "the name of the github repository, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "commit_most_this_year",
                "description": "Ten GitHub repositories with the most commits in 2024, with every seven GitHub "
                               "repositories packaged into a batch after filtering for repositories created in 2024.",
                "fields": {
                    "date": "the time that the github repository was created at using ISO 8601 datetime format, string",
                    "name": "the name of the github repository, string",
                    "commit_count": "the number of the commits in the github repository, int"
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
        self.github_output = cs.get_stream(self, "commit_most_this_year")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def count_stars(github_dicts):
            date = github_dicts['created_at']
            if date.startswith("2024"):
                return github_dicts
        def count_commit(github_list):
            github_list2 = github_list['item_list']
            sorted_dicts = sorted(github_list2, key=lambda x: int(x['commit_count']), reverse=True)
            top_10_dicts = sorted_dicts[:10]
            for github in top_10_dicts:
                created_at = github.get('created_at')
                commit_count = github.get('commit_count')
                name = github.get('name')
                self.github_output.add_item({
                    "date": created_at,
                    "name": name,
                    "commit_count": commit_count
                })
        self.github_input.for_each(count_stars).batch(by_count=7).for_each(count_commit)
        '''

    def init_environment(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')
        self.output_github_stream = cs.stream.create_stream(self, 'commit_most_this_year')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['commit_most_this_year'].append(data)

        self.output_github_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_github = {'all_github': []}
        for github in self.github_data:
            sent_github['all_github'].append(github)
            self.input_github_stream.add_item(github)
        return sent_github





