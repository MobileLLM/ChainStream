from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class ArxivTask3(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Work,
                                scene=Scene_Task_tag.Office, modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_arxiv",
            "description": "All arxiv paper",
            "fields": {
                "title": "the title of each arxiv article, string",
                "abstract": "the abstract of each arxiv article, string",
                "authors": "the authors of each arxiv article, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "main_idea_by_Victor_Brunton",
                "description": "A list of main ideas of the arxiv articles written by Victor Brunton,summarized by "
                               "the abstracts(every two articles are packaged as a batch after filtering the author "
                               "Victor Brunton)",
                "fields": {
                    "article": "the title of each arxiv article, string",
                    "main idea": "main ideas of the arxiv articles written by Victor Brunton and summarized by the "
                                 "abstracts, string"
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
        self.arxiv_output = cs.get_stream(self, "main_idea_by_Victor_Brunton")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_authors(paper):
            authors = paper.get('authors', "")
            if "Victor Brunton" in authors:
                return paper
        def sum_on_paper(paper):
            paper_list = paper['item_list']
            prompt = "Summarize the main ideas of all these papers here"
            for paper_item in paper_list:
                title = paper_item.get('title', 'No Title')  
                abstract = paper_item.get('abstract', '')  
                res = self.llm.query(cs.llm.make_prompt(abstract, prompt))
                self.arxiv_output.add_item({
                    "article": title,
                    "main idea": res
                })
        self.arxiv_input.for_each(filter_authors).batch(by_count=2).for_each(sum_on_paper)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'main_idea_by_Victor_Brunton')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['main_idea_by_Victor_Brunton'].append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_papers = {'all_arxiv': []}
        for paper in self.paper_data:
            sent_papers['all_arxiv'].append(paper)
            self.input_paper_stream.add_item(paper)
        return sent_papers





