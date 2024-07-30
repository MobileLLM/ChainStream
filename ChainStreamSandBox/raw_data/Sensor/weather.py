import csv
import random
import os
random.seed(42)


class WeatherData:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'weather.csv')

        self.weather_data = []
        self._load_data()

    def _load_data(self):
        with open(self.data_path, "r") as f:
            csv_reader = csv.DictReader(f)
            headers = csv_reader.fieldnames
            expected_headers = ['Location', 'Date_Time', 'Temperature_C', 'Humidity_pct', 'Precipitation_mm', 'Wind_Speed_kmh']
            if not all(header in headers for header in expected_headers):
                raise ValueError("CSV headers do not match expected columns")

            for row in csv_reader:
                weather_entry = {
                    'Location': row['Location'],
                    'Date_Time': row['Date_Time'],
                    'Temperature_C': float(row['Temperature_C']),
                    'Humidity_pct': float(row['Humidity_pct']),
                    'Precipitation_mm': float(row['Precipitation_mm']),
                    'Wind_Speed_kmh': float(row['Wind_Speed_kmh'])
                }
                self.weather_data.append(weather_entry)

    def __len__(self):
        return len(self.weather_data)

    def __getitem__(self, index):
        return self.weather_data[index]

    def get_weather(self, num_entries):
        tmp = random.sample(self.weather_data, num_entries)
        return tmp


if __name__ == '__main__':
    weather_data = WeatherData()
    print(len(weather_data))
    print(weather_data[0])
    print(weather_data.get_weather(5))
