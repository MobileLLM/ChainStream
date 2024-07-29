import csv
import random
import os

random.seed(42)

csv.field_size_limit(2 ** 31 - 1)


def _parse_email(email_text):
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


class EmailData:
    def __init__(self):
        self.data_path = "selected_email.csv"

        self.data_path = os.path.join(os.path.dirname(__file__), self.data_path)

        self.emails = []

        self._load_data()

    def _load_data(self):
        with open(self.data_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 1 and row[1].startswith("Message-ID"):
                    email = _parse_email(row[1])
                    if email:
                        self.emails.append(email)

    def __len__(self):
        return len(self.emails)

    def __getitem__(self, index):
        return self.emails[index]

    def get_emails(self, num_emails=None):
        tmp_emails = random.sample(self.emails, num_emails)
        tmp_emails.sort(key=lambda x: x['Date'], reverse=True)
        return tmp_emails


if __name__ == '__main__':
    email_data = EmailData()
    print(email_data.get_emails(10))
