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
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard, domain=Domain_Task_tag.Office,
                                modality=Modality_Task_tag.Text)
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
                "description": "A stream of main ideas from arxiv articles written by Victor Brunton, with articles "
                               "filtered for the author Victor Brunton first, then packaged into batches of every "
                               "three articles, and finally summarized by the abstracts.",
                "fields": {
                    "title": "the title of each arxiv article, string",
                    "main_idea": "main ideas of the arxiv articles written by Victor Brunton and summarized by the "
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
        self.arxiv_output = cs.create_stream(self, "main_idea_by_Victor_Brunton")
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
                    "title": title,
                    "main_idea": res
                })
        self.arxiv_input.for_each(filter_authors).batch(by_count=3).for_each(sum_on_paper)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'main_idea_by_Victor_Brunton')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['main_idea_by_Victor_Brunton'].append(data)

        self.output_paper_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')

    def init_output_stream(self, runtime):
        self.output_paper_stream = cs.stream.get_stream(self, 'main_idea_by_Victor_Brunton')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['main_idea_by_Victor_Brunton'].append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        data = [
            {
                "authors": "Victor Brunton",
                "title": "Advanced Data Analysis Techniques",
                "abstract": "This article explores advanced techniques in data analysis, including machine learning algorithms and statistical methods. We provide case studies to illustrate practical applications in various fields.",
                "comments": "Preliminary findings; further research needed.",
                "journal-ref": "Journal of Data Science, Vol. 12, pp. 45-60, 2023",
                "license": "http://example.org/licenses/creative-commons/1.0/",
                "versions": "[{'version': 'v1', 'created': 'Mon, 01 Feb 2023 09:00:00 GMT'}]",
                "update_date": "2023-02-01"
            },
            {
                "authors": "Victor Brunton, Alice Smith",
                "title": "Data Visualization Techniques",
                "abstract": "This paper discusses various techniques for effective data visualization, focusing on interactive and dynamic visualizations. Examples from recent projects are included to demonstrate the impact of visualization on data interpretation.",
                "comments": "Draft version; to be updated with new examples.",
                "journal-ref": "Data Science and Analytics, Vol. 8, pp. 101-115, 2022",
                "license": "http://example.org/licenses/nonexclusive-distrib/1.0/",
                "versions": "[{'version': 'v1', 'created': 'Tue, 15 Nov 2022 10:30:00 GMT'}]",
                "update_date": "2022-11-15"
            },
            {
                "authors": "Victor Brunton, John Doe",
                "title": "Machine Learning in Healthcare",
                "abstract": "The article reviews the application of machine learning techniques in the healthcare industry, covering both current trends and future potential. Case studies from various healthcare settings are analyzed.",
                "comments": "For review; suggestions welcomed.",
                "journal-ref": "Healthcare Technology Review, Vol. 6, pp. 78-89, 2024",
                "license": "http://example.org/licenses/public-domain/1.0/",
                "versions": "[{'version': 'v1', 'created': 'Wed, 05 Jun 2024 14:45:00 GMT'}]",
                "update_date": "2024-06-05"
            }
        ]
        self.paper_data.extend(data)
        sent_papers = {'all_arxiv': []}
        for paper in self.paper_data:
            sent_papers['all_arxiv'].append(paper)
            self.input_paper_stream.add_item(paper)
        return sent_papers
