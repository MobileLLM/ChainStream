from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class ArxivTask2(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_arxiv_with_EOS_tag",
            "description": "All arxiv paper, xxx which is a dict like `{\"EOS\":\"This is an end tag\"}",
            "fields": {
                "title": "the title of each arxiv article, string",
                "abstract": "the abstract of each arxiv article, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "arxiv_research_method",
                "description": "A list of research methods for arxiv articles on math topics",
                "fields": {
                    "abstract": "the abstract of each arxiv article on math topic, string",
                    "method": "the research method of each arxiv article on math topic, string"
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
            prompt = "Summarize the research method of the papers here"
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

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.paper_data:
            sent_messages.append(message)
            self.input_paper_stream.add_item(message)
        return sent_messages





