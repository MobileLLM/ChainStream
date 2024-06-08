from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.llm import get_model


class Arxiv_Edge_LLM_Agent_Filter(Agent):
    def __init__(self):
        super(Arxiv_Edge_LLM_Agent_Filter, self).__init__("Arxiv_Edge_LLM_Agent_Filter")
        self.paper_from = get_stream("all_arxiv")
        self.llm_paper = create_stream("llm_paper")
        self.llm = get_model("text")

    def start(self):
        def filter_arxiv(paper):
            paper_content = paper["abstract"]
            prompt = "Is this abstract related to edge LLM agent? Say 'yes' or 'no'."
            response = self.llm.generate(prompt, paper_content)
            if response.lower() == "yes":
                self.llm_paper.add_item(paper)

        self.paper_from.register_listener(self, filter_arxiv)

    def stop(self):
        self.paper_from.deregister_listener(self)