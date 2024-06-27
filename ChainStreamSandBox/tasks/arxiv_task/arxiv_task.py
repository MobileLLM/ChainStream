import raw_data
from ..task_config_base import TaskConfigBase
import os
import json
import random
import chainstream as cs
from datetime import datetime
import time
import threading
from ChainStreamSandBox.raw_data import ArxivData

random.seed(6666)


class ArxivTaskConfig(TaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
        self.task_description = (
            "Retrieve data from the input stream all_arxiv, and process the value corresponding to the 'abstract' key in the paper dictionary: "
            "Extract the abstract content and generate a prompt asking whether the abstract is related to 'edge LLM agent'. "
            "Query the prompt using the text type llm to get a response. If the response is 'Yes', add the paper to the output stream cs_arxiv, "
            "and save the results in the output stream.")

        self.paper_data = ArxivData().get_random_papers(paper_number)

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
