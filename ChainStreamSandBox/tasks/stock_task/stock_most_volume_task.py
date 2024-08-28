from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import StockData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class StockTask2(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_stock_stream = None
        self.input_stock_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Daily_information,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_stocks",
            "description": "A series of stock information (every ten stock information are packaged as a batch)",
            "fields": {
                "symbol": "The symbol of the stock, string",
                "volume": "The trading volume of the stock, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "top_five_volume_stock",
                "description": "A series of the filtered stocks with top five trading volume",
                "fields": {
                    "symbol": "The symbol of the stock, string",
                    "volume": "The trading volume of the stock, float"
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
        self.output_stream = cs.get_stream(self,"top_five_volume_stock")
        self.llm = get_model("Text")
    def start(self):
        def process_stocks(stock_dict):
            stocks = stock_dict['item_list']
            sorted_stocks = sorted(stocks, key=lambda x: int(x['volume']), reverse=True)
            top_5_dicts = sorted_stocks[:5]
            for stock in top_5_dicts:
                volume = stock['volume']
                stock_symbol = stock['symbol']
                self.output_stream.add_item({
                "symbol": stock_symbol,
                "volume": volume
                })
        self.input_stream.batch(by_count=10).for_each(process_stocks)
        '''

    def init_environment(self, runtime):
        self.input_stock_stream = cs.stream.create_stream(self, 'all_stocks')
        self.output_stock_stream = cs.stream.create_stream(self, 'top_five_volume_stock')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['top_five_volume_stock'].append(data)

        self.output_stock_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_stock_stream = cs.stream.create_stream(self, 'all_stocks')

    def init_output_stream(self, runtime):
        self.output_stock_stream = cs.stream.get_stream(self, 'top_five_volume_stock')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['top_five_volume_stock'].append(data)

        self.output_stock_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        stock_dict = {'all_stocks': []}
        for stock in self.stock_data:
            self.input_stock_stream.add_item(stock)
            stock_dict['all_stocks'].append(stock)
        return stock_dict
