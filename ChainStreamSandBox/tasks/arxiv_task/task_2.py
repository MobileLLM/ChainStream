from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class ArxivTask2(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None

        self.eos_gap = eos_gap
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_arxiv",
            "description": "All arxiv information",
            "fields": {
                "title": "name xxx, string",
                "abstract": "text xxx, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "research_method",
                "description": "A list of research method on arxiv paper on math",
                "fields": {
                    "abstract": "xxx, string",
                    "method": "xxx, string"
                }
            }
        ])

        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForArxivTask2(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_arxiv_task_2"):
        super().__init__(agent_id)
        self.arxiv_input = cs.get_stream(self, "all_arxiv")
        self.arxiv_output = cs.get_stream(self, "research_method")

        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_topic(paper):
            prompt = "Is this paper on math? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(paper['title'], prompt))
            # print("filter_topic", res,paper)
            if res.lower() == 'y':
                return paper

        def sum_on_paper(paper):
            paper_list = paper['item_list']
            print(paper_list)
            prompt = "Summarize the research method of the papers here"
            for paper_item in paper_list:
                print(paper_item)
                title = paper_item.get('title', 'No Title')  
                abstract = paper_item.get('abstract', '')  
                print("sum_on_paper: query", abstract, prompt)
                res = self.llm.query(cs.llm.make_prompt(abstract, prompt))
                print("sum_on_paper", res)
                self.arxiv_output.add_item({
                    "title": title,
                    "method": res
                })
        self.arxiv_input.for_each(filter_topic).batch(by_count=2).for_each(sum_on_paper)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'research_method')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.paper_data:
            sent_messages.append(message)
            self.input_paper_stream.add_item(message)
        return sent_messages





