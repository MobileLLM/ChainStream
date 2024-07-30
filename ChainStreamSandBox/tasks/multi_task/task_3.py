from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class MessageTaskTest2(SingleAgentTaskConfigBase):
    def __init__(self, number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.input_news_stream = None
        self.output_local_stream = None
        self.eos_gap = eos_gap
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_message",
            "description": "All message messages",
            "fields": {
                "sender": "name xxx, string",
                "Content": "text xxx, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_reply_in_office",
                "description": "Replied list of messages,excluding ads when I am in the office",
                "fields": {
                    "content": "xxx, string",
                    "tag": "Received, string"
                }
            }
        ])
        self.news_data = NewsData().get_random_articles(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context.buffer import TextBuffer
class AgentExampleForMessageTask4(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_message_task_4"):
        super().__init__(agent_id)
        self.news_input = cs.get_stream(self, "all_news")
        self.message_buffer = TextBuffer(max_text_num=10000)
        self.output_local_stream = cs.get_stream(self, "summary_output")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def save_message(message):
            self.message_buffer.append(message)
        self.news_input.for_each(save_message)

        def send_msg(stocks):
            stock_list = stocks["item_list"]
            # print(stock)
            messages = self.message_buffer.pop_all()
            # print("messages", messages)
            for message in messages:  
                for stock in stock_list:  
                    print(message["id"],stock["symbol"])
                    self.stock_output.add_item({
                        "stock": stock["symbol"], 
                        "id": message["id"]  
                    })
            return messages

        def extract_type(news):
            news_type = news['category']
            if news_type == "MONEY":
                return news

        self.news_input.for_each(extract_type).batch(by_count=7).for_each(send_msg)
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
        return sent_messages





