from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class NewsTask4(SingleAgentTaskConfigBase):
    def __init__(self, news_number=50):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_news_stream = None
        self.input_news_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard, domain=Domain_Task_tag.Daily_information,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_news",
            "description": "All news items",
            "fields": {
                "category": "the category of the news, string",
                "link": "the website link that presents the news, string",
                "short_description": "the short description of the news, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "extract_entertainment_news_website",
                "description": "A stream of website links and their short descriptions, filtered by the "
                               "'ENTERTAINMENT' category from the 'category' field, with every two pieces of news "
                               "packaged together in a batch after filtering by the entertainment topic",
                "fields": {
                    "short_description": "the short description of the 'ENTERTAINMENT' news, string",
                    "link": "the website link that presents the specific 'ENTERTAINMENT' news, string"
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
        self.news_output = cs.create_stream(self, "extract_entertainment_news_website")
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
                    "short_description": description,
                    "link": link
                })

        self.news_input.for_each(filter_news).batch(by_count=2).for_each(extract_website)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')
        self.output_news_stream = cs.stream.create_stream(self, 'extract_entertainment_news_website')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['extract_entertainment_news_website'].append(data)

        self.output_news_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')

    def init_output_stream(self, runtime):
        self.output_news_stream = cs.stream.get_stream(self, 'extract_entertainment_news_website')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['extract_entertainment_news_website'].append(data)

        self.output_news_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_news = {'all_news': []}
        for news in self.news_data:
            sent_news['all_news'].append(news)
            self.input_news_stream.add_item(news)
        return sent_news
