from ChainStreamSandBox.report_evaluator.evaluator_base import EvaluatorBase
from ChainStreamSandBox.report_evaluator.utils import *
from ChainStreamSandBox.tasks import get_task_with_data_batch
import os

ALL_TASK_LIST = get_task_with_data_batch()


class EvaluatorSuccessRate(EvaluatorBase):
    def __init__(self, log_path, save_name="success_rate_result",
                 save_folder=os.path.dirname(os.path.abspath(__file__))):
        super().__init__(log_path, save_name, save_folder)

    def calculate_success_rate(self, first_n: list | int | None = None):
        if first_n is None:
            first_n = [[1, 3, 5] for _ in range(len(self.reports))]
        if not isinstance(first_n, list) and not isinstance(first_n, int):
            raise ValueError("first_n should be a list or an integer")
        if isinstance(first_n, int):
            first_n = [[first_n] for _ in range(len(self.reports))]

        self.eval_results['eval_result'] = {}

        cou = 0
        for log_path, all_reports in self.reports.items():

            self.eval_results['eval_result'][log_path] = {}
            for N in first_n[cou]:
                success_result = {}
                for task, reports in all_reports.items():
                    if task not in ALL_TASK_LIST:
                        continue
                    is_success = False
                    for report in reports[:N]:
                        if report.get('start_agent', '') == '[OK]':
                            is_success = True
                            break
                    success_result[task] = is_success

                success_count = sum(success_result.values())
                total_task_count = len(success_result)
                print(f"{log_path} first {N} success rate: {success_count}/{total_task_count}={success_count/total_task_count*100:.2f}%")
                success_rate = (success_count / total_task_count) * 100 if total_task_count > 0 else 0
                self.eval_results['eval_result'][log_path][N] = {
                    'log_path': log_path,
                    'first_n': N,
                    'success_rate': success_rate,
                    'success_count': success_count,
                    'total_task_count': total_task_count,
                    'success_details': success_result
                }
            cou += 1

        self._save_results()


if __name__ == "__main__":
    base_folder_path = [
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-00-50_chainstream_human_written/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-01-40_gpt-4o_native_gpt4o/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_04-36-20_gpt-4o_native_gpt4o/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-04_20-25-46_gpt-4_native_gpt4/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_04-42-59_gpt-4_/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-01-29_native_python_zeroshot/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_09-25-50_native_python_oneshot/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-11-04_chainstream_fewshot_0shot/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-10-46_chainstream_fewshot_1shot/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_22-49-44_chainstream_fewshot_2shot/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-05-59_chainstream_fewshot_3shot/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_22-54-14_chainstream_fewshot_1shot_llm/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_22-54-19_chainstream_fewshot_2shot_llm/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_22-54-27_chainstream_fewshot_3shot_llm/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-41-03_langchain_zeroshot/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_01-45-37_langchain_oneshot/test_log.json',
        r'/Users/liou/Desktop/2024-09-03_19-36-37_chainstream-0-shot-0-example/test_log_20240904_141552_concat_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/test_log_20240904_200721_concat_log_for_feedback_0shot_1llm.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/test_log_20240904_201310_concat_log_for_feedback_0shot_2llm.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/test_log_20240904_201434_concat_log_for_feedback_0shot_3llm.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_05-42-28_chainstream_feedback_0example_without_stdout/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_05-41-40_chainstream_feedback_0example_without_output/test_log.json',
        r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_05-38-35_chainstream_feedback_0example_without_err/test_log.json'
    ]
    first_n = [
        [1],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1],
        [1],
        [1],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1, 3, 5],
        [1],
        [1],
        [1]
    ]
    evaluator_success_rate = EvaluatorSuccessRate(base_folder_path)
    evaluator_success_rate.calculate_success_rate(first_n)
