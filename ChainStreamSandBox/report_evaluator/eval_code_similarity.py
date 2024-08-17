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

    def calculate_code_similarity(self, first_n: list | int = None):
        if first_n is None:
            first_n = [1, 3, 5]
        if not isinstance(first_n, list) or not isinstance(first_n, int):
            raise ValueError("first_n should be a list or an integer")
        if isinstance(first_n, int):
            first_n = [first_n]

        for N in first_n:
            code_similarity = {}
            for task, reports in self.candidate_report.items():
                task_code_similarity = {
                    "bleu": 0,
                    "edit_distance": 0,
                    "codebleu": 0,
                }
                reference_code = self.reference_report[task][0]['sandbox_info']['agent_code']
                for report in reports[:N]:
                    candidate_code = report['sandbox_info']['agent_code']
                    task_code_similarity['bleu'] = max(task_code_similarity['bleu'],
                                                       cal_str_bleu_similarity(reference_code, candidate_code))
                    task_code_similarity['edit_distance'] = max(task_code_similarity['edit_distance'],
                                                                cal_str_edit_distance_similarity(reference_code,
                                                                                                 candidate_code))
                    task_code_similarity['codebleu'] = max(task_code_similarity['codebleu'],
                                                           cal_code_bleu_similarity(reference_code, candidate_code))
                    code_similarity[task] = task_code_similarity
            avg_code_similarity = {
                "bleu": sum([code_similarity[task]['bleu'] for task in code_similarity]) / len(code_similarity),
                "edit_distance": sum([code_similarity[task]['edit_distance'] for task in code_similarity]) / len(
                    code_similarity),
                "codebleu": sum([code_similarity[task]['codebleu'] for task in code_similarity]) / len(code_similarity),
            }
            self.eval_results['eval_result'] = {
                "reference_log": self.reference_log,
                "candidate_log": self.candidate_log,
                "first_n": first_n,
                "avg_code_similarity": avg_code_similarity,
                "code_similarity": code_similarity,
            }


if __name__ == "__main__":
    base_folder_path = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result\result-new'
    evaluator_code = EvalCodeSimilarity(base_folder_path)
    evaluator_code.calculate_code_similarity(result_output_path='./code_similarity_report.txt')
