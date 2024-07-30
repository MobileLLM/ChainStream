import csv
import random
import os

random.seed(42)


class HealthData:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'health_data.csv')

        self.health_data = []
        self._load_data()

    def _load_data(self):
        with open(self.data_path, "r") as f:
            csv_reader = csv.DictReader(f)
            headers = csv_reader.fieldnames
            expected_headers = [
                'Gender', 'Age', 'Occupation', 'Sleep Duration', 'Quality of Sleep',
                'Physical Activity Level', 'Stress Level', 'BMI Category', 'Daily Steps',
                'Sleep Disorder', 'SystolicBP', 'DiastolicBP', 'BS', 'BodyTemp', 'HeartRate','RiskLevel'
            ]
            if not all(header in headers for header in expected_headers):
                raise ValueError("CSV headers do not match expected columns")

            for row in csv_reader:
                health_entry = {
                    'Gender': row['Gender'],
                    'Age': int(row['Age']),
                    'Occupation': row['Occupation'],
                    'Sleep Duration': float(row['Sleep Duration']),
                    'Quality of Sleep': row['Quality of Sleep'],
                    'Physical Activity Level': row['Physical Activity Level'],
                    'Stress Level': row['Stress Level'],
                    'BMI Category': row['BMI Category'],
                    'Daily Steps': int(row['Daily Steps']),
                    'Sleep Disorder': row['Sleep Disorder'],
                    'SystolicBP': float(row['SystolicBP']),
                    'DiastolicBP': float(row['DiastolicBP']),
                    'BS': float(row['BS']),
                    'BodyTemp': float(row['BodyTemp']),
                    'HeartRate': row['HeartRate'],
                    'RiskLevel': row['RiskLevel']
                }
                self.health_data.append(health_entry)

    def __len__(self):
        return len(self.health_data)

    def __getitem__(self, index):
        return self.health_data[index]

    def get_health_data(self, num_entries):
        tmp = random.sample(self.health_data, num_entries)
        return tmp


if __name__ == '__main__':
    health_data = HealthData()
    print(len(health_data))
    print(health_data[0])
    print(health_data.get_health_data(5))
