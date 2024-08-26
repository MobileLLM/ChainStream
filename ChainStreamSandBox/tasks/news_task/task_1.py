from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class NewsTask1(SingleAgentTaskConfigBase):
    def __init__(self, news_number=30):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_news_stream = None
        self.input_news_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Daily_information,
                                scene=Scene_Task_tag.Other, modality=Modality_Task_tag.Text)
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
                "stream_id": "summary_from_dialogue",
                "description": "A summary of the dialogues in conference from the politics news with the date (every "
                               "two pieces of news are packaged as a batch after filtering the politics topic)",
                "fields": {
                    "conference_date": "the date of the conference in the news, string",
                    "summary": "the summary of the dialogues in conference from the news, string"
                }
            }
        ])

        self.news_data = NewsData().get_random_articles(news_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForNewsTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_news_task_1"):
        super().__init__(agent_id)
        self.news_input = cs.get_stream(self, "all_news")
        self.news_output = cs.get_stream(self, "summary_from_dialogue")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_politics(news):
            news_type = news['category']
            if news_type == "POLITICS":
                return news

        def sum_by_dialogues(news_list):
            news_list = news_list['item_list']
            for news in news_list:
                date = news.get('date')
                prompt = "Summarize the main idea of the dialogues in the conference"
                descriptions = [x.get('short_description', '') for x in news_list]
                res = self.llm.query(cs.llm.make_prompt(descriptions, prompt))
                self.news_output.add_item({
                    "conference_date": date,
                    "summary": res
                })

        self.news_input.for_each(filter_politics).batch(by_count=2).for_each(sum_by_dialogues)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')
        self.output_news_stream = cs.stream.create_stream(self, 'summary_from_dialogue')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['summary_from_dialogue'].append(data)

        self.output_news_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_news = {'all_news': []}
        for news in self.news_data:
            sent_news['all_news'].append(news)
            self.input_news_stream.add_item(news)
        return sent_news
