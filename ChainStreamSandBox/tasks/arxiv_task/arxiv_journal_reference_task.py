from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class OldArxivTask8(SingleAgentTaskConfigBase):
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
                "journal-ref": "The journal reference of the arxiv article, string",
                "title": "The title of the arxiv article, string",
                "comments": "The comments of the arxiv article, string",
                "update_date": "The update date of the arxiv article, string",
                "authors": "The authors of the arxiv article, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "arxiv_reference",
                "description": "A list of arxiv articles with their references provided",
                "fields": {
                    "title": "The title of the arxiv article, string",
                    "reference": "The journal reference of the arxiv article, string"
                }
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
        self.output_stream = cs.get_stream(self, "arxiv_reference")
        self.llm = get_model("Text")
    def start(self):
        def process_paper(paper):
            paper_title = paper["title"]
            paper_reference = paper["journal-ref"]      
            if paper_reference is not None: 
                self.output_stream.add_item({
                    "title": paper_title,
                    "reference": paper_reference
                })
        self.input_stream.for_each(process_paper)

        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'arxiv_reference')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['arxiv_reference'].append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_paper = {'all_arxiv': []}
        for message in self.paper_data:
            self.input_paper_stream.add_item(message)
            sent_paper['all_arxiv'].append(message)
        return sent_paper

