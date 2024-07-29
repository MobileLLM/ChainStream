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

    def evaluate_similarity(self, agent1_example, agent2):
        distance = self.levenshtein_distance(agent1_example, agent2)
        max_distance = max(len(agent1_example), len(agent2))
        similarity = 1 - distance / max_distance
        return similarity

def extract_agent_code_from_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data.get("sandbox_info", {}).get("agent_code", "")

def find_task_name_from_filename(filename):
    parts = filename.split('_')
    for part in parts:
        if "Task" in part:
            return part
    return ""

if __name__ == "__main__":
    task_list = get_task_batch()
    result_folder_path = './result'
    result_output_path = './code_similarity.txt'

    with open(result_output_path, 'w', encoding='utf-8') as result_file:
        for subdir in os.listdir(result_folder_path):
            subdir_path = os.path.join(result_folder_path, subdir)
            if os.path.isdir(subdir_path):
                task_reports_path = os.path.join(subdir_path, 'task_reports')
                if os.path.isdir(task_reports_path):
                    task_similarities = {}
                    total_files = 0
                    processed_files = 0
                    for root, dirs, files in os.walk(task_reports_path):
                        total_files += len([file for file in files if file.endswith(".json")])
                    for root, dirs, files in os.walk(task_reports_path):
                        for file in files:
                            if file.endswith(".json"):
                                file_path = os.path.join(root, file)
                                agent_code2 = extract_agent_code_from_json(file_path)
                                task_name = find_task_name_from_filename(file)

                                if task_name in task_list:
                                    task_instance = task_list[task_name]()
                                    if hasattr(task_instance, 'agent_example'):
                                        agent_example = task_instance.agent_example
                                        evaluator = AgentComparator(task_list)
                                        similarity_score = evaluator.evaluate_similarity(agent_example, agent_code2)

                                        if task_name not in task_similarities:
                                            task_similarities[task_name] = similarity_score
                                        else:
                                            task_similarities[task_name] = max(task_similarities[task_name], similarity_score)

                                processed_files += 1
                                print(f"Processed {processed_files}/{total_files} files in {task_reports_path}")

                    for task_name, similarity_score in task_similarities.items():
                        result = f"Task: {task_name} in {subdir}, Max code similarity score: {similarity_score}\n"
                        print(result)
                        result_file.write(result)
