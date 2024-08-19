import json
import os
import datetime


def _load_sandbox_logs(log_paths: list):
    log_data = {}
    for log_path in log_paths:
        with open(log_path, 'r', encoding='utf-8') as file:
            tmp_log = json.load(file)
        log_data[log_path] = tmp_log
    return log_data


def _check_and_load_task_report(report_path):
    with open(report_path, 'r', encoding='utf-8') as file:
        report_data = json.load(file)
    key_list = ['sandbox_info', 'start_agent', 'start_task', 'input_stream_items', 'output_stream_items',
                'runtime_report', 'error_message']
    for key in key_list:
        if key not in report_data:
            print(f"Key {key} not found in report {report_path}")
            # raise ValueError(f"Key {key} not found in report {report_path}")
    return report_data


class EvaluatorBase:
    def __init__(self, log_path_list: list, save_name=None, save_folder=None):
        if isinstance(log_path_list, str):
            log_path_list = [log_path_list]
        self.log_path_list = log_path_list
        self.logs = _load_sandbox_logs(log_path_list)

        self.eval_results = {
            "eval_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "eval_log_path_list": self.log_path_list,
            "eval_class_name": self.__class__.__name__,
            "integrity_check_result": {},
            "eval_result": {}
        }

        self.reports = self._check_and_load_task_reports()

        self.save_name = save_name
        self.save_folder = save_folder

        if self.save_folder is not None and not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        self.save_path = os.path.join(
            self.save_folder, "result", datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + self.save_name + ".json") \
            if self.save_folder is not None else None



    def _check_and_load_task_reports(self):
        reports = {}
        for log_path, log in self.logs.items():
            repeat_time = log['repeat_time']
            run_times = log['run_times']
            task_report_count = {x: {"all": 0, "success": 0} for x in log['task_list']}
            task_report_data = {}
            for task, report_list in log['task_reports'].items():
                task_report_data[task] = []
                for report in report_list:
                    if "report_path" in report and report["report_path"] is not None:
                        task_report_count[task]["all"] += 1
                    if "error_msg" in report and report["error_msg"] == "success":
                        tmp_rel_path = os.path.relpath(report["report_path"], os.path.dirname(log_path))
                        if tmp_rel_path.startswith(".."):
                            tmp_rel_path = os.sep.join(tmp_rel_path.split(os.sep)[2:])
                        tmp_report_path = os.path.join(os.path.dirname(log_path), tmp_rel_path)
                        task_report_data[task].append(_check_and_load_task_report(tmp_report_path))
                        # TODO: check report format
                        # task_report_data[task].append(tmp_report_path)

                        task_report_count[task]["success"] += 1

            for task, report_count in task_report_count.items():
                if report_count["success"] < repeat_time:
                    raise ValueError(f"Task {task} in log {log_path} has less than {repeat_time} successful reports")
            self.eval_results["integrity_check_result"][
                log_path] = f"All {len(log['task_list'])} tasks have {repeat_time} successful reports in {run_times} runs"

            task_report_data = {k: sorted(v, key=lambda x: x['sandbox_info']['sandbox_init_time']) for k, v in
                                task_report_data.items()}
            reports[log_path] = task_report_data

        return reports

    def _save_results(self):
        if self.save_path is not None:
            if not os.path.exists(os.path.dirname(self.save_path)):
                os.makedirs(os.path.dirname(self.save_path))
            with open(self.save_path, 'w', encoding='utf-8') as file:
                json.dump(self.eval_results, file, indent=4)
            print(f"Evaluation results saved to {self.save_path}")
        else:
            print("Evaluation results not saved because save_folder is None")

    # def __del__(self):
    #     self._save_results()


# if __name__ == '__main__':
#     Evaluator_base = EvaluatorBase()
#     Evaluator_base.get_data_from_task_reports(
#         r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result')
