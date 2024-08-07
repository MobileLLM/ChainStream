from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription
import time

random.seed(6666)


class StoreOpinionTest(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.input_news_stream = None
        self.output_local_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_news",
            "description": "All news items",
            "fields": {
                "category": "the category of the news, string",
                "short_description": "the short description of the news, string",
                "headline": "the headline of the news event, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "summary_output",
                "description": "A list of the summary of the CEOs' opinions on Techtronic",
                "fields": {
                    "news": "the headline of the news event, string",
                    "summary": "the summary of the CEOs' opinions on Techtronic, string"
                }
            }
        ])
        self.news_data = NewsData().get_random_articles(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask3(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task_3"):
        super().__init__(agent_id)
        self.news_input = cs.get_stream(self, "all_news")
        self.message_buffer = Buffer()
        self.output_local_stream = cs.get_stream(self, "summary_output")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def summary_description(news):
            news_list = news["item_list"]
            for news in news_list:
                title = news["headline"]
                prompt = "Summarize the opinions of the CEO in the news"
                res = self.llm.query(cs.llm.make_prompt(news['short_description'], prompt))
                self.output_local_stream.add_item({
                    "news": title,
                    "summary": res
                })
            return messages

        def extract_type(news):
            news_type = news['category']
            if news_type == "Techtronic":
                return news

        self.news_input.for_each(extract_type).batch(by_time=1).for_each(summary_description)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')
        self.output_local_stream = cs.stream.create_stream(self, 'summary_output')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_local_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.news_data:
            sent_messages.append(message)
            self.input_news_stream.add_item(message)
            time.sleep(3)
        return sent_messages
