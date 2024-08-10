from ChainStreamSandBox.evaluator.evaluator_base import EvaluatorBase
from ChainStreamSandBox.tasks import get_task_batch


class EvalCodeSimilarity(EvaluatorBase):
    def __init__(self, base_folder):
        super().__init__()
        self.base_folder = base_folder
        self.task_list = get_task_batch()

    def calculate_code_similarity(self, result_output_path):
        task_data_dict, task_folder = self.get_data_from_task_reports(self.base_folder)
        task_similarities = {}
        for folder_name, task_data in task_data_dict.items():
            for task_name, data_list in task_data.items():
                if task_name in self.task_list:
                    task_instance = self.task_list[task_name]()
                    if hasattr(task_instance, 'agent_example'):
                        agent_example = task_instance.agent_example
                        for json_data in data_list:
                            agent_code2 = json_data.get("sandbox_info", {}).get("agent_code", "")
                            similarity_score = self.evaluate_similarity(agent_example, agent_code2)
                            key = (folder_name, task_name)
                            if key not in task_similarities:
                                task_similarities[key] = similarity_score
                            else:
                                task_similarities[key] = max(task_similarities[key], similarity_score)
        formatted_results = [f"Folder: {folder_name}, Task Name: {task_name}, Max Similarity: {similarity:.4f}"
                             for (folder_name, task_name), similarity in task_similarities.items()]
        self.dump_eval_report(formatted_results, result_output_path)


if __name__ == "__main__":
    base_folder_path = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result'
    evaluator_code = EvalCodeSimilarity(base_folder_path)
    evaluator_code.calculate_code_similarity(result_output_path='./code_similarity_report.txt')
