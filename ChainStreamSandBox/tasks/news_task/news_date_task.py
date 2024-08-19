from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class OldNewsTask3(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_news_stream = None
        self.input_news_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Daily_information,
                                scene=Scene_Task_tag.Other, modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_news",
            "description": "A list of news information",
            "fields": {
                "headline": "The headline of the news,string",
                "authors": "The authors of the news,string",
                "category": "The category of the news,string",
                "date": "The release date of the news,string",
                "short_description": "The short description of the news,string",
                "link": "The website link of the news,string",
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "news_date",
                "description": "A list of the release date of the news",
                "fields": {
                    "headline": "The headline of the news,string",
                    "date": "The release date of the news,string"
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
        self.output_stream = cs.get_stream(self,"news_date")
        self.llm = get_model("Text")
    def start(self):
        def process_news(news):
            news_headline = news["headline"]
            news_date = news["date"]           
            self.output_stream.add_item({
            "headline":news_headline,
            "date":news_date})
        self.input_stream.for_each(process_news)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')
        self.output_news_stream = cs.stream.create_stream(self, 'news_date')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['news_date'].append(data)

        self.output_news_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        news_dict = {'all_news': []}
        for message in self.news_data:
            self.input_news_stream.add_item(message)
            news_dict['all_news'].append(message)
        return news_dict
