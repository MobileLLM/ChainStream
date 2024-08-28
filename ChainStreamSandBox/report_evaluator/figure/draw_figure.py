import matplotlib
import matplotlib.pyplot as plt
import json
import os
import numpy as np

from ChainStreamSandBox.tasks import get_task_with_data_batch

ALL_TASK_LIST = get_task_with_data_batch().keys()
print("ALL_TASK_LIST:", len(ALL_TASK_LIST))


def get_score(eval_result, N, Metric, metric, task=None):
    if N == -1:
        N = str(max([int(k) for k in eval_result.keys()]))
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


def draw_different_task_score_for_specific_Metric(all_eval_result, Metric):
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
        for task in ALL_TASK_LIST:
            all_figure_data[metric][task] = {}
            for generator_name, generator_result in all_eval_result.items():
                if generator_result is not None:
                    all_figure_data[metric][task][generator_name] = get_score(generator_result, -1, Metric, metric,
                                                                              task=task)

    plot_different_task_histograms(all_figure_data)


def plot_different_task_histograms(all_figure_data: dict):
    num_figures = len(all_figure_data)
    num_rows_per_figure = 4  # Number of rows per figure
    num_subplots = (num_figures + num_rows_per_figure - 1) // num_rows_per_figure  # Total number of figures needed

    figure_titles = list(all_figure_data.keys())

    for fig_index in range(num_subplots):
        # Calculate which subplots belong to the current figure
        start_index = fig_index * num_rows_per_figure
        end_index = min(start_index + num_rows_per_figure, num_figures)
        current_titles = figure_titles[start_index:end_index]

        num_tasks = len(ALL_TASK_LIST)

        # Create a figure with 4 rows and 1 column for the subplots
        fig, axs = plt.subplots(num_rows_per_figure, 1, figsize=(0.3 * num_tasks, 6 * num_rows_per_figure))
        axs = axs.flatten()

        for subplot_index, title in enumerate(current_titles):
            ax = axs[subplot_index]
            one_figure_data = all_figure_data[title]
            tasks = list(one_figure_data.keys())
            num_tasks = len(tasks)
            generators = list(one_figure_data[tasks[0]].keys())
            num_generators = len(generators)

            # Bar properties
            width = 0.15  # Width of bars
            offsets = np.arange(num_tasks)  # x locations for each task

            for i, generator in enumerate(generators):
                scores = [one_figure_data[task][generator] for task in tasks]
                # Plot each generator's bars within each task
                ax.bar(offsets + i * width, scores, width, label=f'{generator}')

            # Add vertical lines between tasks to separate groups of bars
            for x in np.arange(1, num_tasks):
                ax.axvline(x=x - 0.5 * (1 - width), color='grey', linestyle='--', linewidth=0.5)

            # Set x-axis labels and title
            ax.set_xticks(offsets + (num_generators - 1) * width / 2)
            ax.set_xticklabels(tasks, rotation=45, ha='right')
            ax.set_ylabel('Score')
            ax.set_title(title)
            ax.set_ylim(0, 1)  # Set y-axis range from 0 to 1
            ax.legend(title='Generator')

        # Hide any unused subplots in the current figure
        for subplot_index in range(len(current_titles), num_rows_per_figure):
            fig.delaxes(axs[subplot_index])

        plt.tight_layout()
        plt.show()


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
                    all_figure_data[metric][generator_name][int(N)] = get_score(generator_result, int(N), Metric,
                                                                                metric)

    plot_different_generator_histograms(all_figure_data)


def load_all_results(base_file_path):
    # Metric_list = ['success_rate', 'code_similarity', 'output_similarity']
    # generator_list = ['result-chainstream-cot', 'result-python', 'result-chainstream-zero-shot',
    #                   'result-chainstream-one-shot', 'result-human-written', 'result-langchain-zero-shot']
    Metric_list = ['output_similarity', 'code_similarity']
    generator_list = [
        "result-chainstream_zeroshot",
        "result-chainstream_1shot",
        'result-chainstream_feedback_0shot',
        'result-chainstream_feedback_1shot',
        'result-native_python_zeroshot',
        'result-human_written',
        "result-langchain_zeroshot",
        "result-chainstream_cot",
        "result-chainstream_cot_1shot",
    ]

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


