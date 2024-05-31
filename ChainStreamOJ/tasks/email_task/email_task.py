import os
import csv
import random
import chainstream as cs
from datetime import datetime
from ..task_config_base import TaskConfigBase
import sys

csv.field_size_limit(2**31 - 1)

random.seed(6666)

class EmailTaskConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.task_description = (
            "Get the emails from the `all_emails` stream, "
            "and finally output it to the `cs_emails` stream")
        self.email_data = self._get_email_data()

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

    def _get_email_data(self, num_emails=20):
        data_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "test_data", "email",
                                 "selected_email.csv")
        emails = []

        with open(data_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) > 1 and row[1].startswith("Message-ID"):
                    email = self._parse_email(row[1])
                    if email:
                        emails.append(email)

        if emails:
            if len(emails) > num_emails:
                emails = random.sample(emails, num_emails)
            emails.sort(key=lambda x: x['Date'], reverse=True)
            return emails
        else:
            return None

    def _parse_email(self, email_text):
        email_info = {}
        lines = email_text.split('\n')
        collecting = False
        collected_text = []
        for line in lines:
            if line.startswith('Date:'):
                email_info['Date'] = line[len('Date: '):].strip()
            elif line.startswith('From:'):
                email_info['From'] = line[len('From: '):].strip()
            elif line.startswith('To:'):
                email_info['To'] = line[len('To: '):].strip()
            elif line.startswith('Subject:'):
                email_info['Subject'] = line[len('Subject: '):].strip()
            elif line.startswith('X-FileName:'):
                # email_info['X-FileName'] = line[len('X-FileName: '):].strip()
                collecting = True
            elif collecting:
                collected_text.append(line.strip())

        if collected_text:
            email_info['Content'] = '\n'.join(collected_text)

        if all(key in email_info for key in ('Date', 'From', 'To', 'Subject', 'Content')):
            return email_info
        return None

if __name__ == '__main__':
    config = EmailTaskConfig()
