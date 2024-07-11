import raw_data
from ..task_config_base import SingleAgentTaskConfigBase
import os
import json
import random
import chainstream as cs
from datetime import datetime
import time
import threading
from ChainStreamSandBox.raw_data import ArxivData
from tqdm import tqdm

random.seed(6666)


class ArxivDateConfig(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_arxiv'. "
            "Process the value corresponding to the 'update_date' key in the paper dictionary: "
            "Add the paper's title followed by the update date to the output stream 'cs_arxiv'."
        )

        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
        import chainstream as cs
        from chainstream.llm import get_model
        class testAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("test_arxiv_agent")
                self.input_stream = cs.get_stream("all_arxiv")
                self.output_stream = cs.get_stream("cs_arxiv")
                self.llm = get_model(["text"])
            def start(self):
                def process_paper(paper):
                    paper_title = paper["title"]
                    paper_date = paper["update_date"]      
                    if paper_date is not None: 
                        self.output_stream.add_item(paper_title+" : "+paper_date)
                self.input_stream.for_each(self, process_paper)
        
            def stop(self):
                self.input_stream.unregister_all(self)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream('all_arxiv')
        self.output_paper_stream = cs.stream.create_stream('cs_arxiv')
        self.clock_stream = cs.stream.create_stream('clock_every_day')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(self, record_output)

    def start_task(self, runtime):
        for message in self.paper_data:
            self.input_paper_stream.add_item(message)


if __name__ == '__main__':
    config = ArxivDateConfig()
