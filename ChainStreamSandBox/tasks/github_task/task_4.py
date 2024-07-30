from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GitHubData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class GithubTask4(SingleAgentTaskConfigBase):
    def __init__(self, github_number=10, eos_gap=4):
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
                "pull_requests": "xxx,int",
                "languages_used": "xxx, string",
                "name": "xxx, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "language_from_most_pr",
                "description": "select ten github repositories with most numbers of pr and tell me the computer "
                               "language used of them",
                "fields": {
                    "pull_requests": "xxx,int",
                    "name": "name xxx, string",
                    "languages_used": "xxx, string"
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
            # print("after sort",sorted_dicts)
            top_10_dicts = sorted_dicts[:10]
            print(top_10_dicts)
            return top_10_dicts
        def find_language(github_list):
            pull_requests = github_list.get('pull_requests')
            languages_used = github_list.get('languages_used')
            name = github_list.get('name')
            self.github_output.add_item({
                "pull_requests":pull_requests,
                "name": name,
                "languages_used": languages_used
            })
        self.github_input.batch(by_count=10).for_each(count_pr).for_each(find_language)
        '''

    def init_environment(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')
        self.output_github_stream = cs.stream.create_stream(self, 'language_from_most_pr')

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





