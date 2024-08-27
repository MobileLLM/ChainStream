from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class OldArxivTask1(SingleAgentTaskConfigBase):
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
            "description": "A series of arxiv articles",
            "fields": {
                "abstract": "The abstract of the arxiv article, string",
                "title": "The title of the arxiv article, string",
                "authors": "The authors of the arxiv article, string",
                "update_date": "The date of the arxiv article, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "computer_science_arxiv",
                "description": "A series of arxiv articles on computer science domain filtered by the abstracts",
                "fields": {
                    "title": "The title of the arxiv article, string",
                    "authors": "The authors of the arxiv article, string",
                    "update_date": "The date of the arxiv article, string"}
            }
        ])

        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
import chainstream as cs
class testAgent(cs.agent.Agent):
    def __init__(self,agent_id ="test_arxiv_agent"):
        super().__init__(agent_id)
        self.input_stream = cs.get_stream(self, "all_arxiv")
        self.output_stream = cs.get_stream(self, "computer_science_arxiv")
        self.llm = cs.llm.get_model("Text")
    def start(self):
        def process_paper(paper):
            # print(paper)
            paper_content = paper["abstract"]
            title = paper["title"]
            authors = paper["authors"]
            date = paper["update_date"]
            prompt = "Is this abstract related to computer science? Simply answer y or n."
            response = self.llm.query(cs.llm.make_prompt(paper_content, prompt))
            if response.lower() == 'y':
                self.output_stream.add_item({
                    "title": title,
                    "authors": authors,
                    "update_date": date
                })
            return paper
        self.input_stream.for_each(process_paper)
    

        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'computer_science_arxiv')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['computer_science_arxiv'].append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_paper = {'all_arxiv': []}
        for message in self.paper_data:
            self.input_paper_stream.add_item(message)
            sent_paper['all_arxiv'].append(message)
        return sent_paper
