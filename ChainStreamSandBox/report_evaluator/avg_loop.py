import json


def avg_loop(log_path):
    with open(log_path) as log_file:
        log_data = json.load(log_file)



