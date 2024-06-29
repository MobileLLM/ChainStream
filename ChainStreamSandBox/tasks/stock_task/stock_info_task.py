import os
import csv
import random
import chainstream as cs
from datetime import datetime
from ..task_config_base import TaskConfigBase
from ChainStreamSandBox.raw_data import StockData

csv.field_size_limit(2 ** 31 - 1)

random.seed(6666)


class StockInfoConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_stock_stream = None
        self.input_stock_stream = None
        self.task_description = ("Get the stock information from the `all_stocks` stream, and finally "
                                 "output it to the `cs_stocks` stream")
        self.stock_data = StockData().get_stocks(10)
        self.agent_example = '''
        import chainstream as cs
        from chainstream.llm import get_model
        class testAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("test_news_agent")
                self.input_stream = cs.get_stream("all_stocks")
                self.output_stream = cs.get_stream("cs_stocks")
                self.llm = get_model(["text"])
            def start(self):
                def process_stocks(stocks):
                    # stocks_index = stocks["symbol"]
                    # stocks_date = stocks["date"]           
                    # #print(news_category)
                    self.output_stream.add_item(stocks)
                self.input_stream.register_listener(self, process_stocks)
        
            def stop(self):
                self.input_stream.unregister_listener(self)
        '''
    def init_environment(self, runtime):
        self.input_stock_stream = cs.stream.create_stream('all_stocks')
        self.output_stock_stream = cs.stream.create_stream('cs_stocks')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_stock_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for stock in self.stock_data:
            self.input_stock_stream.add_item(stock)

    def record_output(self, runtime):
        print(self.output_record)
        if len(self.output_record) == 0:
            return False, "No stock data found"
        else:
            return True, self.output_record


if __name__ == '__main__':
    config = StockInfoConfig()
