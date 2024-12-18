import csv
import random
import os


class GPSData:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'gps.csv')

        self.gps_data = []
        self._load_data()

    def _load_data(self):
        with open(self.data_path, "r") as f:
            csv_reader = csv.DictReader(f)
            headers = csv_reader.fieldnames
            expected_headers = ['CountryName', 'CapitalName', 'CapitalLatitude', 'CapitalLongitude', 'CountryCode',
                                'ContinentName']
            if not all(header in headers for header in expected_headers):
                raise ValueError("CSV headers do not match expected columns")

            for row in csv_reader:
                gps_entry = {
                    'CountryName': row['CountryName'],
                    'CapitalName': row['CapitalName'],
                    'CapitalLatitude': float(row['CapitalLatitude']),
                    'CapitalLongitude': float(row['CapitalLongitude']),
                    'CountryCode': row['CountryCode'],
                    'ContinentName': row['ContinentName']
                }
                self.gps_data.append(gps_entry)

    def __len__(self):
        return len(self.gps_data)

    def __getitem__(self, index):
        return self.gps_data[index]

    def get_gps(self, num_gps):
        tmp_random = random.Random(42)
        tmp = tmp_random.sample(self.gps_data, num_gps)
        return tmp


if __name__ == '__main__':
    gps_data = GPSData()
    print(len(gps_data))
    print(gps_data[0])
    print(gps_data.get_gps(5))
