from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.llm import get_model


class TagArxiv(Agent):
    """
    Agent to tag arxiv paper with several different tag types.

    """

    def __init__(self):
        super().__init__("tag_arxiv_agent")
        self.paper_from = get_stream("all_arxiv")
        self.paper_to = create_stream("all_arxiv_tagged")
        self.llm = get_model("text")

    def start(self):
        def tag_arxiv(paper):
            paper_content = paper["abstract"]
            base_tag_prompt = ("Give you an abstract of a paper: %s . What tag would you like to add to this paper? Choose from "
                               "the following: ") % paper_content
            topic_tags = ['Artificial Intelligence', 'Computer Vision and Pattern Recognition', 'Machine Learning', 'Neural and Evolutionary Computing', 'Robotics', 'Graphics', 'Human-Computer Interaction', 'Multiagent Systems', 'Software Engineering','Other']

            prompt_topic = base_tag_prompt + ", ".join(topic_tags)

            topic_tag = self.llm.query(prompt_topic)

            new_paper = paper.copy()
            new_paper["tags"] = {"topic": topic_tag,}
            self.paper_to.send(new_paper)

        self.paper_from.for_each(self, tag_arxiv)

    def stop(self):
        self.paper_to.unregister_all(self)