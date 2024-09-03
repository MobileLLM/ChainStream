from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import GitHubData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


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
                              "datetime",
                "name": "the name of the github repository, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "most_commit_github",
                "description": "A stream of github repositories information (including the name, the created date and "
                               "the commit count) sorted in descending order by the commit count, with every ten "
                               "repositories packaged into a batch.",
                "fields": {
                    "created_at": "the time that the github repository was created at using ISO 8601 datetime format, "
                                  "datetime",
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
        self.github_output = cs.create_stream(self, "most_commit_github")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def count_stars(github_dicts):
            date = github_dicts['created_at']
            return github_dicts
        def count_commit(github_list):
            github_list2 = github_list['item_list']
            sorted_dicts = sorted(github_list2, key=lambda x: int(x['commit_count']), reverse=True)
            for github in sorted_dicts:
                created_at = github.get('created_at')
                commit_count = github.get('commit_count')
                name = github.get('name')
                self.github_output.add_item({
                    "created_at": created_at,
                    "name": name,
                    "commit_count": commit_count
                })
        self.github_input.for_each(count_stars).batch(by_count=10).for_each(count_commit)
        '''

    def init_environment(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')
        self.output_github_stream = cs.stream.create_stream(self, 'most_commit_github')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['most_commit_github'].append(data)

        self.output_github_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')

    def init_output_stream(self, runtime):
        self.output_github_stream = cs.stream.get_stream(self, 'most_commit_github')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['most_commit_github'].append(data)

        self.output_github_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_github = {'all_github': []}
        for github in self.github_data:
            sent_github['all_github'].append(github)
            self.input_github_stream.add_item(github)
        return sent_github
