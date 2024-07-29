from tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData


class NewsLinkConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_news_stream = None
        self.input_news_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_news' and process the values corresponding to the 'headline' and 'link' keys in the news dictionary: "
            "Add the news headline followed by its link to the output stream 'cs_news'."
        )

        self.news_data = NewsData().get_random_articles(10)
        self.agent_example = '''
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
                    news_link = news["link"]           
                    #print(news_category)
                    self.output_stream.add_item(news_headline+" : "+news_link)
                self.input_stream.for_each(self, process_news)
        
            def stop(self):
                self.input_stream.unregister_all(self)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream('all_news')
        self.output_news_stream = cs.stream.create_stream('cs_news')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_news_stream.for_each(self, record_output)

    def start_task(self, runtime):
        for message in self.news_data:
            self.input_news_stream.add_item(message)


if __name__ == '__main__':
    config = NewsLinkConfig()
