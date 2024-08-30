import os
from ChainStreamSandBox.report_evaluator.evaluator_base import EvaluatorBase
from ChainStreamSandBox.report_evaluator.utils import *
from ChainStreamSandBox.tasks import get_task_with_data_batch

TASK_WITH_DATA_LIST = get_task_with_data_batch().keys()


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
                if task not in TASK_WITH_DATA_LIST:

                    continue
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
                    candidate_outputs = report["output_stream_items"] if "output_stream_items" in report else {}

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
    # ['result-native_python_zeroshot', 'result-chainstream_with_real_task', 'result-human_written', "result-chainstream_zeroshot", "result-chainstream_1shot"]
    tmp_list = {
        # "result-chainstream_cot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-25_09-32-44_chainstream_cot/test_log.json",
        # "result-chainstream_cot_1shot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-26_16-45-07_chainstream_cot_1shot/test_log.json",
        # "result-chainstream_zeroshot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-23_17-32-10_chainstream_zero_shot/test_log.json",
        # "result-chainstream_1shot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-24_04-27-20_chainstream_1shot/test_log.json" ,
        # "result-chainstream_feedback_1shot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-24_04-30-23_chainstream_real_task_framework_1shot/test_log.json",
        # "result-native_python_zeroshot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-25_09-31-41_stream_native_python_zeroshot/test_log.json",
        # "result-langchain_zeroshot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-25_10-38-14_stream_langchain_zeroshot/test_log.json",
        # "result-native_python_zeroshot": r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-29_18-59-07_native_python_zero_shot\test_log.json',
        # "result-langchain_zeroshot": r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-29_19-02-44_langchain_zero_shot\test_log.json',
        # "result-gpt-4o": r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-29_19-04-07_gpt-4o_native_gpt_4o\test_log.json',
        # "result-chainstream_zeroshot": r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-29_19-05-29_chainstream_zero_shot\test_log.json',
        # "result-chainstream_cot": r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-29_19-09-40_chainstream_cot_zero_shot\test_log.json',
        # "result-chainstream_feedback_0shot": r"C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-29_02-51-10_chainstream_with_real_task_0_shot\test_log.json"
        "result-human_written": r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-30_20-38-19_human_written_test_after_fixing\test_log.json'
    }
    # result_folder_path = r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-23_19-56-23_chainstream_human_written_code_task_with_data/test_log.json'
    agent_by_human_path = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\batch_simulation_scripts\result\2024-08-30_20-38-19_human_written_test_after_fixing\test_log.json'

    first_n_list = {
        "result-human_written": [1],

        # "result-chainstream_1shot": [1, 3, 5],
        # "result-chainstream_feedback_1shot": [1, 2],
        # "result-chainstream_cot_1shot": [1, 3, 5],
        "result-native_python_zeroshot": [1, 3, 5],
        "result-chainstream_feedback_0shot": [1, 2, 3],
        "result-gpt-4o": [1, 3, 5],
        "result-chainstream_zeroshot": [1, 3, 5],
        "result-langchain_zeroshot": [1, 3, 5],
        "result-chainstream_cot": [1, 3, 5]
    }

    for gen_name,tmp_path in tmp_list.items():
        evaluator_output = EvalOutputSimilarity(agent_by_human_path, tmp_path, save_name="output_similarity_" + gen_name)
        evaluator_output.calculate_output_similarity(first_n=first_n_list[gen_name])
