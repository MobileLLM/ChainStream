from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class ArxivTask11(SingleAgentTaskConfigBase):
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
            "description": "A stream of arxiv articles",
            "fields": {
                "journal-ref": "The journal reference of the arxiv article, string",
                "title": "The title of the arxiv article, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "arxiv_reference_in_French",
                "description": "A stream of arxiv articles titles with their translated references in French provided",
                "fields": {
                    "title": "The title of the arxiv article, string",
                    "journal-ref-French": "The journal reference of the arxiv article translated in French, string"
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
        self.output_stream = cs.create_stream(self, "arxiv_reference_in_French")
        self.llm = get_model("Text")
    def start(self):
        def process_paper(paper):
            paper_title = paper["title"]
            paper_reference = paper["journal-ref"]
            prompt = 'Please translate the following paper reference into French.Only give me the translated sentence.'  
            res = self.llm.query(cs.llm.make_prompt(prompt,paper_reference))    
            if paper_reference is not None: 
                self.output_stream.add_item({
                    "title": paper_title,
                    "journal-ref-French": res
                })
        self.input_stream.for_each(process_paper)

        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'arxiv_reference_in_French')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['arxiv_reference_in_French'].append(data)

        self.output_paper_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')

    def init_output_stream(self, runtime):
        self.output_paper_stream = cs.stream.get_stream(self, 'arxiv_reference_in_French')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['arxiv_reference_in_French'].append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_paper = {'all_arxiv': []}
        for message in self.paper_data:
            self.input_paper_stream.add_item(message)
            sent_paper['all_arxiv'].append(message)
        return sent_paper
