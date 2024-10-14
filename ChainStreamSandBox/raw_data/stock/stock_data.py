import csv
import random
from datetime import datetime
import os


class StockData:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'stock_data.csv')

        self.stock_data = []
        self._load_data()

    def _load_data(self):
        with open(self.data_path, "r") as f:
            csv_reader = csv.DictReader(f)
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
                self.stock_data.append(stock)

    def __len__(self):
        return len(self.stock_data)

    def __getitem__(self, index):
        return self.stock_data[index]

    def get_stocks(self, stock_num=10):
        tmp_random = random.Random(42)
        tmp = tmp_random.sample(self.stock_data, stock_num)
        tmp.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        return tmp


if __name__ == '__main__':
    stock_data = StockData()
    print(len(stock_data))
    print(stock_data[0])
    print(stock_data.get_stocks(5))


