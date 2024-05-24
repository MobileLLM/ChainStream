from ..task_config_base import TaskConfigBase
import os
import json
import random
import chainstream as cs
from datetime import datetime
random.seed(6666)


class CSArxivTaskConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.task_description = ("Find all work-related arxiv. Get the message from the `all_arxiv` stream, and finally "
                                 "output it to the `cs_arxiv` stream")

        self.paper_data = self._get_paper_data()

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream('all_arxiv')
        self.output_paper_stream = cs.stream.create_stream('cs_arxiv')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)
        self.output_paper_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for message in self.paper_data:
            self.input_paper_stream.add_item(message)

    def evaluate_task(self, runtime):
        print(self.output_record)
        if len(self.output_record) == 0:
            return False, "No cs-related message found"
        else:
            return True, "cs-related message found"


    def _get_cs_paper(self,num_papers=10):
        data_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "test_data", "arxiv",
                                 "arxiv-random-selected.json")
        cs_papers = []
        data = json.load(open(data_file, "r"))
        for item in data:
            if 'categories' in item and 'cs' in item['categories']:
                paper = {}
                paper['authors'] = item['authors']
                paper['title'] = item['title']
                paper['abstract'] = item['abstract']
                paper['update_date'] = item['update_date']
                paper['update_date'] = datetime.strptime(item['update_date'], '%Y-%m-%d')
        if cs_papers:
            if len(cs_papers) > num_papers:
                cs_papers = random.sample(cs_papers, num_papers)
            cs_papers.sort(key=lambda x: x['update_date'], reverse=True)
            return cs_papers
        else:
            return None

if __name__ == '__main__':
    config = CSArxivTaskConfig()