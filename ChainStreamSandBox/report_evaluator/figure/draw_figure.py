import matplotlib
import matplotlib.pyplot as plt
import json
import os
import numpy as np


def get_score(eval_result, N, Metric, metric, task=None):
    if task is None:
        if Metric == 'code_similarity':
            score = eval_result[str(N)]['avg_code_similarity'][metric]
        elif Metric == 'output_similarity':
            key1, key2 = metric
            score = eval_result[str(N)]['avg_output_similarity'][key1][key2]
        else:
            raise ValueError('Invalid Metric')
    else:
        if Metric == 'code_similarity':
            score = eval_result[str(N)]['code_similarity'][task][metric]["score"]
        elif Metric == 'output_similarity':
            key1, key2 = metric
            score = eval_result[str(N)]['output_similarity'][task][key1][key2]["score"]
        else:
            raise ValueError('Invalid Metric')

    return score


def draw_different_generator_score_for_specific_Metric(all_eval_result, Metric):
    def get_different_N_for_specific_generator(eval_result, N_list, Metric, metric):
        all_scores = []
        for N in N_list:
            all_scores.append(get_score(eval_result, N, Metric, metric))
        return all_scores

    if Metric == 'code_similarity':
        metric_list = ['bleu', 'edit_distance', 'codebleu']
    elif Metric == 'output_similarity':
        metric_list = [
            ('str_metric', 'bleu'),
            ('str_metric', 'ed'),
            ('str_metric', 'len_weighted_bleu'),
            ('str_metric', 'len_weighted_ed'),
            ('hard_list_metric', 'bleu'),
            ('hard_list_metric', 'ed'),
            ('hard_list_metric', 'len_weighted_bleu'),
            ('hard_list_metric', 'len_weighted_ed'),
            ('soft_list_metric', 'bleu'),
            ('soft_list_metric', 'ed'),
            ('soft_list_metric', 'len_weighted_bleu'),
            ('soft_list_metric', 'len_weighted_ed'),
        ]
    else:
        raise ValueError('Invalid Metric')

    all_eval_result = all_eval_result[Metric]

    all_figure_data = {}
    for metric in metric_list:
        all_figure_data[metric] = {}
        for generator_name, generator_result in all_eval_result.items():
            if generator_result is not None:
                all_figure_data[metric][generator_name] = {}
                for N, _ in generator_result.items():
                    all_figure_data[metric][generator_name][int(N)] = get_score(generator_result, int(N), Metric, metric)

    plot_histograms(all_figure_data)





def load_all_results(base_file_path):
    Metric_list = ['success_rate', 'code_similarity', 'output_similarity']
    generator_list = ['result-chainstream-cot', 'result-python', 'result-chainstream-zero-shot',
                      'result-chainstream-one-shot', 'result-human-written', 'result-langchain-zero-shot']

    all_file_name = os.listdir(base_file_path)

    all_eval_results = {}
    for Metric in Metric_list:
        all_eval_results[Metric] = {}
        for generator in generator_list:
            tmp_path = Metric + '_' + generator + '.json'
            for filename in all_file_name:
                tmp_filename = '_'.join(filename.split('_')[2:])
                if tmp_path == tmp_filename:
                    with open(os.path.join(base_file_path, filename), 'r') as f:
                        eval_result = json.load(f)
                    all_eval_results[Metric][generator] = eval_result['eval_result']
            if all_eval_results[Metric].get(generator) is None:
                all_eval_results[Metric][generator] = None

    return all_eval_results


def plot_histograms(all_figure_data: dict):
    num_figures = len(all_figure_data)
    fig, axes = plt.subplots(num_figures, 1, figsize=(10, 5 * num_figures))

    # Ensure axes is iterable even if there's only one subplot
    if num_figures == 1:
        axes = [axes]

    for ax, (title, one_figure_data) in zip(axes, all_figure_data.items()):
        generators = list(one_figure_data.keys())
        num_generators = len(generators)

        # Bar properties
        width = 0.2  # Width of bars
        offsets = np.arange(num_generators)  # x locations for each generator

        for i, generator in enumerate(generators):
            one_generator_data = one_figure_data[generator]
            Ns = list(one_generator_data.keys())
            scores = list(one_generator_data.values())

            # Plot each generator's bars
            ax.bar(offsets[i] + np.arange(len(Ns)) * width, scores, width, label=f'{generator}')

            # Label each bar with the corresponding N
            for j, (n, score) in enumerate(zip(Ns, scores)):
                ax.text(offsets[i] + j * width, score + 0.02, f'N={n}', ha='center', va='bottom')

        # Set x-axis labels and title
        ax.set_xticks(offsets + (len(Ns) - 1) * width / 2)
        ax.set_xticklabels(generators)
        # ax.set_xlabel('Generator')
        ax.set_ylabel('Score')
        ax.set_title(title)
        # ax.legend(title='Generator')

    plt.tight_layout()
    plt.show()


def test_plot_histograms():
    # Example usage
    all_figure_data = {
        "Figure 1": {
            "Generator A": {1: 0.8, 2: 0.85, 3: 0.9},
            "Generator B": {1: 0.75, 2: 0.78, 3: 0.82},
            "Generator C": {1: 0.65, 2: 0.68, 3: 0.7}
        },
        "Figure 2": {
            "Generator X": {1: 0.88, 2: 0.92, 3: 0.95},
            "Generator Y": {1: 0.6, 2: 0.63, 3: 0.67}
        }
    }

    plot_histograms(all_figure_data)


if __name__ == '__main__':
    base_file_path = '/Users/liou/project/llm/ChainStream/ChainStreamSandBox/report_evaluator/result'
    eval_result = load_all_results(base_file_path)
    draw_different_generator_score_for_specific_Metric(eval_result, 'code_similarity')
    draw_different_generator_score_for_specific_Metric(eval_result, 'output_similarity')

