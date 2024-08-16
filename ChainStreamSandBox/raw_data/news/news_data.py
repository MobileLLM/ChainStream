import json
import random
import os
random.seed(42)


class NewsData:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'News.json')
        self.news_articles = []
        self._load_data()

    def _load_data(self):
        with open(self.data_path, "r",encoding = 'UTF-8') as f:
            for line in f:
                item = json.loads(line)
                article = {
                    'category': item.get('category'),
                    'headline': item.get('headline'),
                    'authors': item.get('authors'),
                    'link': item.get('link'),
                    'short_description': item.get('short_description'),
                    'date': item.get('date')
                }
                self.news_articles.append(article)

    def __len__(self):
        return len(self.news_articles)

    def __getitem__(self, index):
        return self.news_articles[index]

    def get_random_article(self):
        return random.choice(self.news_articles)

    def get_random_articles(self, num_articles):
        tmp_list = random.sample(self.news_articles, num_articles)
        return sorted(tmp_list, key=lambda x: x['date'], reverse=True)


if __name__ == '__main__':
    news_data = NewsData()
    print(len(news_data))
    print(news_data.get_random_article())
    print(news_data.get_random_articles(5))
