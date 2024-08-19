from ChainStreamSandBox.report_evaluator.evaluator_base import EvaluatorBase
from ChainStreamSandBox.report_evaluator.utils import *
import os


class EvaluatorSuccessRate(EvaluatorBase):
    def __init__(self, log_path, save_name="success_rate_result",
                 save_folder=os.path.dirname(os.path.abspath(__file__))):
        super().__init__(log_path, save_name, save_folder)

    def calculate_success_rate(self, first_n: list | int | None = None):
        if first_n is None:
            first_n = [1, 3, 5]
        if not isinstance(first_n, list) and not isinstance(first_n, int):
            raise ValueError("first_n should be a list or an integer")
        if isinstance(first_n, int):
            first_n = [first_n]

        self.eval_results['eval_result'] = {}
        for log_path, all_reports in self.reports.items():

            self.eval_results['eval_result'][log_path] = {}
            for N in first_n:
                success_result = {}
                for task, reports in all_reports.items():
                    is_success = False
                    for reports in reports[:N]:
                        if reports.get('start_agent', '') == '[OK]':
                            is_success = True
                            break
                    success_result[task] = is_success

                success_count = sum(success_result.values())
                total_task_count = len(success_result)
                success_rate = (success_count / total_task_count) * 100 if total_task_count > 0 else 0
                self.eval_results['eval_result'][log_path][N] = {
                    'log_path': log_path,
                    'first_n': N,
                    'success_rate': success_rate,
                    'success_count': success_count,
                    'total_task_count': total_task_count,
                    'success_details': success_result
                }

        self._save_results()


if __name__ == "__main__":
    base_folder_path = [r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-19_23-15-20/test_log.json',
                        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-19_23-15-33/test_log.json']
    evaluator_success_rate = EvaluatorSuccessRate(base_folder_path)
    evaluator_success_rate.calculate_success_rate()
