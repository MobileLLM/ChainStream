import os
import json
from collections import defaultdict

def extract_task_name(file_name):
    parts = file_name.split('_')
    task_name = parts[2]
    return task_name

def calculate_success_rate(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

    task_success_status = defaultdict(bool)
    unique_tasks = set()

    for file_name in json_files:
        task_name = extract_task_name(file_name)
        unique_tasks.add(task_name)

        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
        start_agent_status = data.get('start_agent', '')
        if start_agent_status == "[OK]":
            task_success_status[task_name] = True

    success_count = sum(task_success_status.values())
    total_task_count = len(unique_tasks)
    success_rate = (success_count / total_task_count) * 100 if total_task_count > 0 else 0

    return success_rate, total_task_count, success_count

def find_task_reports_folders(base_folder):
    task_reports_folders = []
    for root, dirs, files in os.walk(base_folder):
        if 'task_reports' in dirs:
            task_reports_folders.append(os.path.join(root, 'task_reports'))
    return task_reports_folders

def extract_folder_name(folder_path):
    return os.path.basename(os.path.dirname(folder_path))

def write_results_to_file(results, output_file):
    with open(output_file, 'w') as file:
        for result in results:
            file.write(result + '\n')

if __name__ == "__main__":
    base_folder_path = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result'
    task_reports_folders = find_task_reports_folders(base_folder_path)

    results = []
    for folder_path in task_reports_folders:
        success_rate, total_task_count, success_count = calculate_success_rate(folder_path)
        folder_name = extract_folder_name(folder_path)
        result = (f"Method: {folder_name}\n"
                  f"Tasks processed: {total_task_count}\n"
                  f"Agent started successfully: {success_count}\n"
                  f"Success rate: {success_rate:.2f}%\n")
        results.append(result)

    output_file = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result\test_result.txt'
    write_results_to_file(results, output_file)
