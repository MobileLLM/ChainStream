from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GitHubData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class GithubTask1(SingleAgentTaskConfigBase):
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
                "stars_count": "xxx,int",
                "watchers": "xxx, int",
                "name": "xxx, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "watchers_and_stars",
                "description": "select ten github repositories with most stars and tell me the number of watchers of "
                               "them",
                "fields": {
                    "stars": "xxx, int",
                    "name": "name xxx, string",
                    "watchers": "xxx, int"
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
        self.github_output = cs.get_stream(self, "watchers_and_stars")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def count_stars(github_dicts):
            # all_github = []
            github_list = github_dicts['item_list']
            sorted_dicts = sorted(github_list, key=lambda x: x['stars_count'], reverse=True)
            # print("after sort",sorted_dicts)
            top_10_dicts = sorted_dicts[:10]
            print(top_10_dicts)
            return top_10_dicts
        def count_watchers(github_list):
            print(github_list)
            stars = github_list.get('stars_count')
            watchers = github_list.get('watchers')
            name = github_list.get('name')
            self.github_output.add_item({
                "stars":stars,
                "name": name,
                "watchers": watchers
            })

        self.github_input.batch(by_count=10).for_each(count_stars).for_each(count_watchers)
        '''

    def init_environment(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')
        self.output_github_stream = cs.stream.create_stream(self, 'watchers_and_stars')

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





