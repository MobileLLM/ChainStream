from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GitHubData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class GithubTask2(SingleAgentTaskConfigBase):
    def __init__(self, github_number=40, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_github_stream = None
        self.input_github_stream = None

        self.eos_gap = eos_gap
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_github",
            "description": "All github messages",
            "fields": {
                "commit_count": "xxx,int",
                "created_at": "xxx, string",
                "name": "xxx, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "commit_most_this_year",
                "description": "select ten github repositories this year and tell me the number of commits of "
                               "them",
                "fields": {
                    "date": "xxx, string",
                    "name": "name xxx, string",
                    "commit_count": "xxx, int"
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
                # print(github_dicts)
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

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_github_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_github = []
        for message in self.github_data:
            sent_github.append(message)
            self.input_github_stream.add_item(message)
        return sent_github





