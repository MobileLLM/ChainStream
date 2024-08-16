import os
from ChainStreamSandBox.report_evaluator.evaluator_base import EvaluatorBase


class EvalOutputSimilarity(EvaluatorBase):
    def __init__(self, reference_log, candidate_log, save_name="output_similarity_result",
                 save_folder=os.path.dirname(os.path.abspath(__file__))):
        super().__init__([reference_log, candidate_log], save_name, save_folder)
        self.reference_log = reference_log
        self.candidate_log = candidate_log

        self.reference_reports = self.reports['reference_log']
        self.candidate_reports = self.reports['candidate_log']

    def calculate_output_similarity(self, first_n: list | int = None):
        if first_n is None:
            first_n = [1, 3, 5]
        if not isinstance(first_n, list) or not isinstance(first_n, int):
            raise ValueError("first_n should be a list or an integer")
        if isinstance(first_n, int):
            first_n = [first_n]

        for N in first_n:
            output_similarity = {}
            for task, reports in self.candidate_reports.items():
                task_output_similarity = {
                    "str_metric": 0,
                    "list_metric": {
                        "bleu": 0,
                        "ed": 0,
                        # "llm": 0,
                    }
                }
                reference_outputs = self.reference_reports[task][0]["output_stream_output"]
                for report in reports:
                    candidate_outputs = report["output_stream_output"]
                    pre_stream_output_similarity = {}
                    for stream_name, output in candidate_outputs.items():
                        pass
                        # TODO: stop here to sleep



if __name__ == '__main__':
    result_folder_path = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result\agent_by_human_new'
    agent_by_human_path = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result\result-new'
    evaluator_output = EvalOutputSimilarity(result_folder_path)
    evaluator_output.calculate_output_similarity(agent_by_human_path,
                                                 result_output_path='./result_similarity_report.txt')
