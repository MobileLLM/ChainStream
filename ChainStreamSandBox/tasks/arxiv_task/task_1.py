from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class ArxivTask1(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None

        self.eos_gap = eos_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "summary_by_sender",
                "description": "A list of summaries of each arxiv paper on LLM",
                "fields": {
                    "website": "name xxx, string",
                    "summary": "sum xxx, string"
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
        self.arxiv_output = cs.get_stream(self, "summary_of_paper")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_topic(paper):
            prompt = "Is this paper on computer science? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(paper['title'], prompt))
            print("filter_topic", res,paper)
            if res.lower() == 'y':
                return paper

        def sum_on_paper(paper):
            paper_list = paper['item_list']
            print(paper_list)
            prompt = "Summarize all these papers here"
            for paper_item in paper_list:
                # print(paper_item)
                title = paper_item.get('title', 'No Title')  
                abstract = paper_item.get('abstract', '')  
                print("sum_on_paper: query", abstract, prompt)
                res = self.llm.query(cs.llm.make_prompt(abstract, prompt))
                print("sum_on_paper", res)
                self.arxiv_output.add_item({
                    "title": title,
                    "summary": res
                })
        self.arxiv_input.for_each(filter_topic).batch(by_count=2).for_each(sum_on_paper)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'summary_of_paper')

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





