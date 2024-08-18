from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import StockData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class StockTask1(SingleAgentTaskConfigBase):
    def __init__(self, number=200):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_stock_stream = None
        self.input_stock_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_stock",
            "description": "All stock information",
            "fields": {
                "symbol": "the symbol of the stock, string",
                "open": "the opening price of the stock, float",
                "close": "the closing price of the stock, float",
                "volume": "the trading volume of the stock, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "up_or_down",
                "description": "A list of the change percentages with the volume of the MLM stock if it has fallen",
                "fields": {
                    "change_percentage": "The percentage change in the stock price, float",
                    "volume": "the trading volume of the stock, float"
                }
            }
        ])

        self.stock_data = StockData().get_stocks(number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForStockTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_stock_task_1"):
        super().__init__(agent_id)
        self.stock_input = cs.get_stream(self, "all_stock")
        self.stock_output = cs.get_stream(self, "up_or_down")
        self.llm = cs.llm.get_model("Text")

        def filter_mlm_stocks(stock_dict):
            mlm_stocks = [stock for stock in stock_dict if isinstance(stock, dict) and stock.get('symbol') == 'MLM']
            return mlm_stocks
        
        def up_or_down(stock):
            open_price = stock['open']
            close_price = stock['close']
            volume = stock['volume']
            if open_price != 0:
                change_percentage = (close_price - open_price) / open_price * 100
            else:
                change_percentage = 0.0
            self.stock_output.add_item({
                "change_percentage": change_percentage,
                "volume": volume
            }) 

        self.stock_input.for_each(up_or_down)
        '''

    def init_environment(self, runtime):
        self.input_stock_stream = cs.stream.create_stream(self, 'all_stock')
        self.output_stock_stream = cs.stream.create_stream(self, 'up_or_down')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['up_or_down'].append(data)

        self.output_stock_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_stock = {'all_stock': []}
        for stock in self.stock_data:
            sent_stock['all_stock'].append(stock)
            self.input_stock_stream.add_item(stock)
        return sent_stock
