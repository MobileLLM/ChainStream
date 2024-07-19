from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class NewsTask4(SingleAgentTaskConfigBase):
    def __init__(self, news_number=50, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_news_stream = None
        self.input_news_stream = None

        self.eos_gap = eos_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "extract_characters",
                "description": "An extraction of the website link from the entertainment news",
                "fields": {
                    "description": "xxx, string",
                    "link": "xxx, string"
                }
            }
        ])

        self.news_data = NewsData().get_random_articles(news_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForNewsTask4(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_news_task_4"):
        super().__init__(agent_id)
        self.news_input = cs.get_stream(self, "all_news")
        self.news_output = cs.get_stream(self, "extract_website")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_news(news):
            news_type = news['category']
            if news_type == "ENTERTAINMENT":
                return news

        def extract_website(news_list):
            news_list = news_list['item_list']
            for news in news_list:
                link = news.get('link')
                description = news.get('short_description')
                self.news_output.add_item({
                    "description": description,
                    "link": link
                })

        self.news_input.for_each(filter_news).batch(by_count=2).for_each(extract_website)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')
        self.output_news_stream = cs.stream.create_stream(self, 'extract_website')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_news_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.news_data:
            sent_messages.append(message)
            self.input_news_stream.add_item(message)
        return sent_messages