def rename_generator(name):
    if name == "result-native_python_zeroshot":
        return "Py-0shot"
    elif name == "result-chainstream_feedback_0shot":
        return "CS-Feedback-0shot"
    elif name == "result-chainstream_feedback_1shot":
        return "CS-Feedback-1shot"
    elif name == "result-human_written":
        return "Human"
    elif name == "result-chainstream_zeroshot":
        return "CS-0shot"
    elif name == "result-chainstream_1shot":
        return "CS-1shot"
    elif name == "result-chainstream_cot":
        return "CS-Cot"
    elif name == "result-chainstream_cot_1shot":
        return "CS-Cot-1shot"
    elif name == "result-langchain_zeroshot":
        return "LC-0shot"
    raise ValueError("Invalid generator name")


def plot_different_generator_histograms(all_figure_data: dict):
    num_figures = len(all_figure_data)
    cols = 4  # Number of columns in the subplot grid
    rows = (num_figures + cols - 1) // cols  # Calculate the number of rows needed

    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    axes = axes.flatten()  # Flatten axes array for easy iteration

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
            ax.bar(offsets[i] + np.arange(len(Ns)) * width, scores, width, label=f'{rename_generator(generator)}')

            # Label each bar with the corresponding N
            for j, (n, score) in enumerate(zip(Ns, scores)):
                ax.text(offsets[i] + j * width, score + 0.02, f'N={n}', ha='center', va='bottom')

        # Set x-axis labels and title
        ax.set_xticks(offsets + (len(Ns) - 1) * width / 2)
        ax.set_xticklabels([rename_generator(generator) for generator in generators], rotation=45, ha='right')
        ax.set_ylabel('Score')
        ax.set_title(title)
        ax.set_ylim(0, 1)  # Set y-axis range from 0 to 1

    # Hide any unused subplots
    for ax in axes[num_figures:]:
        ax.set_visible(False)

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

    plot_different_generator_histograms(all_figure_data)


def _load_eval_result_for_success_rate(base_file_path):
    all_file_name = os.listdir(base_file_path)

    all_eval_results = []
    for filename in all_file_name:
        tmp_filename = '_'.join(filename.split('_')[2:5])
        if tmp_filename.split('.')[0] == "success_rate_result":
            with open(os.path.join(base_file_path, filename), 'r') as f:
                eval_result = json.load(f)
            all_eval_results.append(eval_result)

    return all_eval_results


def _draw_avg_success_rate(generator_avg_success_rate):
    def _rename_generator(generator):
        if generator == "chainstream_with_real_task_stdout_err_msg":
            return "CS-Feedback-0Shot"
        elif generator == "chainstream_real_task_framework_1shot":
            return "CS-Feedback-1shot"
        elif generator == "chainstream_human_written_code_task_with_data":
            return "Human"
        elif generator == 'chainstream_zero_shot':
            return "CS-0shot"
        elif generator == 'stream_python_zeroshot_task_with_data':
            return "Py-0shot"
        elif generator == 'chainstream_1shot':
            return "CS-1shot"
        elif generator == "chainstream_cot":
            return "CS-Cot"
        elif generator == "chainstream_cot_1shot":
            return "CS-Cot-1shot"
        elif generator == "stream_langchain_zeroshot":
            return "LC-0shot"
        elif generator == "stream_native_python_zeroshot":
            return "Py-0shot"
        else:
            raise ValueError("Invalid generator name")

    fig, ax = plt.subplots(1, 1)
    # ax = axs.flatten()[0]

    generators = list(generator_avg_success_rate.keys())
    num_generators = len(generators)

    # Bar properties
    width = 0.2  # Width of bars
    offsets = np.arange(num_generators)  # x locations for each generator

    for i, generator in enumerate(generators):
        one_generator_data = generator_avg_success_rate[generator]
        Ns = list(one_generator_data.keys())
        scores = list(one_generator_data.values())

        # Plot each generator's bars
        ax.bar(offsets[i] + np.arange(len(Ns)) * width, scores, width, label=f'{generator}')

        # Label each bar with the corresponding N
        for j, (n, score) in enumerate(zip(Ns, scores)):
            ax.text(offsets[i] + j * width, score + 0.02, f'N={n}', ha='center', va='bottom')

    # Set x-axis labels and title
    ax.set_xticks(offsets + (len(Ns) - 1) * width / 2)
    ax.set_xticklabels([_rename_generator(generator) for generator in generators], rotation=45, ha='right')
    ax.set_ylabel('Score')
    ax.set_title("Success Rate for all generators")
    ax.set_ylim(0, 100)  # Set y-axis range from 0 to 1
    # ax.legend(title='Generator')

    plt.tight_layout()
    plt.show()


