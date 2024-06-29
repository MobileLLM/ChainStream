from ..task_config_base import TaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData


class NewsDescriptionConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_news_stream = None
        self.input_news_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_news' and process the values corresponding to the 'headline' and 'short_description' keys in the news dictionary: "
            "Add the news headline followed by its short description to the output stream 'cs_news'."
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
                    news_short_description = news["short_description"]           
                    self.output_stream.add_item(news_headline+" : "+news_short_description)
                self.input_stream.register_listener(self, process_news)
        
            def stop(self):
                self.input_stream.unregister_listener(self)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream('all_news')
        self.output_news_stream = cs.stream.create_stream('cs_news')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_news_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for message in self.news_data:
            self.input_news_stream.add_item(message)

    def record_output(self, runtime):
        print(self.output_record)
        if len(self.output_record) == 0:
            return False, "No news messages found"
        else:
            return True, self.output_record


if __name__ == '__main__':
    config = NewsDescriptionConfig()
