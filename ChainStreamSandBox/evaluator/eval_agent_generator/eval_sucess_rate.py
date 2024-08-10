from collections import defaultdict
from ChainStreamSandBox.evaluator.evaluator_base import EvaluatorBase


class EvaluatorSuccessRate(EvaluatorBase):
    def __init__(self, base_folder_path):
        super().__init__()
        self.base_folder_path = base_folder_path

    def calculate_success_rate(self, result_output_path):
        results = []
        task_data_dict, task_folder = self.get_data_from_task_reports(self.base_folder_path)
        for folder_name, task_data in task_data_dict.items():
            task_success_status = defaultdict(bool)
            unique_tasks = set()
            for task_name, data_list in task_data.items():
                unique_tasks.add(task_name)
                for json_data in data_list:
                    start_agent_status = json_data.get('start_agent', '')
                    if start_agent_status == "[OK]":
                        task_success_status[task_name] = True
            success_count = sum(task_success_status.values())
            total_task_count = len(unique_tasks)
            success_rate = (success_count / total_task_count) * 100 if total_task_count > 0 else 0
            result = (f"Method: {folder_name}\n"
                      f"Tasks processed: {total_task_count}\n"
                      f"Agent started successfully: {success_count}\n"
                      f"Success rate: {success_rate:.2f}%\n")
            results.append(result)
        self.dump_eval_report(results, result_output_path)


if __name__ == "__main__":
    base_folder_path = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result'
    evaluator_success_rate = EvaluatorSuccessRate(base_folder_path)
    evaluator_success_rate.calculate_success_rate(result_output_path="./success_rate_report.txt")
