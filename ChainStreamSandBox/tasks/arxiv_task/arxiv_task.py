from ..task_config_base import TaskConfigBase
import os
import json
import random
import chainstream as cs
from datetime import datetime
import time
import threading
random.seed(6666)


class ArxivTaskConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.task_description = (
            "Retrieve data from the input stream all_arxiv, and process the value corresponding to the 'abstract' key in the paper dictionary: "
            "Extract the abstract content and generate a prompt asking whether the abstract is related to 'edge LLM agent'. "
            "Query the prompt using the text type llm to get a response. If the response is 'Yes', add the paper to the output stream cs_arxiv, "
            "and save the results in the output stream.")

        self.paper_data = self._get_paper_data()

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream('all_arxiv')
        self.output_paper_stream = cs.stream.create_stream('cs_arxiv')
        self.clock_stream = cs.stream.create_stream('clock_every_day')
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

    def _get_paper_data(self, num_papers=10):
        data_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "test_data", "paper",
                                 "arxiv-random-selected.json")
        cs_papers = []

        with open(data_file, 'r', encoding='utf-8') as file:
            for line in file:
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

        if cs_papers:
            if len(cs_papers) > num_papers:
                cs_papers = random.sample(cs_papers, num_papers)
            cs_papers.sort(key=lambda x: x['update_date'], reverse=True)
            return cs_papers
        else:
            return None
    def start_clock_stream(self):
        def add_current_date():
            while True:
                current_date = datetime.now().isoformat()
                self.clock_stream.add_item({'date': current_date})
                time.sleep(86400)  # Sleep for one day (86400 seconds)

        clock_thread = threading.Thread(target=add_current_date)
        clock_thread.daemon = True  # Daemonize thread
        clock_thread.start()

if __name__ == '__main__':
    config = ArxivTaskConfig()
