from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *



class ArxivTask10(SingleAgentTaskConfigBase):
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
                "abstract": "The abstract of the arxiv article, string",
                "title": "The title of the arxiv article, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "arxiv_implementation",
                "description": "A stream of arxiv articles with their implementation tags chosen from ['Software', "
                               "'Hardware', 'Hybrid', 'System Integration', 'Other'] based on the abstracts",
                "fields": {
                    "title": "The title of the arxiv article, string",
                    "implementation": "The implementation tag of the arxiv article, string"
                }
            }
        ])
        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model

class TestAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_arxiv_agent")
        self.input_stream = cs.get_stream(self, "all_arxiv")
        self.output_stream = cs.create_stream(self, "arxiv_implementation")
        self.llm = get_model("Text")

    def start(self):
        def process_paper(paper):
            if "abstract" in paper:
                paper_title = paper["title"]
                paper_content = paper["abstract"]
                implementation_tags = ['Software', 'Hardware', 'Hybrid', 'System Integration', 'Other']
                prompt = "Give you an abstract of a paper: {}. What tag would you like to add to this paper? Choose from the following: {}".format(paper_content, ', '.join(implementation_tags))
                response = self.llm.query(cs.llm.make_prompt(prompt))
                self.output_stream.add_item({
                    "title": paper_title,
                    "implementation": response
                })

        self.input_stream.for_each(process_paper)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'arxiv_implementation')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['arxiv_implementation'].append(data)

        self.output_paper_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')

    def init_output_stream(self, runtime):
        self.output_paper_stream = cs.stream.get_stream(self, 'arxiv_implementation')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['arxiv_implementation'].append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_paper = {'all_arxiv': []}
        for message in self.paper_data:
            self.input_paper_stream.add_item(message)
            sent_paper['all_arxiv'].append(message)
        return sent_paper
