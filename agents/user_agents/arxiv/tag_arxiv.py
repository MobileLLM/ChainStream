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
            approch_tags = ['Theoretical Research', 'Experimental Research', 'Simulation and Modeling', 'Empirical Research','Case Studies','Other']
            problems_tags = ['Optimization', 'Classification', 'Regression', 'Clustering', 'Generation','Other']
            implementation_tags = ['Software', 'Hardware', 'Hybrid', 'System Integration','Other']
            algorithms_tags = ['Deep Learning', 'Machine Learning', 'Classical', 'Heuristic','Evolutionary','Other']
            stage_tags = ['Conceptual', 'Development', 'Testing', 'Deployment', 'Maintenance','Other']

            prompt_topic = base_tag_prompt + ", ".join(topic_tags)
            prompt_approch = base_tag_prompt + ", ".join(approch_tags)
            prompt_problems = base_tag_prompt + ", ".join(problems_tags)
            prompt_implementation = base_tag_prompt + ", ".join(implementation_tags)
            prompt_algorithms = base_tag_prompt + ", ".join(algorithms_tags)
            prompt_stage = base_tag_prompt + ", ".join(stage_tags)

            topic_tag = self.llm.query(prompt_topic)
            approch_tag = self.llm.query(prompt_approch)
            problems_tag = self.llm.query(prompt_problems)
            implementation_tag = self.llm.query(prompt_implementation)
            algorithms_tag = self.llm.query(prompt_algorithms)
            stage_tag = self.llm.query(prompt_stage)

            new_paper = paper.copy()
            new_paper["tags"] = {"topic": topic_tag,
                                "approach": approch_tag,
                                "problems": problems_tag,
                                "implementation": implementation_tag,
                                "algorithms": algorithms_tag,
                                "stage": stage_tag}
            self.paper_to.send(new_paper)

        self.paper_from.register_listener(self, tag_arxiv)

    def stop(self):
        self.paper_to.unregister_listener(self)