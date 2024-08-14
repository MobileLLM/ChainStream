from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData

random.seed(6666)


class OldArxivTask1(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
        self.task_description = (
            "Retrieve data from the input stream all_arxiv, and process the value corresponding to the 'abstract' key "
            "in the paper dictionary: Extract the abstract content and judge whether the abstract is related to 'edge "
            "LLM agent'. If the response is 'Yes', add the paper to the output stream cs_arxiv"
        )

        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
import chainstream as cs
class testAgent(cs.agent.Agent):
    def __init__(self,agent_id ="test_arxiv_agent"):
        super().__init__(agent_id)
        self.input_stream = cs.get_stream(self,"all_arxiv")
        self.output_stream = cs.get_stream(self,"cs_arxiv")
        self.llm = cs.llm.get_model("Text")
    def start(self):
        def process_paper(paper):
            paper_content = paper["abstract"]     
            prompt = "Is this abstract related to edge LLM agent? Say 'yes' or 'no'."
            response = self.llm.query(cs.llm.make_prompt(paper_content, prompt))
            if response == 'Yes':
                self.output_stream.add_item(paper)
            return paper
        self.input_stream.for_each(process_paper)
    

        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_paper_stream = cs.stream.create_stream(self, 'cs_arxiv')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_paper = []
        for message in self.paper_data:
            self.input_paper_stream.add_item(message)
            sent_paper.append(message)
        return sent_paper

