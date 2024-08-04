import json
from ChainStreamSandBox.evaluator.evaluator_base import EvaluatorBase
class EvalOutputSimilarity(EvaluatorBase):
    def __init__(self,base_folder):
        super().__init__()
        self.base_folder = base_folder
    def get_output_string(self, data):
        output = data.get("output_stream_output", {})
        status = output.get("status", "")
        if status == "[OK] Task completed":
            return json.dumps(output.get("data", []), ensure_ascii=False)
        return json.dumps([], ensure_ascii=False)
    def calculate_output_similarity(self, agent_by_human_path, result_output_path):
        agent_by_human_data_dict, task_folder1 = self.get_data_from_task_reports(agent_by_human_path)
        result_output = {}
        current_data_dict, task_folder2 = self.get_data_from_task_reports(self.base_folder)
        for folder_name1, task_data1 in agent_by_human_data_dict.items():
            for folder_name2, task_data2 in current_data_dict.items():
                for task_name in task_data1:
                    if task_name in task_data2:
                        data1_list = task_data1[task_name]
                        data2_list = task_data2[task_name]
                        for data1 in data1_list:
                            output_1_str = self.get_output_string(data1)
                            for data2 in data2_list:
                                output_2_str = self.get_output_string(data2)
                                similarity_score = self.evaluate_similarity(output_1_str, output_2_str)
                                key = (folder_name1, task_name)
                                if key not in result_output:
                                    result_output[key] = similarity_score
                                else:
                                    result_output[key] = max(result_output[key], similarity_score)
        formatted_results = [f"Folder: {folder_name1}, Task Name: {task_name}, Max Similarity: {similarity:.4f}"
                             for (folder_name1, task_name), similarity in result_output.items()]
        self.dump_eval_report(formatted_results, result_output_path)

if __name__ == '__main__':
    result_folder_path = r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result'
    agent_by_human_path =  r'C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\scripts\result\agent_by_human'
    evaluator_output = EvalOutputSimilarity(result_folder_path)
    evaluator_output.calculate_output_similarity(agent_by_human_path,result_output_path='./result_similarity_output.txt')
