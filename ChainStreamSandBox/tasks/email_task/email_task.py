import os
import csv
import random
import chainstream as cs
from datetime import datetime
from ..task_config_base import TaskConfigBase
import sys
from ChainStreamSandBox.raw_data import EmailData

csv.field_size_limit(2 ** 31 - 1)

random.seed(6666)


class EmailTaskConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.task_description = ("Read data from the input stream 'all_news', where each item is a dictionary with at "
                                 "least the keys 'headline' and 'category'.Extract the values of the 'headline' and "
                                 "'category' keys. Generate a string combining the headline and category, and output "
                                 "this string to the stream 'cs_news'."
                                 "and save the results in the output stream.")
        self.email_data = EmailData().get_emails(10)

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream('all_emails')
        self.output_email_stream = cs.stream.create_stream('cs_emails')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_email_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for message in self.email_data:
            self.input_email_stream.add_item(message)

    def evaluate_task(self, runtime):
        print(self.output_record)
        if len(self.output_record) == 0:
            return False, "No emails found"
        else:
            return True, f"{len(self.output_record)} emails found"


if __name__ == '__main__':
    config = EmailTaskConfig()
