import os
import json
from ChainStreamSandBox.tasks import get_task_batch
from ChainStreamSandBox.sandbox_batch_interface import SandboxBatchInterface


class AgentComparator(SandboxBatchInterface):
    def __init__(self, task_list, repeat_time=1, result_path='./result/similarity_reports', task_log_path=None):
        super().__init__(task_list, repeat_time, result_path, task_log_path)

    def levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def evaluate_similarity(self, s1, s2):
        distance = self.levenshtein_distance(s1, s2)
        max_distance = max(len(s1), len(s2))
        if max_distance == 0:
            return 1.0
        similarity = 1 - distance / max_distance
        return similarity


def extract_data_from_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        output = data.get("output_stream_output", {})
        status = output.get("status", "")
        if status == "[OK] Task completed":
            return output.get("data", [])
        return []


def find_task_name_from_filename(filename):
    parts = filename.split('_')
    for part in parts:
        if "Task" in part:
            return part
    return ""


def get_data_from_task_reports(task_reports_path):
    task_data = {}
    for root, dirs, files in os.walk(task_reports_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                task_name = find_task_name_from_filename(file)
                data = extract_data_from_json(file_path)
                if task_name not in task_data:
                    task_data[task_name] = []
                task_data[task_name].extend(data)
    return task_data


if __name__ == "__main__":
    task_list = get_task_batch()
    result_folder_path = './result'
    result_output_path = 'result_similarity.txt'

    agent_by_human_path = os.path.join(result_folder_path, 'agent_by_human', 'task_reports')
    react_with_output_path = os.path.join(result_folder_path, 'react_with_output', 'task_reports')

    agent_by_human_data = get_data_from_task_reports(agent_by_human_path)
    react_with_output_data = get_data_from_task_reports(react_with_output_path)

    with open(result_output_path, 'w', encoding='utf-8') as result_file:
        for task_name in agent_by_human_data:
            if task_name in react_with_output_data:
                evaluator = AgentComparator(task_list)
                data1_list = agent_by_human_data[task_name]
                data2_list = react_with_output_data[task_name]

                max_similarity = 0
                for data1 in data1_list:
                    data1_str = json.dumps(data1, ensure_ascii=False)
                    print(data1_str)
                    for data2 in data2_list:
                        data2_str = json.dumps(data2, ensure_ascii=False)
                        print(data2_str)
                        similarity_score = evaluator.evaluate_similarity(data1_str, data2_str)
                        if similarity_score > max_similarity:
                            max_similarity = similarity_score

                result = f"Task: {task_name}, Max output similarity score: {max_similarity}\n"
                print(result)
                result_file.write(result)
