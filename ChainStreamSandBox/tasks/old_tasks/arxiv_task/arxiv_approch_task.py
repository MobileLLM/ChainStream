from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class OldArxivTask3(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_arxiv",
            "description": "A list of arxiv articles",
            "fields": {
                "abstract": "The abstract of the arxiv article,string",
                "title": "The title of the arxiv article,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "tag_approach",
                "description": "A list of arxiv articles with tags on approach chosen from ['Theoretical Research', "
                               "'Experimental Research', 'Simulation and Modeling', 'Empirical Research',"
                               "'Case Studies','Other'] based on their abstracts",
                "fields": {
                    "title": "The title of the arxiv article,string",
                    "approach": "The approach tag of the arxiv article,string"}
            }
        ])

        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
import chainstream as cs

class TestAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_arxiv_agent")
        self.input_stream = cs.get_stream(self,"all_arxiv")
        self.output_stream = cs.get_stream(self,"tag_approach")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def process_paper(paper):
            paper_title = paper["title"]
            paper_content = paper["abstract"]
            approach_tags = ['Theoretical Research', 'Experimental Research', 'Simulation and Modeling', 'Empirical Research','Case Studies','Other']
            prompt = "Give you an abstract of a paper: {}. What tag would you like to add to this paper? Choose from the following: {}".format(paper_content, ', '.join(approach_tags))
            response = self.llm.query(cs.llm.make_prompt(prompt))
            self.output_stream.add_item({
                    "title":paper_title,
                    "approach":response
                })
        self.input_stream.for_each(process_paper)
        
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'tag_approach')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime):
        sent_paper = []
        for message in self.paper_data:
            self.input_paper_stream.add_item(message)
            sent_paper.append(message)
        return sent_paper
