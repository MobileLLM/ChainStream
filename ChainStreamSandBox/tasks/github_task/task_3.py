from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GitHubData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class GithubTask3(SingleAgentTaskConfigBase):
    def __init__(self, github_number=20):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_github_stream = None
        self.input_github_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_github",
            "description": "All github information",
            "fields": {
                "licence": "the licence of the github repository,string",
                "forks_count": "the number of forks from the github repository, int",
                "name": "the name of the github repository, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "most_forks_with_licence",
                "description": "A list of fork number of github repositories with licence(every three github "
                               "repositories are packaged as a batch after filtering the github with licence)",
                "fields": {
                    "licence": "the licence of the github repository,string",
                    "name": "the name of the github repository, string",
                    "forks_count": "the number of forks from the github repository, int"
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
        self.github_output = cs.get_stream(self, "most_forks_with_licence")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def license_or_not(github_dicts):
            license_value = github_dicts.get('licence') 
            if license_value:  
                return github_dicts
        def count_forks(github_list):
            github_list2 = github_list['item_list']
            sorted_dicts = sorted(github_list2, key=lambda x: int(x['forks_count']), reverse=True)
            top_10_dicts = sorted_dicts[:10]
            for github in top_10_dicts:
                forks_count = github.get('forks_count')
                name = github.get('name')
                licence =  github.get('licence')
                self.github_output.add_item({
                    "licence":licence,
                    "name": name,
                    "forks_count": forks_count
                })
        self.github_input.for_each(license_or_not).batch(by_count=3).for_each(count_forks)
        '''

    def init_environment(self, runtime):
        self.input_github_stream = cs.stream.create_stream(self, 'all_github')
        self.output_github_stream = cs.stream.create_stream(self, 'most_forks_with_licence')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_github_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_github = []
        for github in self.github_data:
            sent_github.append(github)
            self.input_github_stream.add_item(github)
        return sent_github





