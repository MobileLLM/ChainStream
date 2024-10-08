import traceback

from ChainStreamSandBox.sandbox import get_sandbox_class
import datetime
import os
import json
import tqdm
import inspect
from typing_extensions import Literal


class BatchInterfaceBase:
    def __init__(self, task_list, repeat_time=5, result_path='result', task_log_path=None, sandbox_type=None):
        if sandbox_type is None:
            raise ValueError("Please specify the sandbox_type for the batch interface")
        self.sandbox_type = sandbox_type

        self.task_list = task_list

        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if task_log_path is None:
            self.run_times = 1

            tmp_name = input("给这次的log路径取名，尽量是英文:")
            if hasattr(self, "model_name"):
                tmp_name = self.model_name + "_" + tmp_name
            self.report_path_base = os.path.join(result_path, self.start_time + "_" + tmp_name)
            if not os.path.exists(self.report_path_base):
                os.makedirs(self.report_path_base)

            self.repeat_time = repeat_time

            self.test_log = {}
            self._set_base_log()
        else:
            self.test_log = self._load_log(task_log_path)
            self.test_log['run_times'] = self.test_log['run_times'] + 1
            self.report_path_base = self.test_log['report_path_base']
            self.repeat_time = self.test_log['repeat_time']

            if self.test_log['test_description'] is None:
                self.test_log['test_description'] = [self._get_test_description()]
            else:
                self.test_log['test_description'].append(self._get_test_description())

            self.run_times = self.test_log["run_times"]

            if isinstance(self.test_log['start_time'], str):
                self.test_log['start_time'] = [self.test_log['start_time'],
                                               datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")]
            else:
                self.test_log['start_time'].append(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

    def _get_test_description(self):
        tmp_des = {
            "test_description": input("描述一下这次测试的目的，这段文字会被自动记录到log文件中，用于后续区分测试结果:"),
            "time": datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        }
        return tmp_des

    def _set_base_log(self):
        self.test_log = {
            "run_times": self.run_times,
            "start_time": self.start_time,
            "end_time": None,
            "report_path_base": self.report_path_base,
            "task_list": list(self.task_list),
            "repeat_time": self.repeat_time,
            "generator": self._set_generator_log(),
            "test_description": [self._get_test_description()],
            "task_reports": {
                xx: []
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
        try:
            for i in range(self.repeat_time):
                for task_name, task in self.task_list.items():
                    if self.run_times > 1:
                        success_times = 0
                        for log in self.test_log['task_reports'][task_name]:
                            if log['error_msg'] == "success":
                                success_times += 1
                        # if success_times >= len(self.test_log['task_reports'][task_name]):
                        if success_times > i:
                            pbar.update(1)
                            continue
                    pbar.set_description(f"Task: {task_name}, Repeat: {i + 1}")
                    self._one_task_step(task)
                    pbar.update(1)
                    self._save_log()

        except Exception as e:
            print(traceback.format_exc())
            print(f"ReRun Error: {e}")
        finally:
            self.test_log['end_time'] = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            self._save_log()

    def _save_log(self):
        with open(os.path.join(self.report_path_base, 'test_log.json'), 'w') as f:
            json.dump(self.test_log, f, indent=4)

    def _load_log(self, log_path):
        with open(log_path, 'r') as f:
            log = json.load(f)
        return log

    def _one_task_step(self, task):
        task = task()
        tmp_task_log = {
            "task_name": task.task_id,
            "start_time": datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
            "end_time": None,
            "error_msg": None,
        }
        loop_count, history, selected_example_name = None, None, None
        tmp_return = self.get_agent_for_specific_task(task)
        if len(tmp_return) == 3:
            agent_code, latency, tokens = tmp_return
        elif len(tmp_return) == 5:
            agent_code, latency, tokens, loop_count, history = tmp_return
        elif len(tmp_return) == 6:
            agent_code, latency, tokens, loop_count, history, selected_example_name = tmp_return
        else:
            raise ValueError(f"The return of get_agent_for_specific_task() should be a tuple of (agent_code, latency, tokens) or (agent_code, latency, tokens, _), but got {tmp_return}")

        try:
            if not os.path.exists(os.path.join(self.report_path_base, "task_reports")):
                os.makedirs(os.path.join(self.report_path_base, "task_reports"))

            sandbox_class = get_sandbox_class(self.sandbox_type)
            sandbox = sandbox_class(task, agent_code, save_path=os.path.join(self.report_path_base, "task_reports"),
                                    raise_exception=False, only_init_agent=False)
            report_path = sandbox.start_test_agent(return_report_path=True)
            tmp_task_log['report_path'] = report_path
        except Exception as e:
            tmp_task_log['error_msg'] = str(e)
            traceback.print_exc()
        else:
            tmp_task_log['error_msg'] = "success"
        finally:
            tmp_task_log['latency'] = latency
            tmp_task_log['loop_count'] = loop_count
            tmp_task_log['history'] = history
            tmp_task_log['selected_example_name'] = selected_example_name
            tmp_task_log['tokens'] = {
                "prompt_tokens": tokens[0],
                "completion_tokens": tokens[1],
            } if tokens is not None else None
            tmp_task_log['end_time'] = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            self.test_log['task_reports'][task.task_id].append(tmp_task_log)

    def get_agent_for_specific_task(self, task) -> str:
        raise NotImplementedError(
            "Please implement get_agent_for_specific_task() method in your BatchInterfaceBase subclass")


SandboxType = Literal["chainstream", "native_python_batch", "langchain_batch", "stream_interface"]


class SandboxBatchInterface(BatchInterfaceBase):
    def __init__(self, task_list, repeat_time=5, result_path='result', task_log_path=None,
                 sandbox_type: SandboxType = None):
        super().__init__(task_list, repeat_time, result_path, task_log_path, sandbox_type)

    def start(self):
        self._start()

    def get_agent_for_specific_task(self, task) -> object:
        raise NotImplementedError(
            "Please implement get_agent_for_specific_task() method in your BatchInterfaceBase subclass")
