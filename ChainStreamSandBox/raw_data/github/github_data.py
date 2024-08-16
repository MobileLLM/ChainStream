import csv
import random
import os
random.seed(42)

class GitHubData:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'github.csv')

        self.github_data = []
        self._load_data()

    def _load_data(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            csv_reader = csv.DictReader(f)
            headers = csv_reader.fieldnames
            expected_headers = ['name', 'stars_count', 'forks_count', 'watchers', 'pull_requests', 'primary_language',
                                'languages_used', 'commit_count', 'created_at', 'licence']
            if not all(header in headers for header in expected_headers):
                raise ValueError("CSV headers do not match expected columns")

            for row in csv_reader:
                github_entry = {
                    'name': row['name'],
                    'stars_count': int(row['stars_count']) if row['stars_count'].isdigit() else 0,
                    'forks_count': int(row['forks_count']) if row['forks_count'].isdigit() else 0,
                    'watchers': int(row['watchers']) if row['watchers'].isdigit() else 0,
                    'pull_requests': int(row['pull_requests']) if row['pull_requests'].isdigit() else 0,
                    'primary_language': row['primary_language'],
                    'languages_used': row['languages_used'].split(','),
                    'commit_count': int(row['commit_count']) if row['commit_count'].isdigit() else 0,
                    'created_at': row['created_at'],
                    'licence': row['licence']
                }
                self.github_data.append(github_entry)

    def __len__(self):
        return len(self.github_data)

    def __getitem__(self, index):
        return self.github_data[index]

    def get_github_data(self, num_entries):
        tmp = random.sample(self.github_data, num_entries)
        return tmp


if __name__ == '__main__':
    github_data = GitHubData()
    print(len(github_data))
    print(github_data[0])
    print(github_data.get_github_data(5))
