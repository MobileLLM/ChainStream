import csv
import random

random.seed(42)


class WifiData:
    def __init__(self):
        self.data_path = "wifi.csv"

        self.wifi_data = []
        self._load_data()

    def _load_data(self):
        with open(self.data_path, "r") as f:
            csv_reader = csv.DictReader(f)
            headers = csv_reader.fieldnames
            expected_headers = ['Time', 'MAC.Address', 'Vendor', 'SSID', 'Signal.Strength', 'Channel']
            if not all(header in headers for header in expected_headers):
                raise ValueError("CSV headers do not match expected columns")

            for row in csv_reader:
                wifi_entry = {
                    'Time': row['Time'],
                    'MAC.Address': row['MAC.Address'],
                    'Vendor': row['Vendor'],
                    'SSID': row['SSID'],
                    'Signal': row['Signal.Strength'],
                    'Channel': row['Channel']
                }
                self.wifi_data.append(wifi_entry)

    def __len__(self):
        return len(self.wifi_data)

    def __getitem__(self, index):
        return self.wifi_data[index]

    def get_wifi(self, num_entries):
        tmp = random.sample(self.wifi_data, num_entries)
        return tmp


if __name__ == '__main__':
    wifi_data = WifiData()
    print(len(wifi_data))
    print(wifi_data[0])
    print(wifi_data.get_wifi(5))
