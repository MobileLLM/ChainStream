if __name__ == "__main__":
    from tasks import ALL_TASKS

    ArxivTaskConfig = ALL_TASKS['ArxivTask']

    agent_file = '''
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
                algorithms_tags = ['Deep Learning', 'Machine Learning', 'Classical', 'Heuristic','Evolutionary','Other']
                prompt = "Give you an abstract of a paper: {}. What tag would you like to add to this paper? Choose from the following: {}".format(paper_content, ', '.join(algorithms_tags))
                prompt_message = [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
                response = self.llm.query(prompt_message)
                print(paper_title+" : "+response)
                self.output_stream.add_item(paper_title+" : "+response)

        self.input_stream.register_listener(self, process_paper)

    def stop(self):
        self.input_stream.unregister_listener(self)
'''
    oj = OJ(ArxivTaskConfig(), agent_file)
    oj.start_test_agent()

