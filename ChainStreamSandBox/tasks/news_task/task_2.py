from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class NewsTask2(SingleAgentTaskConfigBase):
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
                "date": "ISO 8601 datetime format, string",
                "short_description": "the short description of the news, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "extract_characters",
                "description": "An extraction of the characters from the politics news with the date, with every two "
                               "pieces of news packaged as a batch after filtering the politics topic",
                "fields": {
                    "characters": "the characters extracted from the political news, string",
                    "date": "the date of the political news, string"
                }
            }
        ])

        self.news_data = NewsData().get_random_articles(news_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForNewsTask2(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_news_task_2"):
        super().__init__(agent_id)
        self.news_input = cs.get_stream(self, "all_news")
        self.news_output = cs.create_stream(self, "extract_characters")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_news(news):
            news_type = news['category']
            if news_type == "POLITICS":
                return news

        def extract_from_dialogues(news_list):
            news_list = news_list['item_list']
            for news in news_list:
                date = news.get('date')
                prompt = "Extract the main characters of the news"
                description = news['short_description']
                res = self.llm.query(cs.llm.make_prompt(description, prompt))
                self.news_output.add_item({
                    "characters": res,
                    "date": date
                })

        self.news_input.for_each(filter_news).batch(by_count=2).for_each(extract_from_dialogues)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')
        self.output_news_stream = cs.stream.create_stream(self, 'extract_characters')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['extract_characters'].append(data)

        self.output_news_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')

    def init_output_stream(self, runtime):
        self.output_news_stream = cs.stream.get_stream(self, 'extract_characters')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['extract_characters'].append(data)

        self.output_news_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_news = {'all_news': []}
        for news in self.news_data:
            sent_news['all_news'].append(news)
            self.input_news_stream.add_item(news)
        return sent_news
