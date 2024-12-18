import json
import random
import os



class ArxivData:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'arxiv-random-selected.json')

        self.paper_data = self._load_data()

    def _load_data(self):
        cs_papers = []
        with open(self.data_path, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                if 'categories' in item and 'cs' in item['categories']:
                    paper = {
                        'authors': str(item['authors']),
                        'title': str(item['title']),
                        'abstract': str(item['abstract']),
                        'comments': str(item['comments']),
                        'journal-ref': str(item['journal-ref']),
                        'license': str(item['license']),
                        'versions': str(item['versions']),
                        'update_date': str(item['update_date'])
                    }
                    cs_papers.append(paper)

        return cs_papers

    def __len__(self):
        return len(self.paper_data)

    def __getitem__(self, index):
        return self.paper_data[index]

    def get_random_paper(self):
        tmp_random = random.Random(42)
        return tmp_random.choice(self.paper_data)

    def get_random_papers(self, num_papers):
        tmp_random = random.Random(42)
        tmp = tmp_random.sample(self.paper_data, num_papers)
        return sorted(tmp, key=lambda x: x['update_date'], reverse=True)


if __name__ == '__main__':
    arxiv_data = ArxivData()
    print(len(arxiv_data))
    print(arxiv_data.get_random_paper())
    print(arxiv_data.get_random_papers(10))
