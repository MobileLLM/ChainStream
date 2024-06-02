if __name__ == "__main__":
    from tasks import ALL_TASKS

    ArxivTaskConfig = ALL_TASKS['ArxivTask']

    agent_file = '''
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
        self.input_stream.register_listener(self, process_paper)

    def stop(self):
        self.input_stream.unregister_listener(self)

    '''
    oj = OJ(ArxivTaskConfig(), agent_file)
    oj.start_test_agent()