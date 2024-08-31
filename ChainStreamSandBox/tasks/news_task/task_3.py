from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class NewsTask3(SingleAgentTaskConfigBase):
    def __init__(self, news_number=30):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_news_stream = None
        self.input_news_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard, domain=Domain_Task_tag.Daily_information,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_USA_news",
            "description": "All news items",
            "fields": {
                "category": "the category of the news, string",
                "date": "ISO 8601 datetime format, datetime",
                "headline": "the headline of the news event, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "USA_news_in_July",
                "description": "A stream of the extraction of the USA news in July with the headline and the category "
                               "of them, with every two pieces of news are packaged as a batch after filtering the "
                               "USA news happened in July",
                "fields": {
                    "headline": "the headline of the news event, string",
                    "category": "the category of the news, string"
                }
            }
        ])

        self.news_data = NewsData().get_random_articles(news_number)
        self.agent_example = '''
import chainstream as cs
class AgentExampleForNewsTask3(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_news_task_3"):
        super().__init__(agent_id)
        self.news_input = cs.get_stream(self, "all_USA_news")
        self.news_output = cs.create_stream(self, "USA_news_in_July")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_month(news):
            date_str = news.get('date')
            if not date_str or len(date_str) < 7:
                return None            
            month = date_str[5:7]
            if month == "07":
                return news
            return None

        def tag_news(news_list):
            news_list = news_list['item_list']
            for news in news_list:
                tag = news.get('category')
                headline = news.get('headline')
                self.news_output.add_item({
                    "headline": headline,
                    "category": tag
                })

        self.news_input.for_each(filter_month).batch(by_count=2).for_each(tag_news)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_USA_news')
        self.output_news_stream = cs.stream.create_stream(self, 'USA_news_in_July')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['USA_news_in_July'].append(data)

        self.output_news_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_USA_news')

    def init_output_stream(self, runtime):
        self.output_news_stream = cs.stream.get_stream(self, 'USA_news_in_July')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['USA_news_in_July'].append(data)

        self.output_news_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_news = {'all_USA_news': []}
        for news in self.news_data:
            sent_news['all_USA_news'].append(news)
            self.input_news_stream.add_item(news)
        return sent_news
