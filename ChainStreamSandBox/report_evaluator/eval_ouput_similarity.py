import os
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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

        score_record_for_loop_count = {}

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
                    raise RuntimeError("Reference log does not have output_stream_items")

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

                    avg_stream_score, stream_similarity = cal_multi_stream_similarity(reference_outputs, candidate_outputs, list_mode="list",
                                                    similarity_func="bleu", hard_fields=True, len_weight=True)
                    if task not in score_record_for_loop_count:
                        score_record_for_loop_count[task] = {}
                    score_record_for_loop_count[task][report['sandbox_info']['sandbox_init_time']] = avg_stream_score

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

            assert len(output_similarity) == len(TASK_WITH_DATA_LIST)

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

        # cal_loop_count_score(score_record_for_loop_count, self.candidate_log)


def cal_loop_count_score(score_record_for_loop_count, log_path):
    with open(log_path, "r") as f:
        log_data = json.load(f)

    loop_record = {}
    tot_token = {"prompt_tokens": [], "completion_tokens": []}
    tot_latency = []
    tot_loop = []
    count = 0

    loop_token_latency_record = {}
    for task_name, reports in log_data['task_reports'].items():
        if task_name not in TASK_WITH_DATA_LIST:
            continue

        for report in reports:
            report_path = report['report_path']
            loop_count = report['loop_count']
            tokens = report['tokens']
            latency = report['latency']
            with open(report_path, "r") as f:
                tmp_report = json.load(f)
                tmp_report_init_time = tmp_report['sandbox_info']['sandbox_init_time']
            score = score_record_for_loop_count[task_name][tmp_report_init_time]
            tmp_record = {
                'log_path': report_path,
                'path': report_path,
                'task': task_name,
                'tokens': tokens,
                'latency': latency,
                'loop_count': loop_count,
                'score': score
            }

            count += 1
            if loop_count not in loop_record:
                loop_record[loop_count] = []
            loop_record[loop_count].append(score)

            tot_token["prompt_tokens"].append(tokens['prompt_tokens'])
            tot_token["completion_tokens"].append(tokens['completion_tokens'])
            tot_latency.append(latency)
            tot_loop.append(loop_count)

            if task_name not in loop_token_latency_record:
                loop_token_latency_record[task_name] = []
            loop_token_latency_record[task_name].append(tmp_record)

    with open("loop_token_latency_record.json", "w") as f:
        json.dump(loop_token_latency_record, f)

    print(f"Tot count {count}")
    print(f"Average latency {sum(tot_latency) / len(tot_latency)}")
    # if len(tot_loop) > 0:
    #     print(f"Average loop {sum(tot_loop) / len(tot_loop)}")
    print(f"Average prompt tokens {sum(tot_token['prompt_tokens']) / len(tot_token['prompt_tokens'])}")
    print(f"Average completion tokens {sum(tot_token['completion_tokens']) / len(tot_token['completion_tokens'])}")

    sorted_keys = sorted(loop_record.keys())
    sorted_values = [loop_record[key] for key in sorted_keys]

    plt.boxplot(sorted_values, labels=sorted_keys)
    plt.xlabel('Loop count')
    plt.ylabel('List dp bleu score')
    # plt.title(f"")
    plt.show()

    a = 1


