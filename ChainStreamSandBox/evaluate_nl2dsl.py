from .sandbox import SandBox
from ..NL2DSL.nl2dsl import NL2DSL
from tasks import ALL_TASKS
import json


def evaluate_nl2dsl():
    all_results = []
    for task in ALL_TASKS:
        task_description = task.task_description
        agent = NL2DSL(task_description)
        oj = SandBox(task, agent)
        res = oj.start_test_agent()
        all_results.append(res)
        json.dump(res, open(f"./results/{task.task_name}.json", "w"))
    return all_results


if __name__ == '__main__':
    all_results = evaluate_nl2dsl()
    print(all_results)
