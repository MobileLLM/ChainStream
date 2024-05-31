if __name__ == "__main__":
    from tasks import ALL_TASKS

    NewsTaskConfig = ALL_TASKS['NewsTask']

    agent_file = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_news_agent")
        self.input_stream = cs.get_stream("all_news")
        self.output_stream = cs.get_stream("cs_news")
        self.llm = get_model(["text"])
    def start(self):
        def process_news(news):
            news_headline = news["headline"]
            news_short_description = news["short_description"]       
            prompt = "Now you have received some news,please tell me the people who involved in the news"          
            prompt = [
                {
                    "role": "user",
                    "content": prompt+news_short_description
                }
            ]
            response = self.llm.query(prompt)
            print(response)
            self.output_stream.add_item(news_headline+" : "+response)
        self.input_stream.register_listener(self, process_news)

    def stop(self):
        self.input_stream.unregister_listener(self)

    '''
    oj = OJ(NewsTaskConfig(), agent_file)
    oj.start_test_agent()