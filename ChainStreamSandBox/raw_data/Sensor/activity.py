import csv
import random

class ActivityData:
    def __init__(self):
        self.data_path = "activity.csv"
        self.activity_data = []
        self._load_data()

        self.activity = ['Walking', 'Standing', 'Sitting', 'Upstairs', 'Downstairs', 'Jogging']

    def _load_data(self):
        with open(self.data_path, "r") as f:
            csv_reader = csv.DictReader(f)
            headers = csv_reader.fieldnames
            expected_headers = [
                'user', 'activity', 'timestamp', 'x-axis', 'y-axis', 'z-axis', 'Date',
                'Total_Distance', 'Very_Active_Distance', 'Moderately_Active_Distance',
                'Light_Active_Distance', 'Sedentary_Active_Distance', 'Very_Active_Minutes',
                'Fairly_Active_Minutes', 'Lightly_Active_Minutes', 'Sedentary_Minutes',
                'Steps', 'Calories_Burned'
            ]
            if not all(header in headers for header in expected_headers):
                raise ValueError("CSV headers do not match expected columns")

            for row in csv_reader:
                activity_entry = {
                    'user': row['user'],
                    'activity': row['activity'],
                    'timestamp': row['timestamp'],
                    'x-axis': float(row['x-axis']),
                    'y-axis': float(row['y-axis']),
                    'z-axis': float(row['z-axis']),
                    'Date': row['Date'],
                    'Total_Distance': float(row['Total_Distance']),
                    'Very_Active_Distance': float(row['Very_Active_Distance']),
                    'Moderately_Active_Distance': float(row['Moderately_Active_Distance']),
                    'Light_Active_Distance': float(row['Light_Active_Distance']),
                    'Sedentary_Active_Distance': float(row['Sedentary_Active_Distance']),
                    'Very_Active_Minutes': int(row['Very_Active_Minutes']),
                    'Fairly_Active_Minutes': int(row['Fairly_Active_Minutes']),
                    'Lightly_Active_Minutes': int(row['Lightly_Active_Minutes']),
                    'Sedentary_Minutes': int(row['Sedentary_Minutes']),
                    'Steps': int(row['Steps']),
                    'Calories_Burned': float(row['Calories_Burned'])
                }
                self.activity_data.append(activity_entry)

    def __len__(self):
        return len(self.activity_data)

    def __getitem__(self, index):
        return self.activity_data[index]

    def get_random_activity_data(self):
        activity_sequence = self.get_activity_sequence()
        print(activity_sequence)
        result = []
        for activity in activity_sequence:
            num_entries = random.randint(0, 20)
            activity_entries = random.sample([entry for entry in self.activity_data if entry['activity'].lower() == activity.lower()], num_entries)
            result.extend(activity_entries)

        return result

    def get_activity_sequence(self):
        activity_sequence = []

        act_num = random.randint(1, 4)

        act_seq = [random.choice(self.activity) for _ in range(act_num)]

        for act in act_seq:
            act_len = random.randint(1, 5)
            activity_sequence.extend([act for i in range(act_len)])

        return activity_sequence


if __name__ == '__main__':
    activity_data = ActivityData()
    random_activity_data = activity_data.get_random_activity_data()

    print(f"Random Activity Data:")
    for entry in random_activity_data:
        print(entry)
