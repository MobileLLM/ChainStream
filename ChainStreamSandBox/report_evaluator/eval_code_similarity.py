from ChainStreamSandBox.report_evaluator.evaluator_base import EvaluatorBase
from ChainStreamSandBox.report_evaluator.utils import *
import os


class EvalCodeSimilarity(EvaluatorBase):
    def __init__(self, reference_log, candidate_log, save_name="code_similarity_result",
                 save_folder=os.path.dirname(os.path.abspath(__file__))):
        super().__init__([reference_log, candidate_log], save_name, save_folder)
        self.reference_log = reference_log
        self.candidate_log = candidate_log

        self.reference_report = self.reports[reference_log]
        self.candidate_report = self.reports[candidate_log]

    def calculate_code_similarity(self, first_n: list | int | None = None):
        if first_n is None:
            first_n = [1, 3, 5]
        if not isinstance(first_n, list) and not isinstance(first_n, int):
            raise ValueError("first_n should be a list or an integer")
        if isinstance(first_n, int):
            first_n = [first_n]

        self.eval_results['eval_result'] = {}
        for N in first_n:
            self.eval_results['eval_result'][N] = {}
            code_similarity = {}
            for task, reports in self.candidate_report.items():
                task_code_similarity = {
                    "bleu": {"score": 0, "code": None, "report_init_time": None},
                    "edit_distance": {"score": 0, "code": None, "report_init_time": None},
                    "codebleu": {"score": 0, "code": None, "report_init_time": None},
                }
                reference_code = self.reference_report[task][0]['sandbox_info']['agent_code']

                for i, report in enumerate(reports[:N]):
                    candidate_code = report['sandbox_info']['agent_code']
                    tmp_bleu = cal_str_bleu_similarity(reference_code, candidate_code)
                    if tmp_bleu > task_code_similarity['bleu']['score']:
                        task_code_similarity['bleu']['score'] = tmp_bleu
                        task_code_similarity['bleu']['code'] = candidate_code
                        task_code_similarity['bleu']['report_init_time'] = report['sandbox_info']['sandbox_init_time']

                    tmp_ed = cal_str_edit_distance_similarity(reference_code, candidate_code)
                    if tmp_ed > task_code_similarity['edit_distance']['score']:
                        task_code_similarity['edit_distance']['score'] = tmp_ed
                        task_code_similarity['edit_distance']['code'] = candidate_code
                        task_code_similarity['edit_distance']['report_init_time'] = report['sandbox_info'][
                            'sandbox_init_time']

                    tmp_codebleu = cal_code_bleu_similarity(reference_code, candidate_code)
                    if tmp_codebleu > task_code_similarity['codebleu']['score']:
                        task_code_similarity['codebleu']['score'] = tmp_codebleu
                        task_code_similarity['codebleu']['code'] = candidate_code
                        task_code_similarity['codebleu']['report_init_time'] = report['sandbox_info'][
                            'sandbox_init_time']

                code_similarity[task] = task_code_similarity
            avg_code_similarity = {
                "bleu": sum([code_similarity[task]['bleu']['score'] for task in code_similarity]) / len(code_similarity),
                "edit_distance": sum([code_similarity[task]['edit_distance']['score'] for task in code_similarity]) / len(
                    code_similarity),
                "codebleu": sum([code_similarity[task]['codebleu']['score'] for task in code_similarity]) / len(code_similarity),
            }
            self.eval_results['eval_result'][N] = {
                "reference_log": self.reference_log,
                "candidate_log": self.candidate_log,
                "first_n": N,
                "avg_code_similarity": avg_code_similarity,
                "code_similarity": code_similarity,
            }

        self._save_results()


if __name__ == "__main__":
    path1 = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-21_19-43-43_human-written\test_log.json'
    path2 = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-21_19-32-30_langchain-zero-shot\test_log.json'
    evaluator_code = EvalCodeSimilarity(path1, path2)
    evaluator_code.calculate_code_similarity()
