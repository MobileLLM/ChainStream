from tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData

random.seed(6666)


class ArxivAbstractConfig(SingleAgentTaskConfigBase):
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
        from chainstream.llm import get_model
        class testAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("test_arxiv_agent")
                self.input_stream = cs.get_stream("all_arxiv")
                self.output_stream = cs.get_stream("cs_arxiv")
                self.llm = get_model(["text"])
            def start(self):
                def process_paper(paper):
                    paper_content = paper["abstract"]     
                    prompt = "Is this abstract related to edge LLM agent? Say 'yes' or 'no'."
                    prompt = [
                        {
                            "role": "user",
                            "content": prompt+paper_content
                        }
                    ]
                    response = self.llm.query(prompt)
                    print(response)
                    if response == 'Yes':
                        self.output_stream.add_item(paper)
                self.input_stream.for_each(self, process_paper)
        
            def stop(self):
                self.input_stream.unregister_all(self)

        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream('all_arxiv')
        self.output_paper_stream = cs.stream.create_stream('cs_arxiv')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(self, record_output)

    def start_task(self, runtime):
        for message in self.paper_data:
            self.input_paper_stream.add_item(message)


if __name__ == '__main__':
    config = ArxivAbstractConfig()
