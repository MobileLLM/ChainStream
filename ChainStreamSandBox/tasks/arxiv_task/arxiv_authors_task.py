from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class OldArxivTask4(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Office,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_arxiv",
            "description": "A list of arxiv articles",
            "fields": {
                "authors": "The authors of the arxiv article, string",
                "title": "The title of the arxiv article, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "authors_number",
                "description": "A list of arxiv articles with calculated numbers of the authors",
                "fields": {
                    "title": "The title of the arxiv article, string",
                    "authors": "The authors of the arxiv article, string",
                    "number": "The number of authors of the arxiv article, int"}
            }
        ])

        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_arxiv_agent")
        self.input_stream = cs.get_stream(self, "all_arxiv")
        self.output_stream = cs.get_stream(self, "authors_number")
        self.llm = get_model("Text")
    def start(self):
        def process_paper(paper):
            paper_title = paper["title"]
            paper_authors = paper["authors"]      
            prompt = "Now I give you the information on the authors of these papers. How many authors does this paper have? Please just provide the number of authors."
            response = self.llm.query(cs.llm.make_prompt(prompt,paper_authors))
            self.output_stream.add_item({
                    "title": paper_title,
                    "authors": paper_authors,
                    "number": response
                })
        self.input_stream.for_each(process_paper)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'authors_number')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['authors_number'].append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_paper = {'all_arxiv': []}
        for message in self.paper_data:
            self.input_paper_stream.add_item(message)
            sent_paper['all_arxiv'].append(message)
        return sent_paper
