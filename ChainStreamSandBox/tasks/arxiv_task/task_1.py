from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class ArxivTask1(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_arxiv",
            "description": "All arxiv paper",
            "fields": {
                "title": "the title of each arxiv article, string",
                "abstract": "the abstract of each arxiv article, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "summary_of_arxiv",
                "description": "A list of summaries of each arxiv paper on computer science domain(every two articles "
                               "are packaged as a batch after filtering the topic of computer science)",
                "fields": {
                    "title": "the title of each arxiv article, string",
                    "summary": "the summary of each arxiv article on computer science, string"
                }
            }
        ])

        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForArxivTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_arxiv_task_1"):
        super().__init__(agent_id)
        self.arxiv_input = cs.get_stream(self, "all_arxiv")
        self.arxiv_output = cs.get_stream(self, "summary_of_arxiv")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_topic(paper):
            prompt = "Is this paper on computer science? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(paper['title'], prompt))
            if res.lower() == 'y':
                return paper

        def sum_on_paper(paper):
            paper_list = paper['item_list']
            prompt = "Summarize all these papers here"
            for paper_item in paper_list:
                title = paper_item.get('title', 'No Title')  
                abstract = paper_item.get('abstract', '')  
                res = self.llm.query(cs.llm.make_prompt(abstract, prompt))
                self.arxiv_output.add_item({
                    "title": title,
                    "summary": res
                })
        self.arxiv_input.for_each(filter_topic).batch(by_count=2).for_each(sum_on_paper)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'summary_of_arxiv')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_papers = []
        for paper in self.paper_data:
            sent_papers.append(paper)
            self.input_paper_stream.add_item(paper)
        return sent_papers





