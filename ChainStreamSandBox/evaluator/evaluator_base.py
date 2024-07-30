import json
import datetime
import os


class EvaluatorBase:
    def __init__(self):
        pass

    def load_sandbox_logs(self, log_paths: list):
        log_data = []
        for log_path in log_paths:
            log_data.append(self.load_sandbox_log(log_path))
        return log_data

    def load_sandbox_log(self, log_path: str):
        tmp_log = json.load(open(log_path))
        repeat_time = tmp_log['repeat_time']
        all_task_logs = tmp_log['task_log']

        # TODO: process the logs

        return tmp_log, repeat_time, all_task_logs

    def dump_eval_report(self, results: dict, output_name: str = None):
        pass