def _draw_success_rate_for_tasks(generator_success_rate_for_tasks):
    one_figure_data = generator_success_rate_for_tasks
    generators = list(one_figure_data.keys())
    num_generators = len(generators)
    all_tasks = set()
    for generator in generators:
        all_tasks.update(one_figure_data[generator].keys())
    num_tasks = len(all_tasks)
    all_tasks = list(all_tasks)

    fig, ax = plt.subplots(1, 1, figsize=(0.3 * num_tasks, 6))
    # ax = axs.flatten()[0]

    # Bar properties
    width = 0.15  # Width of bars
    offsets = np.arange(num_tasks)  # x locations for each task

    for i, generator in enumerate(generators):
        scores = [not one_figure_data[generator][task] if task in one_figure_data[generator] else 0 for task in
                  all_tasks]
        # Plot each generator's bars within each task
        ax.bar(offsets + i * width, scores, width, label=f'{generator}')

    # Add vertical lines between tasks to separate groups of bars
    for x in np.arange(1, num_tasks):
        ax.axvline(x=x - 0.5 * (1 - width), color='grey', linestyle='--', linewidth=0.5)

    # Set x-axis labels and title
    ax.set_xticks(offsets + (num_generators - 1) * width / 2)
    ax.set_xticklabels(all_tasks, rotation=45, ha='right')
    ax.set_ylabel('Score')
    ax.set_title("Not success for each task")
    ax.set_ylim(0, 1)  # Set y-axis range from 0 to 1
    ax.legend(title='Generator')

    plt.tight_layout()
    plt.show()


def draw_success_rate(base_file_path):
    tmp_all_eval_results = _load_eval_result_for_success_rate(base_file_path)

    all_generator_name = []
    all_eval_results = {}
    for tmp_eval_result in tmp_all_eval_results:
        tmp_gen_list = tmp_eval_result['integrity_check_result']
        for tmp_gen in tmp_gen_list.keys():
            if tmp_gen not in all_generator_name:
                all_generator_name.append(tmp_gen)
                all_eval_results[tmp_gen.split(os.sep)[-2][20:]] = tmp_eval_result['eval_result'][tmp_gen]
            else:
                raise ValueError("Duplicate generator name")

    generator_avg_success_rate = {}
    generator_success_rate_for_tasks = {}

    for gen_name, gen_results in all_eval_results.items():
        generator_avg_success_rate[gen_name] = {}
        generator_success_rate_for_tasks[gen_name] = {}
        for N, gen_N_results in gen_results.items():
            generator_avg_success_rate[gen_name][N] = gen_N_results['success_rate']
            print(
                f"Gen: {gen_name}, N: {N}, Success Rate: {gen_N_results['success_rate']} ({gen_N_results["success_count"]} / {gen_N_results['total_task_count']})")

            for task, task_bool in gen_N_results['success_details'].items():
                if task not in generator_success_rate_for_tasks[gen_name]:
                    generator_success_rate_for_tasks[gen_name][task] = task_bool
                else:
                    generator_success_rate_for_tasks[gen_name][task] = generator_success_rate_for_tasks[gen_name][
                                                                           task] or task_bool

    _draw_avg_success_rate(generator_avg_success_rate)
    _draw_success_rate_for_tasks(generator_success_rate_for_tasks)


if __name__ == '__main__':
    base_file_path = '/Users/liou/project/llm/ChainStream/ChainStreamSandBox/report_evaluator/result'
    eval_result = load_all_results(base_file_path)
    # draw_different_generator_score_for_specific_Metric(eval_result, 'code_similarity')

    draw_different_generator_score_for_specific_Metric(eval_result, 'output_similarity')
    draw_different_task_score_for_specific_Metric(eval_result, 'output_similarity')

    draw_success_rate(base_file_path)