if __name__ == '__main__':
    # ['result-native_python_zeroshot', 'result-chainstream_with_real_task', 'result-human_written', "result-chainstream_zeroshot", "result-chainstream_1shot"]
    tmp_list = {
        # "result-native_python_zeroshot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-01-29_native_python_zeroshot/test_log.json",
        # "result-native_python_oneshot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_09-25-50_native_python_oneshot/test_log.json",
        # "result-langchain_zeroshot": "/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-41-03_langchain_zeroshot/test_log.json",
        # "result-langchain_oneshot": "/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_01-45-37_langchain_oneshot/test_log.json",
        # # "result-chainstream_feedback_1shot_0example_old": "/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-02_15-20-40_chainstream_feedback_1shot_0example_old/test_log.json",
        # "result-chainstream_feedback_0shot_0example_old": r'/Users/liou/Desktop/2024-09-03_19-36-37_chainstream-0-shot-0-example/test_log_20240904_141552_concat_log.json',
        # # "result-chainstream_feedback_0shot_0example_new": "/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-02_15-58-34_chainstream_feedback_0shot_0example_new/test_log.json",
        # "result-chainstream_feedback_0shot_1example_new": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/test_log_20240904_200721_concat_log_for_feedback_0shot_1llm.json",
        # "result-chainstream_feedback_0shot_2example_new": '/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/test_log_20240904_201310_concat_log_for_feedback_0shot_2llm.json',
        # "result-chainstream_feedback_0shot_3example_new": '/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/test_log_20240904_201434_concat_log_for_feedback_0shot_3llm.json',
        #
        # "result-chainstream_fewshot_0shot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-11-04_chainstream_fewshot_0shot/test_log.json",
        # "result-chainstream_fewshot_1shot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-10-46_chainstream_fewshot_1shot/test_log.json",
        "result-chainstream_fewshot_2shot": r"/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_22-49-44_chainstream_fewshot_2shot/test_log.json",
        # "result-chainstream_fewshot_3shot": r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-05-59_chainstream_fewshot_3shot/test_log.json',
        #
        # "result-chainstream_fewshot_1shot_llm": r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_22-54-14_chainstream_fewshot_1shot_llm/test_log.json',
        # "result-chainstream_fewshot_2shot_llm": r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_22-54-19_chainstream_fewshot_2shot_llm/test_log.json',
        # "result-chainstream_fewshot_3shot_llm": r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_22-54-27_chainstream_fewshot_3shot_llm/test_log.json',
        #
        # # "result-human_written": r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-00-50_chainstream_human_written/test_log.json',
        # "result-gpt-4o": "/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-01-40_gpt-4o_native_gpt4o/test_log.json",
        # # "result-gpt-4o-new": "/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_04-36-20_gpt-4o_native_gpt4o/test_log.json",
        # "result-gpt-4": "/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-04_20-25-46_gpt-4_native_gpt4/test_log.json",
        # "result-gpt-4-new": "/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_04-42-59_gpt-4_/test_log.json",
        #
        # "result-chainstream_feedback_0example_without_stdout": r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_05-42-28_chainstream_feedback_0example_without_stdout/test_log.json',
        # "result-chainstream_feedback_0example_without_output": r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_05-41-40_chainstream_feedback_0example_without_output/test_log.json',
        # "result-chainstream_feedback_0example_without_err": r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-05_05-38-35_chainstream_feedback_0example_without_err/test_log.json',
    }
    # result_folder_path = r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-08-23_19-56-23_chainstream_human_written_code_task_with_data/test_log.json'
    agent_by_human_path = r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-03_17-00-50_chainstream_human_written/test_log.json'

    first_n_list = {
        "result-native_python_zeroshot": [1, 3, 5],
        "result-native_python_oneshot": [1, 3, 5],
        "result-langchain_zeroshot": [1, 3, 5],
        "result-langchain_oneshot": [1, 3, 5],
        "result-chainstream_feedback_1shot_0example_old": [1, 2, 3],
        "result-chainstream_feedback_0shot_0example_old": [1, 3, 5],
        "result-chainstream_feedback_0shot_0example_new": [1],
        "result-chainstream_feedback_0shot_1example_new": [1, 3, 5],
        "result-chainstream_feedback_0shot_2example_new": [1, 3, 5],
        "result-chainstream_feedback_0shot_3example_new": [1, 3, 5],

        # "result-chainstream_feedback_1shot_0example": [1],

        "result-chainstream_fewshot_0shot": [1, 3, 5],
        "result-chainstream_fewshot_1shot": [1, 3, 5],
        "result-chainstream_fewshot_2shot": [1, 3, 5],
        "result-chainstream_fewshot_3shot": [1, 3, 5],

        "result-chainstream_fewshot_1shot_llm": [1],
        "result-chainstream_fewshot_2shot_llm": [1],
        "result-chainstream_fewshot_3shot_llm": [1],

        "result-chainstream_feedback_0example_without_stdout": [1],
        "result-chainstream_feedback_0example_without_output": [1],
        "result-chainstream_feedback_0example_without_err": [1],

        "result-gpt-4": [1, 3, 5],
        "result-gpt-4-new": [1, 3, 5],
        "result-gpt-4o": [1, 3, 5],
        "result-gpt-4o-new": [1, 3, 5],
        "result-human_written": [1],
    }

    for gen_name,tmp_path in tmp_list.items():
        evaluator_output = EvalOutputSimilarity(agent_by_human_path, tmp_path, save_name="output_similarity_" + gen_name)
        evaluator_output.calculate_output_similarity(first_n=first_n_list[gen_name])
