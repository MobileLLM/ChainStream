from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class NewsTask6(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_news_stream = None
        self.input_news_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Daily_information,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_news",
            "description": "A series of news information",
            "fields": {
                "headline": "The headline of the news, string",
                "authors": "The authors of the news, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "news_authors",
                "description": "A series of the authors of the news",
                "fields": {
                    "headline": "The headline of the news, string",
                    "authors": "The authors of the news, string"
                }
            }
        ])
        self.news_data = NewsData().get_random_articles(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_news_agent")
        self.input_stream = cs.get_stream(self,"all_news")
        self.output_stream = cs.get_stream(self,"news_authors")
        self.llm = get_model("Text")
    def start(self):
        def process_news(news):
            news_headline = news["headline"]
            news_authors = news["authors"]           
            self.output_stream.add_item({
            "headline": news_headline,
            "authors": news_authors})
        self.input_stream.for_each(process_news)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')
        self.output_news_stream = cs.stream.create_stream(self, 'news_authors')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['news_authors'].append(data)

        self.output_news_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        news_dict = {'all_news': []}
        for message in self.news_data:
            self.input_news_stream.add_item(message)
            news_dict['all_news'].append(message)
        return news_dict
