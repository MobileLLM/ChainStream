import json
import random

random.seed(42)


class ArxivData:
    def __init__(self):
        self.data_path = 'arxiv-random-selected.json'

        self.paper_data = self._load_data()

    def _load_data(self):
        cs_papers = []
        with open(self.data_path, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                if 'categories' in item and 'cs' in item['categories']:
                    paper = {
                        'authors': item['authors'],
                        'title': item['title'],
                        'abstract': item['abstract'],
                        'comments': item['comments'],
                        'journal-ref': item['journal-ref'],
                        'license': item['license'],
                        'versions': item['versions'],
                        'update_date': item['update_date']
                    }
                    cs_papers.append(paper)

        return cs_papers

    def __len__(self):
        return len(self.paper_data)

    def __getitem__(self, index):
        return self.paper_data[index]

    def get_random_paper(self):
        return random.choice(self.paper_data)

    def get_random_papers(self, num_papers):
        return random.sample(self.paper_data, num_papers).sort(key=lambda x: x['update_date'], reverse=True)
