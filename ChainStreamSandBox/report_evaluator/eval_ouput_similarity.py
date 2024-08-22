import os
from ChainStreamSandBox.report_evaluator.evaluator_base import EvaluatorBase
from ChainStreamSandBox.report_evaluator.utils import *


class EvalOutputSimilarity(EvaluatorBase):
    def __init__(self, reference_log, candidate_log, save_name="output_similarity_result",
                 save_folder=os.path.dirname(os.path.abspath(__file__))):
        super().__init__([reference_log, candidate_log], save_name, save_folder)
        self.reference_log = reference_log
        self.candidate_log = candidate_log

        self.reference_reports = self.reports[reference_log]
        self.candidate_reports = self.reports[candidate_log]

    def calculate_output_similarity(self, first_n: list | int | None = None):
        if first_n is None:
            first_n = [1, 3, 5]
        if not isinstance(first_n, list) and not isinstance(first_n, int):
            raise ValueError("first_n should be a list or an integer")
        if isinstance(first_n, int):
            first_n = [first_n]

        self.eval_results['eval_result'] = {}
        for N in first_n:
            self.eval_results['eval_result'][N] = {}
            output_similarity = {}
            for task, reports in self.candidate_reports.items():
                task_output_similarity = {
                    "str_metric": {
                        "len_weighted_bleu": {"score": 0, "output": None, "report_init_time": None},
                        "len_weighted_ed": {"score": 0, "output": None, "report_init_time": None},
                        "bleu": {"score": 0, "output": None, "report_init_time": None},
                        "ed": {"score": 0, "output": None, "report_init_time": None},
                        # "llm": {"score": 0, "output": None, "report_init_time": None},
                    },
                    "hard_list_metric": {
                        "len_weighted_bleu": {"score": 0, "output": None, "report_init_time": None},
                        "len_weighted_ed": {"score": 0, "output": None, "report_init_time": None},
                        "bleu": {"score": 0, "output": None, "report_init_time": None},
                        "ed": {"score": 0, "output": None, "report_init_time": None},
                        # "llm": {"score": 0, "output": None, "report_init_time": None},
                    },
                    "soft_list_metric": {
                        "len_weighted_bleu": {"score": 0, "output": None, "report_init_time": None},
                        "len_weighted_ed": {"score": 0, "output": None, "report_init_time": None},
                        "bleu": {"score": 0, "output": None, "report_init_time": None},
                        "ed": {"score": 0, "output": None, "report_init_time": None},
                        # "llm": {"score": 0, "output": None, "report_init_time": None},
                    }
                }
                if "output_stream_items" in self.reference_reports[task][0]:
                    reference_outputs = self.reference_reports[task][0]["output_stream_items"]
                else:
                    continue

                for report in reports[:N]:
                    candidate_outputs = report["output_stream_items"]

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="str",
                                                    similarity_func="bleu", len_weight=True)
                    if avg_stream_score > task_output_similarity["str_metric"]["len_weighted_bleu"]["score"]:
                        task_output_similarity["str_metric"]["len_weighted_bleu"]["score"] = avg_stream_score
                        task_output_similarity["str_metric"]["len_weighted_bleu"]["output"] = candidate_outputs
                        task_output_similarity["str_metric"]["len_weighted_bleu"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="str",
                                                    similarity_func="ed", len_weight=True)
                    if avg_stream_score > task_output_similarity["str_metric"]["len_weighted_ed"]["score"]:
                        task_output_similarity["str_metric"]["len_weighted_ed"]["score"] = avg_stream_score
                        task_output_similarity["str_metric"]["len_weighted_ed"]["output"] = candidate_outputs
                        task_output_similarity["str_metric"]["len_weighted_ed"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="str", similarity_func="bleu", len_weight=False)
                    if avg_stream_score > task_output_similarity["str_metric"]["bleu"]["score"]:
                        task_output_similarity["str_metric"]["bleu"]["score"] = avg_stream_score
                        task_output_similarity["str_metric"]["bleu"]["output"] = candidate_outputs
                        task_output_similarity["str_metric"]["bleu"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="str", similarity_func="ed", len_weight=False)
                    if avg_stream_score > task_output_similarity["str_metric"]["ed"]["score"]:
                        task_output_similarity["str_metric"]["ed"]["score"] = avg_stream_score
                        task_output_similarity["str_metric"]["ed"]["output"] = candidate_outputs
                        task_output_similarity["str_metric"]["ed"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="list",
                                                    similarity_func="bleu", hard_fields=True, len_weight=True)
                    if avg_stream_score > task_output_similarity["hard_list_metric"]["len_weighted_bleu"]["score"]:
                        task_output_similarity["hard_list_metric"]["len_weighted_bleu"]["score"] = avg_stream_score
                        task_output_similarity["hard_list_metric"]["len_weighted_bleu"]["output"] = candidate_outputs
                        task_output_similarity["hard_list_metric"]["len_weighted_bleu"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="list",
                                                    similarity_func="ed", hard_fields=True, len_weight=True)
                    if avg_stream_score > task_output_similarity["hard_list_metric"]["len_weighted_ed"]["score"]:
                        task_output_similarity["hard_list_metric"]["len_weighted_ed"]["score"] = avg_stream_score
                        task_output_similarity["hard_list_metric"]["len_weighted_ed"]["output"] = candidate_outputs
                        task_output_similarity["hard_list_metric"]["len_weighted_ed"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="list",
                                                    similarity_func="bleu", hard_fields=True, len_weight=False)
                    if avg_stream_score > task_output_similarity["hard_list_metric"]["bleu"]["score"]:
                        task_output_similarity["hard_list_metric"]["bleu"]["score"] = avg_stream_score
                        task_output_similarity["hard_list_metric"]["bleu"]["output"] = candidate_outputs
                        task_output_similarity["hard_list_metric"]["bleu"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="list",
                                                    similarity_func="ed", hard_fields=True, len_weight=False)
                    if avg_stream_score > task_output_similarity["hard_list_metric"]["ed"]["score"]:
                        task_output_similarity["hard_list_metric"]["ed"]["score"] = avg_stream_score
                        task_output_similarity["hard_list_metric"]["ed"]["output"] = candidate_outputs
                        task_output_similarity["hard_list_metric"]["ed"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="list",
                                                    similarity_func="bleu", hard_fields=False, len_weight=True)
                    if avg_stream_score > task_output_similarity["soft_list_metric"]["len_weighted_bleu"]["score"]:
                        task_output_similarity["soft_list_metric"]["len_weighted_bleu"]["score"] = avg_stream_score
                        task_output_similarity["soft_list_metric"]["len_weighted_bleu"]["output"] = candidate_outputs
                        task_output_similarity["soft_list_metric"]["len_weighted_bleu"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="list",
                                                    similarity_func="ed", hard_fields=False, len_weight=True)
                    if avg_stream_score > task_output_similarity["soft_list_metric"]["len_weighted_ed"]["score"]:
                        task_output_similarity["soft_list_metric"]["len_weighted_ed"]["score"] = avg_stream_score
                        task_output_similarity["soft_list_metric"]["len_weighted_ed"]["output"] = candidate_outputs
                        task_output_similarity["soft_list_metric"]["len_weighted_ed"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="list",
                                                    similarity_func="bleu", hard_fields=False, len_weight=False)
                    if avg_stream_score > task_output_similarity["soft_list_metric"]["bleu"]["score"]:
                        task_output_similarity["soft_list_metric"]["bleu"]["score"] = avg_stream_score
                        task_output_similarity["soft_list_metric"]["bleu"]["output"] = candidate_outputs
                        task_output_similarity["soft_list_metric"]["bleu"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                    avg_stream_score,stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="list",
                                                    similarity_func="ed", hard_fields=False, len_weight=False)
                    if avg_stream_score > task_output_similarity["soft_list_metric"]["ed"]["score"]:
                        task_output_similarity["soft_list_metric"]["ed"]["score"] = avg_stream_score
                        task_output_similarity["soft_list_metric"]["ed"]["output"] = candidate_outputs
                        task_output_similarity["soft_list_metric"]["ed"]["report_init_time"] = report['sandbox_info'][
                            'sandbox_init_time']

                output_similarity[task] = task_output_similarity

            avg_output_similarity = {
                "str_metric": {
                    "len_weighted_bleu":
                        sum(output_similarity[task]["str_metric"]["len_weighted_bleu"]['score'] for task in output_similarity) / len(output_similarity),
                    "len_weighted_ed":
                        sum(output_similarity[task]["str_metric"]["len_weighted_ed"]['score'] for task in output_similarity) / len(output_similarity),
                    "bleu":
                        sum(output_similarity[task]["str_metric"]["bleu"]['score'] for task in output_similarity) / len(output_similarity),
                    "ed":
                        sum(output_similarity[task]["str_metric"]["ed"]['score'] for task in output_similarity) / len(output_similarity),
                    # "llm":
                    #     sum(output_similarity[task]["str_metric"]["llm"] for task in output_similarity) / len(output_similarity),
                },
                "hard_list_metric": {
                    "len_weighted_bleu":
                        sum(output_similarity[task]["hard_list_metric"]["len_weighted_bleu"]['score'] for task in output_similarity) / len(output_similarity),
                    "len_weighted_ed":
                        sum(output_similarity[task]["hard_list_metric"]["len_weighted_ed"]['score'] for task in output_similarity) / len(output_similarity),
                    "bleu":
                        sum(output_similarity[task]["hard_list_metric"]["bleu"]['score'] for task in output_similarity) / len(output_similarity),
                    "ed":
                        sum(output_similarity[task]["hard_list_metric"]["ed"]['score'] for task in output_similarity) / len(output_similarity),
                    # "llm":
                    #     sum(output_similarity[task]["hard_list_metric"]["llm"] for task in output_similarity) / len(output_similarity),
                },
                "soft_list_metric": {
                    "len_weighted_bleu":
                        sum(output_similarity[task]["soft_list_metric"]["len_weighted_bleu"]['score'] for task in output_similarity) / len(output_similarity),
                    "len_weighted_ed":
                        sum(output_similarity[task]["soft_list_metric"]["len_weighted_ed"]['score'] for task in output_similarity) / len(output_similarity),
                    "bleu":
                        sum(output_similarity[task]["soft_list_metric"]["bleu"]['score'] for task in output_similarity) / len(output_similarity),
                    "ed":
                        sum(output_similarity[task]["soft_list_metric"]["ed"]['score'] for task in output_similarity) / len(output_similarity),
                    # "llm":
                    #     sum(output_similarity[task]["soft_list_metric"]["llm"] for task in output_similarity) / len(output_similarity),
                }
            }
            self.eval_results['eval_result'][N] = {
                "reference_log": self.reference_log,
                "candidate_log": self.candidate_log,
                "first_n": N,
                "avg_output_similarity": avg_output_similarity,
                "output_similarity": output_similarity
            }
        self._save_results()


if __name__ == '__main__':
    result_folder_path = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-21_19-43-43_human-written\test_log.json'
    agent_by_human_path = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-21_19-43-43_human-written\test_log.json'
    evaluator_output = EvalOutputSimilarity(agent_by_human_path, result_folder_path)
    evaluator_output.calculate_output_similarity()
