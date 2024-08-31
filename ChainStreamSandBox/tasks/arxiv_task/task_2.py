from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class ArxivTask2(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Office,
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
                "stream_id": "arxiv_research_method",
                "description": "A stream of research methods for arxiv articles on the math topic, with articles "
                               "filtered for the math topic first, then packaged into batches of every two articles, "
                               "and finally summarized.",
                "fields": {
                    "title": "the title of each arxiv article on math topic, string",
                    "method": "the research method of each arxiv article on math topic chosen from ['Experimental "
                              "Evaluation', 'Theoretical Research', 'System Implementation', 'Data Analysis and "
                              "Mining', 'Simulation and Modeling', 'User Study', 'Literature Review'] based on "
                              "the abstract, string "
                }
            }
        ])

        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForArxivTask2(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_arxiv_task_2"):
        super().__init__(agent_id)
        self.arxiv_input = cs.get_stream(self, "all_arxiv")
        self.arxiv_output = cs.get_stream(self, "arxiv_research_method")

        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_topic(paper):
            prompt = "Is this paper on math? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(paper['title'], prompt))
            if res.lower() == 'y':
                return paper

        def sum_on_paper(paper):
            paper_list = paper['item_list']
            prompt = "Summarize the research method of the papers chosen from ['Experimental Evaluation', 'Theoretical Research', 'System Implementation', 'Data Analysis and Mining', 'Simulation and Modeling', 'User Study', 'Literature Review'].Only give me the choice."
            for paper_item in paper_list:
                title = paper_item.get('title', 'No Title')  
                abstract = paper_item.get('abstract', '')  
                res = self.llm.query(cs.llm.make_prompt(abstract, prompt))
                self.arxiv_output.add_item({
                    "title": title,
                    "method": res
                })
        self.arxiv_input.for_each(filter_topic).batch(by_count=2).for_each(sum_on_paper)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'arxiv_research_method')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['arxiv_research_method'].append(data)

        self.output_paper_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')

    def init_output_stream(self, runtime):
        self.output_paper_stream = cs.stream.get_stream(self, 'arxiv_research_method')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['arxiv_research_method'].append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_papers = {'all_arxiv': []}
        for paper in self.paper_data:
            sent_papers['all_arxiv'].append(paper)
            self.input_paper_stream.add_item(paper)
        return sent_papers
