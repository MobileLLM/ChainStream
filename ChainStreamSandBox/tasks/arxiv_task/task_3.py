from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class ArxivTask3(SingleAgentTaskConfigBase):
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
                "abstract": "text xxx, string",
                "authors": "authors xxx, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "idea_by_Victor",
                "description": "Filter the papers written by Victor Brunton,then tell me the key idea",
                "fields": {
                    "article": " xxx, string",
                    "key idea": "sum xxx, string"
                }
            }
        ])

        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForArxivTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_arxiv_task_3"):
        super().__init__(agent_id)
        self.arxiv_input = cs.get_stream(self, "all_arxiv")
        self.arxiv_output = cs.get_stream(self, "idea_by_Victor")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_authors(paper):
            authors = paper.get('authors', "")
            if "Victor Brunton" in authors:
                print(paper)
                return paper
        def sum_on_paper(paper):
            paper_list = paper['item_list']
            print(paper_list)
            prompt = "Summarize all these papers here"
            for paper_item in paper_list:
                # print(paper_item)
                title = paper_item.get('title', 'No Title')  
                abstract = paper_item.get('abstract', '')  
                # print("sum_on_paper: query", abstract, prompt)
                res = self.llm.query(cs.llm.make_prompt(abstract, prompt))
                # print("sum_on_paper", res)
                self.arxiv_output.add_item({
                    "title": title,
                    "summary": res
                })
        self.arxiv_input.for_each(filter_authors).batch(by_count=2).for_each(sum_on_paper)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'idea_by_Victor')

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





