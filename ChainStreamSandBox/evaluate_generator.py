import os
import json
from sandbox import SandBox
from AgentGenerator.agent_generator import AgentGenerator
from tasks import ALL_TASKS

def evaluate_generator():
    results_dir = './results'
    os.makedirs(results_dir, exist_ok=True)
    all_results = []
    for task_name, task_class in ALL_TASKS.items():
        task_config = task_class()
        task_description = task_config.task_description
        agent_code = AgentGenerator().generate_dsl(task_description)
        print(agent_code)
        oj = SandBox(task_config, agent_code)
        try:
            oj.start_test_agent()
            res = oj.result
        except Exception as e:
            print(f"Error occurred while testing agent for task {task_name}: {e}")
            res = {"error": str(e)}
        with open(f"{results_dir}/{task_name}.json", "w") as f:
            json.dump(res, f)

    return all_results

if __name__ == '__main__':
    all_results = evaluate_generator()
    print(all_results)
