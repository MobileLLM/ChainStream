from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import StockData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class StockTask1(SingleAgentTaskConfigBase):
    def __init__(self, number=200):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_stock_stream = None
        self.input_stock_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Daily_information,
                                modality=Modality_Task_tag.Text)
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
                "stream_id": "fallen_price_stock",
                "description": "A stream of the change percentages with the volume of the 'MLM' stock in the field "
                               "'symbol' if the change percentage is lower than 0",
                "fields": {
                    "change_percentage": "The percentage change in the fallen-price stock, float",
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
        self.stock_output = cs.create_stream(self, "fallen_price_stock")
        self.llm = cs.llm.get_model("Text")

        def filter_mlm_stocks(stock_dict):
            if stock_dict['symbol'] == "MLM":
                return stock_dict
        
        def up_or_down(stock):
            open_price = float(stock['open'])
            close_price = float(stock['close'])
            volume = float(stock['volume'])
            if open_price != 0:
                change_percentage = (close_price - open_price) / open_price * 100
            else:
                change_percentage = 0.0
            if change_percentage < 0:
                self.stock_output.add_item({
                    "change_percentage": change_percentage,
                    "volume": volume
                }) 

        self.stock_input.for_each(filter_mlm_stocks).for_each(up_or_down)
        '''

    def init_environment(self, runtime):
        self.input_stock_stream = cs.stream.create_stream(self, 'all_stock')
        self.output_stock_stream = cs.stream.create_stream(self, 'fallen_price_stock')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['fallen_price_stock'].append(data)

        self.output_stock_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_stock_stream = cs.stream.create_stream(self, 'all_stock')

    def init_output_stream(self, runtime):
        self.output_stock_stream = cs.stream.get_stream(self, 'fallen_price_stock')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['fallen_price_stock'].append(data)

        self.output_stock_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        stock_data = [
            {
                "date": "2024-09-01",
                "symbol": "MLM",
                "open": "85.00",
                "close": "84.50",
                "low": "83.75",
                "high": "85.20",
                "volume": "800000.0"
            },
            {
                "date": "2024-09-02",
                "symbol": "MLM",
                "open": "84.75",
                "close": "84.00",
                "low": "83.50",
                "high": "85.00",
                "volume": "750000.0"
            },
            {
                "date": "2024-09-03",
                "symbol": "MLM",
                "open": "85.20",
                "close": "84.80",
                "low": "84.00",
                "high": "85.50",
                "volume": "780000.0"
            },
            {
                "date": "2024-09-04",
                "symbol": "MLM",
                "open": "84.90",
                "close": "84.30",
                "low": "83.90",
                "high": "85.10",
                "volume": "770000.0"
            },
            {
                "date": "2024-09-05",
                "symbol": "MLM",
                "open": "85.10",
                "close": "84.60",
                "low": "84.00",
                "high": "85.30",
                "volume": "790000.0"
            }
        ]
        self.stock_data.extend(stock_data)
        sent_stock = {'all_stock': []}
        for stock in self.stock_data:
            sent_stock['all_stock'].append(stock)
            self.input_stock_stream.add_item(stock)
        return sent_stock
