from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class NewsTask3(SingleAgentTaskConfigBase):
    def __init__(self, news_number=30, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_news_stream = None
        self.input_news_stream = None

        self.eos_gap = eos_gap
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_news",
            "description": "All news messages",
            "fields": {
                "category": "name xxx, string",
                "date": "date xxx, string",
                "headline":"text xxx, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "USA_news_tags",
                "description": "A extraction of the news happened in America in July this year,and tell me the "
                               "headline and the category of them",
                "fields": {
                    "headline": "xxx, string",
                    "tag": "xxx, string"
                }
            }
        ])

        self.news_data = NewsData().get_random_articles(news_number)
        self.agent_example = '''
import chainstream as cs
class AgentExampleForNewsTask3(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_news_task_3"):
        super().__init__(agent_id)
        self.news_input = cs.get_stream(self, "all_news")
        self.news_output = cs.get_stream(self, "USA_news_tags")
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
            # prompt = "Extract the main characters of the news"
            # descriptions = [x.get('short_description', '') for x in news_list]
            # print("extract_from_dialogues: query", descriptions, prompt)
            # res = self.llm.query(cs.llm.make_prompt(descriptions, prompt))
            # print("extract_from_dialogues", res)
                self.news_output.add_item({
                    "headline": headline,
                    "tag": tag
                })

        self.news_input.for_each(filter_month).batch(by_count=2).for_each(tag_news)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')
        self.output_news_stream = cs.stream.create_stream(self, 'USA_news_tags')

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





