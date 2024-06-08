from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.llm import get_model, make_prompt
from chainstream.context import TextBuffer


class RecommendPaperDaily(Agent):
    def __init__(self):
        super().__init__("Recommend_paper_daily")
        self.clock = get_stream("clock_every_day")
        self.input_stream = get_stream("all_arxiv")
        self.output_stream = create_stream("recommend_paper_daily")
        self.llm = get_model("text")
        self.paper_buffer = TextBuffer()

    def start(self):
        def receive_arxiv(paper):
            self.paper_buffer.add(paper)

        def recommend_paper_daily(new_day):
            prompt = make_prompt(self.paper_buffer, "From the papers received today, please select one that is most relevant to the topic of edge LLM agents and provide a brief summary of it.")
            summary = self.llm.query(prompt)
            self.output_stream.add_item({"summary": summary, "timestamp": new_day})

        self.clock.register_listener(self, recommend_paper_daily)
        self.input_stream.register_listener(self, receive_arxiv)

    def stop(self):
        self.clock.unregister_listener(self)
        self.input_stream.unregister_listener(self)