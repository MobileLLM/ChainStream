import csv
import random
import os
random.seed(42)


class LandmarkData:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'landmarks.csv')

        self.landmark_data = []
        self._load_data()

    def _load_data(self):
        with open(self.data_path, "r") as f:
            csv_reader = csv.DictReader(f)
            headers = csv_reader.fieldnames
            expected_headers = [
                'PrimaryPropertyType', 'PropertyName', 'Street Address', 'Neighborhood', 'YearBuilt',
                'NumberofFloors', 'Electricity(kWh)', 'NaturalGas(therms)', 'GHGEmissions(MetricTonsCO2e)'
            ]
            if not all(header in headers for header in expected_headers):
                raise ValueError("CSV headers do not match expected columns")

            for row in csv_reader:
                landmark_entry = {
                    'PrimaryPropertyType': row['PrimaryPropertyType'],
                    'PropertyName': row['PropertyName'],
                    'Street Address': row['Street Address'],
                    'Neighborhood': row['Neighborhood'],
                    'YearBuilt': int(row['YearBuilt']),
                    'NumberofFloors': int(row['NumberofFloors']) if row['NumberofFloors'] else None,
                    'Electricity(kWh)': float(row['Electricity(kWh)']) if row['Electricity(kWh)'] else None,
                    'NaturalGas(therms)': float(row['NaturalGas(therms)']) if row['NaturalGas(therms)'] else None,
                    'GHGEmissions(MetricTonsCO2e)': float(row['GHGEmissions(MetricTonsCO2e)']) if row['GHGEmissions(MetricTonsCO2e)'] else None
                }
                self.landmark_data.append(landmark_entry)

    def __len__(self):
        return len(self.landmark_data)

    def __getitem__(self, index):
        return self.landmark_data[index]

    def get_landmarks(self, num_landmarks):
        tmp = random.sample(self.landmark_data, num_landmarks)
        return tmp


if __name__ == '__main__':
    landmark_data = LandmarkData()
    print(len(landmark_data))
    print(landmark_data[0])
    print(landmark_data.get_landmarks(5))
