import raw_data
from tasks.task_config_base import SingleAgentTaskConfigBase
import os
import json
import random
import chainstream as cs
from datetime import datetime
import time
import threading
from ChainStreamSandBox.raw_data import ArxivData

random.seed(6666)


class ArxivStageConfig(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_arxiv'. "
            "Process the value corresponding to the 'abstract' key and the 'versions' key in the paper dictionary: "
            "Assign a stage tag from the predefined list ('Conceptual', 'Development', 'Testing', 'Deployment', 'Maintenance', 'Other') to the paper's abstract and version using an LLM. "
            "Add the paper's title followed by the assigned tag to the output stream 'cs_arxiv'."
        )

        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
        import chainstream as cs
        from chainstream.llm import get_model
        
        class TestAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("test_arxiv_agent")
                self.input_stream = cs.get_stream("all_arxiv")
                self.output_stream = cs.get_stream("cs_arxiv")
                self.llm = get_model(["text"])
        
            def start(self):
                def process_paper(paper):
                    if "abstract" in paper:
                        paper_title = paper["title"]
                        paper_content = paper["abstract"]
                        paper_versions = paper["versions"]
                        stage_tags = ['Conceptual', 'Development', 'Testing', 'Deployment', 'Maintenance','Other']
                        prompt = "Give you an abstract of a paper: {} and the version of this paper:{}. What tag would you like to add to this paper? Choose from the following: {}".format(paper_content,paper_versions, ', '.join(stage_tags))
                        prompt_message = [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                        response = self.llm.query(prompt_message)
                        print(paper_title+" : "+response)
                        self.output_stream.add_item(paper_title+" : "+response)
        
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
    config = ArxivStageConfig()
