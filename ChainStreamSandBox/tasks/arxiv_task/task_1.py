from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription
import time
from ..task_tag import *


class ArxivTask1(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard, domain=Domain_Task_tag.Office,
                                modality=Modality_Task_tag.Text)
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
                "description": "A stream of summaries of arxiv papers in the computer science domain with their "
                               "title, with articles filtered for the computer science topic in the 'title' field "
                               "first, then packaged into batches every two seconds, and finally summarized",
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
        self.arxiv_output = cs.create_stream(self, "summary_of_arxiv")
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
        self.arxiv_input.for_each(filter_topic).batch(by_time=2).for_each(sum_on_paper)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'summary_of_arxiv')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['summary_of_arxiv'].append(data)

        self.output_paper_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')

    def init_output_stream(self, runtime):
        self.output_paper_stream = cs.stream.get_stream(self, 'summary_of_arxiv')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['summary_of_arxiv'].append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_papers = {'all_arxiv': []}
        for paper in self.paper_data:
            sent_papers['all_arxiv'].append(paper)
            self.input_paper_stream.add_item(paper)
            time.sleep(1)
        return sent_papers
