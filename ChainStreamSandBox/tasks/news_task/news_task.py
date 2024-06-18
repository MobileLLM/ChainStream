from ..task_config_base import TaskConfigBase
import os
import json
import random
import chainstream as cs
from datetime import datetime
import time
import threading
random.seed(6666)


class NewsTaskConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.task_description =("Read data from the input stream 'all_news', where each item is a dictionary with at least the keys 'headline' and 'date'.Extract the values of the 'headline' and 'date' keys. Generate a string combining the headline and date, and output this string to the stream 'cs_news'."
        "and save the results in the output stream.")

        self.news_data = self._get_news_data()

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream('all_news')
        self.output_news_stream = cs.stream.create_stream('cs_news')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_news_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for message in self.news_data:
            self.input_news_stream.add_item(message)

    def evaluate_task(self, runtime):
        print(self.output_record)
        if len(self.output_record) == 0:
            return False, "No news messages found"
        else:
            return True, "News messages found"

    def _get_news_data(self, num_articles=10):
        data_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "test_data", "news", "News.json")
        news_articles = []

        with open(data_file, 'r', encoding='utf-8') as file:
            for line in file:
                item = json.loads(line)
                article = {
                    'category': item.get('category'),
                    'headline': item.get('headline'),
                    'authors': item.get('authors'),
                    'link': item.get('link'),
                    'short_description': item.get('short_description'),
                    'date': item.get('date')
                }
                news_articles.append(article)

        if news_articles:
            if len(news_articles) > num_articles:
                news_articles = random.sample(news_articles, num_articles)
            news_articles.sort(key=lambda x: x['date'], reverse=True)
            return news_articles
        else:
            return None


if __name__ == '__main__':
    config = NewsTaskConfig()
