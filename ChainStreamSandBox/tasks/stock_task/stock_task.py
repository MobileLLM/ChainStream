import os
import csv
import random
import chainstream as cs
from datetime import datetime
from ..task_config_base import TaskConfigBase
import sys

csv.field_size_limit(2**31 - 1)

random.seed(6666)

class StockTaskConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.task_description =("Get the stock information from the `all_stocks` stream, and finally "
                                 "output it to the `cs_stocks` stream")
        self.stock_data = self._get_stock_data()

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

    def evaluate_task(self, runtime):
        print(self.output_record)
        if len(self.output_record) == 0:
            return False, "No stock data found"
        else:
            return True, f"{len(self.output_record)} stock entries found"

    def _get_stock_data(self, num_stocks=20):
        data_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "test_data", "stock", "stock_data.csv")
        stocks = []

        with open(data_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            headers = csv_reader.fieldnames
            if 'date' not in headers or 'symbol' not in headers or 'open' not in headers or 'close' not in headers or 'low' not in headers or 'high' not in headers or 'volume' not in headers:
                raise ValueError("CSV headers do not match expected columns")

            for row in csv_reader:
                stock = {
                    'date': row['date'],
                    'symbol': row['symbol'],
                    'open': float(row['open']),
                    'close': float(row['close']),
                    'low': float(row['low']),
                    'high': float(row['high']),
                    'volume': float(row['volume'])
                }
                stocks.append(stock)

        if stocks:
            if len(stocks) > num_stocks:
                stocks = random.sample(stocks, num_stocks)
            stocks.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
            return stocks
        else:
            return None


if __name__ == '__main__':
    config = StockTaskConfig()
