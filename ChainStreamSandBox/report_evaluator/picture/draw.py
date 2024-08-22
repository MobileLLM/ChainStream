import os
import glob
import json


def draw(result_directory):
    metrics = ['success_rate', 'code_similarity', 'output_similarity']
    all_data = []

    for metric in metrics:
        json_files = glob.glob(os.path.join(result_directory, f'*{metric}_result*.json'))
        for file in json_files:
            base_name = os.path.splitext(file)[0]
            result_prefix = 'result-'
            generator = base_name.split(result_prefix, 1)[1]
            if not os.path.isfile(file):
                print(f"File not found: {file}")
                continue
            with open(file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            if metric == 'success_rate':
                results = data.get('eval_result', {})
                single_key = next(iter(results))
                eval_results = results[single_key]
                print(eval_results)
            else:
                eval_results = data.get('eval_result', {})
            for n, result in eval_results.items():
                data_list = get_score(metric, generator, n, result)
                all_data.extend(data_list)

    output_file = os.path.join(result_directory, 'all_data.json')
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(all_data, outfile, indent=4)

    print(f"All data saved to {output_file}")
    return all_data

def get_score(metric, generator, n, result):
    data = []
    if metric == 'code_similarity':
        avg_similarity = result.get('avg_code_similarity', {})
        code_similarity = result.get('code_similarity', {})
        tasks = []

        for task_name, metrics in code_similarity.items():
            task_scores = {}
            for metric_name, metric_data in metrics.items():
                task_scores[metric_name] = metric_data.get('score', 0.0)
            tasks.append({task_name: task_scores})
        metrics = list(avg_similarity.keys())
        values = [avg_similarity[m] for m in metrics]
        metrics_values = dict(zip(metrics, values))
        if int(n) != 5:
            data.append({"generator": generator, "n": n, "metrics_values": metrics_values})
        else:
            data.append({"generator": generator, "n": n, "tasks_values": tasks})
    if metric == "output_similarity":
        avg_similarity = result.get('avg_code_similarity', {})
        code_similarity = result.get('code_similarity', {})
        tasks = []

        for task_name, metrics in code_similarity.items():
            task_scores = {}
            for metric_name, metric_data in metrics.items():
                task_scores[metric_name] = metric_data.get('score', 0.0)
            tasks.append({task_name: task_scores})
        metrics = list(avg_similarity.keys())
        values = [avg_similarity[m] for m in metrics]
        metrics_values = dict(zip(metrics, values))
        if int(n) != 5:
            data.append({"generator": generator, "n": n, "metrics_values": metrics_values})
        else:
            data.append({"generator": generator, "n": n, "tasks_values": tasks})
        pass
    if metric == 'success_rate':
        eval_results = result.get('eval_result', {})
        for task_name, metrics in eval_results.items():
            task_scores = {}
            for metric_name, metric_data in metrics.items():
                task_scores[metric_name] = metric_data.get('success_rate', 0.0)
            data.append({"generator": generator, "n": n, "metrics_values": task_scores})

    return data