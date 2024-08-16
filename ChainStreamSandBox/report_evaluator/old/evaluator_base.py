import json
import os


class EvaluatorBase:
    def __init__(self):
        pass

    # def load_sandbox_logs(self, log_paths: list):
    #     log_data = []
    #     for log_path in log_paths:
    #         log_data.append(self.load_sandbox_log(log_path))
    #     return log_data
    #
    # def load_sandbox_log(self, log_path: str):
    #     with open(log_path, 'r', encoding='utf-8') as file:
    #         tmp_log = json.load(file)
    #     repeat_time = tmp_log['repeat_time']
    #     all_task_logs = tmp_log['task_log']
    #     return tmp_log, repeat_time, all_task_logs
    def get_data_from_task_reports(self, base_folder_path):
        all_task_data = {}
        task_folders = []
        for subdir in os.listdir(base_folder_path):
            subdir_path = os.path.join(base_folder_path, subdir)
            task_reports_path = os.path.join(subdir_path, 'task_reports')
            if os.path.isdir(task_reports_path):
                task_folders.append(task_reports_path)
                task_data = {}
                for root, dirs, files in os.walk(task_reports_path):
                    for file in files:
                        if file.endswith(".json"):
                            file_path = os.path.join(root, file)
                            task_name = ""
                            parts = file.split('_')
                            for part in parts:
                                if "Task" in part:
                                    task_name = part
                                    break
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                if task_name not in task_data:
                                    task_data[task_name] = []
                                task_data[task_name].append(data)
                all_task_data[subdir] = task_data
        return all_task_data, task_folders

    def evaluate_similarity(self, s1, s2):
        if s1 is None or s2 is None:
            raise ValueError("Strings cannot be None")
        if len(s1) < len(s2):
            return self.evaluate_similarity(s2, s1)
        if len(s2) == 0:
            return 1.0 if len(s1) == 0 else 0.0

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        distance = previous_row[-1]
        max_distance = max(len(s1), len(s2))
        similarity = 1 - distance / max_distance
        return similarity

    def dump_eval_report(self, results: list, output_name: str):
        with open(output_name, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(result + '\n')


if __name__ == '__main__':
    Evaluator_base = EvaluatorBase()
    Evaluator_base.get_data_from_task_reports(
        r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result')
