import csv
import random
import os


class AirlineTwitterData:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'Airline_Tweets.csv')

        self.airline_data = []
        self._load_data()

    def _load_data(self):
        with open(self.data_path, "r",encoding="utf-8",errors="ignore") as f:
            csv_reader = csv.DictReader(f)
            headers = csv_reader.fieldnames
            expected_headers = [
                'airline_sentiment', 'negative_reason','airline', 'name',
                'retweet_count', 'text', 'tweet_created','tweet_location', 'user_timezone'
            ]
            if not all(header in headers for header in expected_headers):
                raise ValueError("CSV headers do not match expected columns")
            for row in csv_reader:
                tweet_entry = {
                    'airline_sentiment': row['airline_sentiment'],
                    'negative_reason': row['negative_reason'],
                    'airline': row['airline'],
                    'name': row['name'],
                    'retweet_count': int(row['retweet_count']),
                    'text': row['text'],
                    'tweet_created': row['tweet_created'],
                    'tweet_location': row['tweet_location'],
                    'user_timezone': row['user_timezone']
                }
                self.airline_data.append(tweet_entry)

    def __len__(self):
        return len(self.airline_data)

    def __getitem__(self, index):
        return self.airline_data[index]

    def get_twitter(self, num_twitter):
        tmp_random = random.Random(42)
        tmp = tmp_random.sample(self.airline_data, num_twitter)
        return tmp


if __name__ == '__main__':
    airline_data = AirlineTwitterData()
    print(len(airline_data))
    print(airline_data[0])
    print(airline_data.get_twitter(1))
