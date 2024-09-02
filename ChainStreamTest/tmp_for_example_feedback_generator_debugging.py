import json


def check_feedback_loop_history(log_path):
    with open(log_path) as log_file:
        log_data = json.load(log_file)

    all_task_report = log_data['task_reports']

    while True:
        for i, task_name in enumerate(all_task_report.keys()):
            print(f"{i + 1}. {task_name}")

        task_index = int(input("Enter task index: ")) - 1
        if task_index < 0 or task_index >= len(all_task_report):
            print("Invalid task index!")
            continue

        task_report = all_task_report[list(all_task_report.keys())[task_index]]

        for k, v in task_report[0].items():
            print(f"{k}: {v}")


if __name__ == '__main__':
    log_path = '/Users/liou/project/llm/ChainStream/ChainStreamSandBox/batch_simulation_scripts/result/2024-09-01_15-10-14_chainstream_feedback_1example/test_log.json'
    check_feedback_loop_history(log_path)
