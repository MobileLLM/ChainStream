from sandbox import SandBox
import datetime
import os
import json
import tqdm


class BatchInterfaceBase:
    def __init__(self, task_list, output_path):
        self.task_list = task_list
        self.output_path = output_path

        self.results = []
        self.test_log = {}

    def start(self):
        pass

    def get_agent_for_specific_task(self, task) -> str:
        raise NotImplementedError()


class TestExampleAgent(BatchInterfaceBase):
    def __init__(self, task_list, output_path):
        super().__init__(task_list, output_path)
