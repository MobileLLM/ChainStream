from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SMSData
from ChainStreamSandBox.raw_data import StockData
from AgentGenerator.io_model import StreamListDescription
import time

random.seed(6666)


class MessageStockTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.input_message_stream = None
        self.input_stock_stream = None
        self.stock_message_output = None
        self.input_stream_description1 = StreamListDescription(streams=[{
            "stream_id": "all_message",
            "description": "All message information",
            "fields": {
                "sender": "the name of the message sender, string",
                "Content": "the content of the message, string",
                "id": "the id of the message sender, int"
            }
        }, {
            "stream_id": "all_stock",
            "description": "All stock messages",
            "fields": {
                "open": "the opening price of the stock, float",
                "close": "the closing price of the stock, float",
                "symbol": "the symbol of the stock,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "stock_output",
                "description": "A list of messages to remind all the buyers when the stock plummeted",
                "fields": {
                    "stock": "the symbol of the stock, string",
                    "id": "the ids of all the stock buyers, int"
                }
            }
        ])
        self.stock_data = StockData().get_stocks(number)
        self.message_data = SMSData().get_random_message('zh')
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask2(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task_2"):
        super().__init__(agent_id)
        self.message_input = cs.get_stream(self, "all_message")
        self.stock_input = cs.get_stream(self, "all_stock")
        self.stock_output = cs.get_stream(self, "stock_output")
        self.message_buffer = Buffer()
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def save_message(message):
            self.message_buffer.append(message)
        self.message_input.for_each(save_message)

        def send_msg(stocks):
            stock_list = stocks["item_list"]
            messages = self.message_buffer.pop_all()
            for message in messages:  
                for stock in stock_list:  
                    self.stock_output.add_item({
                        "stock": stock["symbol"], 
                        "id": message["id"]  
                    })
            return messages
        def analysis_stock(stock):
            open_price = stock['open']
            close_price = stock['close']
            if open_price != 0:
                change_percentage = (close_price - open_price) / open_price * 100
                if change_percentage < 0:
                    return stock
        def example_func(item, kwargs):
            buffer = kwargs.get('buffer', Buffer())
            kwargs['buffer'] = buffer
            if len(buffer) < 2:
                buffer.append(item)
                return None, kwargs
            else:
                buffer.append(item)
                all_items = buffer.pop_all()
                return {"item_list": all_items}, kwargs    
        self.stock_input.for_each(analysis_stock).batch(by_func=example_func).for_each(send_msg)
        '''

    def init_environment(self, runtime):
        self.input_stock_stream = cs.stream.create_stream(self, 'all_stock')
        self.input_message_stream = cs.stream.create_stream(self, 'all_message')
        self.stock_message_output = cs.stream.create_stream(self, 'stock_output')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.stock_message_output.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.message_data:
            sent_messages.append(message)
            self.input_message_stream.add_item(message)
            time.sleep(1)
        for stock in self.stock_data:
            sent_messages.append(stock)
            self.input_stock_stream.add_item(stock)
            time.sleep(1)
        return sent_messages
