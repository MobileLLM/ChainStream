from sandbox import SandBox
import datetime
import os
import json
import tqdm
import inspect


class BatchInterfaceBase:
    def __init__(self, task_list, output_path, repeat_time=5, result_path='./result', task_log_path=None):
        self.task_list = task_list
        self.output_path = output_path

        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if task_log_path is None:
            self.run_times = 1

            self.report_path = os.path.join(result_path, self.start_time)

            self.repeat_time = repeat_time

            self.test_log = {}
            self._set_base_log()
        else:
            self.test_log = self._load_log(task_log_path)
            self.test_log['run_times'] = self.test_log['run_times'] + 1
            self.report_path = self.test_log['report_path']
            self.repeat_time = self.test_log['repeat_time']

            if isinstance(self.test_log['start_time'], str):
                self.test_log['start_time'] = [self.test_log['start_time'],
                                               datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            else:
                self.test_log['start_time'].append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _set_base_log(self):
        self.test_log = {
            "run_times": self.run_times,
            "start_time": self.start_time,
            "end_time": None,
            "report_path": self.report_path,
            "task_list": self.task_list,
            "output_path": self.output_path,
            "repeat_time": self.repeat_time,
            "generator": self._set_generator_log(),
            "task_log": {
                xx.__name__: []
                for xx in self.task_list
            }
        }

    def _set_generator_log(self) -> dict:
        generator_log = {
            "generator_class_name": self.__class__.__name__,
            "generator_class_file": inspect.getfile(inspect.getmodule(self.__class__)),
            "generator_code": inspect.getsource(self.get_agent_for_specific_task),
        }
        return generator_log

    def _start(self):
        pbar = tqdm.tqdm(total=len(self.task_list) * self.repeat_time)

        for i in range(self.repeat_time):
            for task in self.task_list:
                if self.run_times > 1:
                    success_times = 0
                    for log in self.test_log['task_log'][task.__name__]:
                        if log['error_msg'] == "success":
                            success_times += 1
                    if success_times >= len(self.test_log['task_log'][task.__name__]):
                        continue
                pbar.set_description(f"Task: {task.__name__}, Repeat: {i + 1}")
                self._one_task_step(task)
                pbar.update(1)

        self.test_log['end_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_log()

    def _save_log(self):
        with open(os.path.join(self.report_path, 'test_log.json'), 'w') as f:
            json.dump(self.test_log, f, indent=4)

    def _load_log(self, log_path):
        with open(log_path, 'r') as f:
            log = json.load(f)
        return log

    def _one_task_step(self, task):
        tmp_task_log = {
            "task_name": task.__name__,
            "start_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": None,
            "error_msg": None,
        }
        agent_code = self.get_agent_for_specific_task(task)
        try:
            sandbox = SandBox(task, agent_code)
            report_path = sandbox.start_test_agent(return_report_path=True)
            tmp_task_log['report_path'] = report_path
        except Exception as e:
            tmp_task_log['error_msg'] = str(e)
        else:
            tmp_task_log['error_msg'] = "success"
        finally:
            tmp_task_log['end_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.test_log['task_log'][task.__name__].append(tmp_task_log)

    def get_agent_for_specific_task(self, task) -> str:
        raise NotImplementedError(
            "Please implement get_agent_for_specific_task() method in your BatchInterfaceBase subclass")


class SandboxBatchInterface(BatchInterfaceBase):
    def __init__(self, task_list, output_path, repeat_time=5, result_path='./result', task_log_path=None):
        super().__init__(task_list, output_path, repeat_time, result_path, task_log_path)

    def start(self):
        self._start()

    def get_agent_for_specific_task(self, task) -> str:
        raise NotImplementedError(
            "Please implement get_agent_for_specific_task() method in your BatchInterfaceBase subclass")
