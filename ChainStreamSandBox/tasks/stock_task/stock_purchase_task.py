from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import StockData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class StockTask3(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_stock_stream = None
        self.input_stock_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Daily_information,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_stocks",
            "description": "A stream of stock information",
            "fields": {
                "open": "The open price of the stock, float",
                "close": "The close price of the price, float",
                "high": "The highest price of the stock, float",
                "low": "The lowest price of the stock, float",
                "symbol": "The symbol of the stock, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "recommendation_buy_stock",
                "description": "A stream of the recommendations for stock purchases based on the open,close,high and "
                               "low price",
                "fields": {
                    "buy": "Decision on whether to buy the stock or not, string = yes or no",
                    "symbol": "The symbol of the stock, string"
                }
            }
        ])
        self.stock_data = StockData().get_stocks(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_news_agent")
        self.input_stream = cs.get_stream(self,"all_stocks")
        self.output_stream = cs.get_stream(self,"recommendation_buy_stock")
        self.llm = get_model("Text")
    def start(self):
        def process_stocks(stock):
            open_price = stock["open"]
            close_price = stock["close"]
            high_price = stock["high"]
            low_price = stock["low"]
            stock_symbol = stock["symbol"]
            stock_text =f"Open Price: {open_price},Close Price: {close_price},High Price: {high_price},Low Price: {low_price}"
            prompt = f"Based on the following stock information: {stock_text}, recommend whether to buy the stock or not.Just tell me y or n."
            response = self.llm.query(cs.llm.make_prompt(prompt))
            if response.lower() == "y":
                self.output_stream.add_item({
                "buy": "yes",
                "symbol": stock_symbol
                })
            else:
                self.output_stream.add_item({
                "buy": "no", 
                "symbol": stock_symbol
                })
            return stock
        self.input_stream.for_each(process_stocks)
        '''

    def init_environment(self, runtime):
        self.input_stock_stream = cs.stream.create_stream(self, 'all_stocks')
        self.output_stock_stream = cs.stream.create_stream(self, 'recommendation_buy_stock')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['recommendation_buy_stock'].append(data)

        self.output_stock_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_stock_stream = cs.stream.create_stream(self, 'all_stocks')

    def init_output_stream(self, runtime):
        self.output_stock_stream = cs.stream.get_stream(self, 'recommendation_buy_stock')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['recommendation_buy_stock'].append(data)

        self.output_stock_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        stock_dict = {'all_stocks': []}
        for stock in self.stock_data:
            self.input_stock_stream.add_item(stock)
            stock_dict['all_stocks'].append(stock)
        return stock_dict
