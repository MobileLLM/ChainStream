import matplotlib
import matplotlib.pyplot as plt
import json
import os
import numpy as np
import matplotlib.cm as cm

from ChainStreamSandBox.tasks import get_task_with_data_batch
from ChainStreamSandBox.tasks.tmp_task_instances import get_all_task_instances

ALL_TASK_LIST = get_task_with_data_batch().keys()
print("ALL_TASK_LIST:", len(ALL_TASK_LIST))
ALL_TASK_INSTANCES_LIST = get_all_task_instances()
ALL_TASK_TAG_LIST = {k: v.task_tag for k, v, in ALL_TASK_INSTANCES_LIST.items()}


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


def generate_colors(num_colors):
    """
    Generate a list of distinct colors.

    Parameters:
    - num_colors: The number of distinct colors needed.

    Returns:
    A list of color codes.
    """
    colors = cm.get_cmap('tab20', num_colors)
    return [colors(i) for i in range(num_colors)]


def plot_task_tag_histograms(data_dict, title):
    """
    Plot histograms with multiple subplots using the new data_dict structure, arranged vertically.

    Parameters:
    - data_dict: A dictionary with keys as subplot titles and values as dictionaries of tags,
      where each tag has a dictionary of generator names and their corresponding scores.

    Example of data_dict structure:
    {
        "Subplot 1": {
            "Tag1": {"Gen1": 10, "Gen2": 15},
            "Tag2": {"Gen1": 8, "Gen2": 12}
        },
        "Subplot 2": {
            "Tag1": {"Gen1": 20, "Gen2": 18},
            "Tag2": {"Gen1": 25, "Gen2": 22}
        }
    }
    """
    def _rename(name):
        if name == "chainstream_feedback_0shot_0example_old":
            return "Ours (0-shot)"
        elif name == "chainstream_feedback_0shot_1example_new":
            return "Ours (1-shot)"
        elif name == "chainstream_feedback_0shot_2example_new":
            return "Ours (2-shot)"
        elif name == "chainstream_feedback_0shot_3example_new":
            return "Ours (3-shot)"
        elif name == "chainstream_fewshot_0shot":
            return "Ours without iteration (0-shot)"
        elif name == "chainstream_fewshot_1shot":
            return "Ours without iteration (1-shot)"
        elif name == "chainstream_fewshot_2shot":
            return "Ours without iteration (2-shot)"
        elif name == "chainstream_fewshot_3shot":
            return "Ours without iteration (3-shot)"
        elif name == "gpt-4o":
            return "GPT-4o"
        elif name == "gpt-4":
            return "GPT-4"
        elif name == "langchain_oneshot":
            return "LangChain (1-shot)"
        elif name == "langchain_zeroshot":
            return "LangChain (0-shot)"
        elif name == "native_python_zeroshot":
            return "Python (0-shot)"
        elif name == "native_python_oneshot":
            return "Python (1-shot)"
        else:
            raise ValueError(f"Invalid name {name}")

    # Determine the number of subplots needed
    def add_labels(ax, rects, labels, y_offset, rotation=0):
        for rect, label in zip(rects, labels):
            x_position = rect.get_x() + rect.get_width() / 2.
            ax.text(x_position, y_offset, label, ha='center', va='top', rotation=rotation)

    # Generate individual plots for each subplot
    for title, tags_data in data_dict.items():
        tags = list(tags_data.keys())
        if len(tags) == 2:
            tags.sort(reverse=True)
        else:
            tags.sort()

        generator_names = {generator_name.split("result-")[-1] for tag_data in tags_data.values() for generator_name in
                           tag_data}
        generator_names = sorted(list(generator_names))

        num_generators = len(generator_names)
        colors = generate_colors(num_generators)
        generator_color_map = {name: colors[i] for i, name in enumerate(generator_names)}

        x = np.arange(len(tags))  # the label locations
        width = 0.8 / num_generators  # the width of the bars

        fig, ax = plt.subplots(figsize=(8, 5))

        max_height = 0
        all_rects = []

        # Plotting each bar
        for i, generator_name in enumerate(generator_names):
            values = [tags_data[tag].get("result-" + generator_name, 0) for tag in tags]
            rects = ax.bar(x + i * width, values, width, label=_rename(generator_name),
                           color=generator_color_map[generator_name])
            all_rects.append(rects)
            max_height = max(max_height, max(values))

        ax.set_title(title)

        # Set x-ticks with two levels of labels
        ax.set_xticks(x + width * (num_generators - 1) / 2)
        # ax.set_xticklabels(tags)

        # Add bar labels below the x-axis, slightly above the tag labels
        bar_label_y_offset = -max_height * 0.05
        # for rects in all_rects:
        #     add_labels(ax, rects, [_rename(x) for x in generator_names], y_offset=bar_label_y_offset,
        #                rotation=45)
        # for gen_name in generator_names:
        #     add_labels(ax, gen_name, y_offset=bar_label_y_offset, rotation=45)

        # Add tag labels below the bar labels
        tag_label_y_offset = bar_label_y_offset - max_height * 0.05
        for i, tag in enumerate(tags):
            ax.text(x[i] + width * (num_generators - 1) / 2, tag_label_y_offset, tag, ha='center', va='top',
                    fontsize=10)

        ax.legend(title="Generators")
        ax.set_ylim(tag_label_y_offset - max_height * 0.1, max_height * 1.1)  # Adjust y-limit to make space for labels
        plt.show()


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
    all_figure_data_with_tag = {}
    for metric in metric_list:
        all_figure_data[metric] = {}

        for task in ALL_TASK_LIST:
            all_figure_data[metric][task] = {}
            for generator_name, generator_result in all_eval_result.items():
                if generator_result is not None:
                    all_figure_data[metric][task][generator_name] = get_score(generator_result, -1, Metric, metric,
                                                                              task=task)

    plot_different_task_histograms(all_figure_data)

    task_tag_score = {k: _process_for_task_tag_plot(v) for k, v in all_figure_data.items()}

    print(task_tag_score[('hard_list_metric', 'bleu')]['Difficulty'])

    plot_task_tag_histograms(task_tag_score[('hard_list_metric', 'bleu')], "('hard_list_metric', 'bleu')")
    # plot_task_tag_histograms(task_tag_score[('hard_list_metric', 'ed')], "('hard_list_metric', 'ed')")


# def _plot_task_tag_histograms(al_data_dict):
#     # Determine number of subplots based on the number of keys in the data_dict
#     num_subplots = len(al_data_dict)
#
#     # Create subplots
#     fig, axes = plt.subplots(3, 1, figsize=(5 * num_subplots, 5 * num_subplots), sharey=True)
#     if num_subplots == 1:
#         axes = [axes]  # Ensure axes is always a list for consistent indexing
#
#     # Define colors and width for bars
#     bar_width = 0.15
#     colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
#     colors = cm.get_cmap('tab20', 15)
#     colors = [colors(i) for i in range(15)]
#
#     # Iterate through each subplot
#     for ax, (title, data_list) in zip(axes, al_data_dict.items()):
#         ax.set_title(title)
#         num_tags = len(data_list)
#         indices = np.arange(num_tags)
#         tags = list(data_list.keys())
#         generators = list(data_list[tags[0]].keys())
#         num_generators = len(generators)
#
#         # Plot bars for each generator in each tag
#         i = 1
#         for tag, bar_list in data_list.items():
#             j = 1
#             for generator_name, generator_value in bar_list.items():
#                 ax.bar(indices[i] + j * bar_width, generator_value, bar_width, color=colors[j % len(colors)],
#                        label=generator_name if i == 0 else "")
#                 j += 1
#             i += 1
#
#         # Set tag labels and remove x-tick labels
#         ax.set_xticks(indices + (num_generators - 1) * bar_width / 2)
#         ax.set_xticklabels([tag for tag, _ in data_list.items()])
#         ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)
#
#         ax.legend(title="Generator")
#
#     # Add legend to the figure
#     # fig.legend(loc='upper center', ncol=len(colors))
#
#     # Display the plot
#     plt.tight_layout()
#     plt.show()
#
#     a = 1


def _process_for_task_tag_plot(eval_result):
    data_dict = {
        "Difficulty": {},
        "Modality": {},
        "Scene": {}
    }
    data_count_dict = {
        "Difficulty": {},
        "Modality": {},
        "Scene": {}
    }
    for task_name, task_score_list in eval_result.items():
        task_tag = ALL_TASK_TAG_LIST[task_name]

        tmp_difficulty = task_tag.difficulty
        tmp_modality = task_tag.modality
        tmp_scene = task_tag.domain

        if tmp_difficulty not in data_dict['Difficulty']:
            data_dict['Difficulty'][tmp_difficulty] = {}
        if tmp_difficulty not in data_count_dict['Difficulty']:
            data_count_dict['Difficulty'][tmp_difficulty] = 0
        data_count_dict['Difficulty'][tmp_difficulty] += 1

        new_tmp_modality_list = []
        if tmp_modality[0] == "[":
            tmp_modality_list = tmp_modality.split(",")
            for tmp_modality_item in tmp_modality_list:
                tmp_modality_item = tmp_modality_item.split(":")[-1].split("'")[-2]
                new_tmp_modality_list.append(tmp_modality_item)
        else:
            new_tmp_modality_list = [tmp_modality]
        for tmp_modality_item in new_tmp_modality_list:
            if tmp_modality_item not in data_dict['Modality']:
                data_dict['Modality'][tmp_modality_item] = {}
            if tmp_modality_item not in data_count_dict['Modality']:
                data_count_dict['Modality'][tmp_modality_item] = 0
            data_count_dict['Modality'][tmp_modality_item] += 1

        new_tmp_scene_list = []
        if tmp_scene[0] == "[":
            tmp_scene_list = tmp_scene.split(",")
            for tmp_scene_item in tmp_scene_list:
                tmp_scene_item = tmp_scene_item.split(":")[-1].split("'")[-2]
                new_tmp_scene_list.append(tmp_scene_item)
        else:
            new_tmp_scene_list = [tmp_scene]
        for tmp_scene_item in new_tmp_scene_list:
            if tmp_scene_item not in data_dict['Scene']:
                data_dict['Scene'][tmp_scene_item] = {}
            if tmp_scene_item not in data_count_dict['Scene']:
                data_count_dict['Scene'][tmp_scene_item] = 0
            data_count_dict['Scene'][tmp_scene_item] += 1

        for generator_name, generator_result in task_score_list.items():
            if generator_name not in data_dict['Difficulty'][tmp_difficulty]:
                data_dict['Difficulty'][tmp_difficulty][generator_name] = 0.0
            data_dict['Difficulty'][tmp_difficulty][generator_name] += generator_result

            for tmp_modality_item in new_tmp_modality_list:
                if generator_name not in data_dict['Modality'][tmp_modality_item]:
                    data_dict['Modality'][tmp_modality_item][generator_name] = 0.0
                data_dict['Modality'][tmp_modality_item][generator_name] += generator_result

            for tmp_scene_item in new_tmp_scene_list:
                if generator_name not in data_dict['Scene'][tmp_scene_item]:
                    data_dict['Scene'][tmp_scene_item][generator_name] = 0.0
                data_dict['Scene'][tmp_scene_item][generator_name] += generator_result

    for difficulty, difficulty_data in data_dict['Difficulty'].items():
        for generator_name, generator_result in difficulty_data.items():
            data_dict['Difficulty'][difficulty][generator_name] = generator_result / data_count_dict['Difficulty'][
                difficulty]

    for modality, modality_data in data_dict['Modality'].items():
        for generator_name, generator_result in modality_data.items():
            data_dict['Modality'][modality][generator_name] = generator_result / data_count_dict['Modality'][modality]

    for scene, scene_data in data_dict['Scene'].items():
        for generator_name, generator_result in scene_data.items():
            data_dict['Scene'][scene][generator_name] = generator_result / data_count_dict['Scene'][scene]

    return data_dict


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
        fig, axs = plt.subplots(num_rows_per_figure, 1, figsize=(0.4 * num_tasks, 6 * num_rows_per_figure))
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
        "result-native_python_oneshot",
        'result-human_written',
        "result-langchain_zeroshot",
        "result-langchain_oneshot",
        "result-chainstream_cot",
        "result-chainstream_cot_1shot",
        "result-gpt-4o",
        "result-gpt-4o-new",
        "result-gpt-4",
        "result-gpt-4-new",
        "result-chainstream_fewshot_0shot",
        "result-chainstream_fewshot_1shot",
        "result-chainstream_fewshot_2shot",
        "result-chainstream_fewshot_3shot",
        "result-chainstream_fewshot_1shot_llm",
        "result-chainstream_fewshot_2shot_llm",
        "result-chainstream_fewshot_3shot_llm",
        "result-chainstream_feedback_example",
        "result-chainstream_feedback_0shot_0example_old",
        "result-chainstream_feedback_0shot_0example_new",
        "result-chainstream_feedback_0shot_1example_new",
        "result-chainstream_feedback_0shot_2example_new",
        "result-chainstream_feedback_0shot_3example_new",
        "result-chainstream_feedback_1shot_0example_old",
        "result-chainstream_feedback_0example_without_stdout",
        "result-chainstream_feedback_0example_without_output",
        "result-chainstream_feedback_0example_without_err"
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
    elif name == "result-native_python_oneshot":
        return "Py-1shot"
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
    elif name == "result-langchain_oneshot":
        return "LC-1shot"
    elif name == "result-gpt-4o":
        return "GPT-4o-old"
    elif name == "result-gpt-4o-new":
        return "GPT-4o-new"
    elif name == "result-gpt-4":
        return "GPT-4-0shot"
    elif name == "result-gpt-4-new":
        return "GPT-4-new"
    elif name == "result-chainstream_fewshot_0shot":
        return "CS-Fews-0shot"
    elif name == "result-chainstream_fewshot_1shot":
        return "CS-Fews-1shot"
    elif name == "result-chainstream_fewshot_2shot":
        return "CS-Fews-2shot"
    elif name == "result-chainstream_fewshot_3shot":
        return "CS-Fews-3shot"
    elif name == "result-chainstream_fewshot_1shot_llm":
        return "CS-Fews-1shot-LLM"
    elif name == "result-chainstream_fewshot_2shot_llm":
        return "CS-Fews-2shot-LLM"
    elif name == "result-chainstream_fewshot_3shot_llm":
        return "CS-Fews-3shot-LLM"
    elif name == "result-chainstream_feedback_example":
        return "CS-Feedback-example"
    elif name == "result-chainstream_feedback_0shot_0example_old":
        return "CS-Feedback-0Shot-0example-old"
    elif name == "result-chainstream_feedback_0shot_0example_new":
        return "CS-Feedback-0Shot-0example-new"
    elif name == "result-chainstream_feedback_0shot_1example_new":
        return "CS-Feedback-0Shot-1example-new"
    elif name == "result-chainstream_feedback_0shot_2example_new":
        return "CS-Feedback-0Shot-2example-new"
    elif name == "result-chainstream_feedback_0shot_3example_new":
        return "CS-Feedback-0Shot-3example-new"
    elif name == "result-chainstream_feedback_1shot_0example_old":
        return "CS-Feedback-1Shot-0example-old"
    elif name == "result-chainstream_feedback_0example_without_stdout":
        return "CS-Feedback-0Shot-0example-no-stdout"
    elif name == "result-chainstream_feedback_0example_without_err":
        return "CS-Feedback-0Shot-0example-no-err"
    elif name == "result-chainstream_feedback_0example_without_output":
        return "CS-Feedback-0Shot-0example-no-output"

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

            print(f"Eval: {title}, Generator {generator} has scores: {scores}")

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
        if generator == "chainstream_with_real_task_0_shot":
            return "CS-Feedback-0Shot"
        elif generator == "chainstream_real_task_framework_1shot":
            return "CS-Feedback-1shot"
        elif generator == "human_written_test_after_fixing":
            return "Human"
        elif generator == 'chainstream_zero_shot':
            return "CS-0shot"
        elif generator == 'native_python_zero_shot':
            return "Py-0shot"
        elif generator == 'native_python':
            return "Py"
        elif generator == 'chainstream_1shot':
            return "CS-1shot"
        elif generator == "chainstream_cot_zero_shot":
            return "CS-Cot"
        elif generator == "chainstream_cot_1shot":
            return "CS-Cot-1shot"
        elif generator == "langchain_zero_shot":
            return "LC-0shot"
        elif generator == "stream_native_python_zeroshot":
            return "Py-0shot"
        elif generator == "gpt-4o_native_gpt4o":
            return "GPT-4o-0shot"
        elif generator == "chainstream_fewshot_0shot":
            return "CS-Fews-0shot"
        elif generator == "chainstream_fewshot_1shot":
            return "CS-Fews-1shot"
        elif generator == "chainstream_fewshot_3shot":
            return "CS-Fews-3shot"
        elif generator == "human_written":
            return "Human"
        elif generator == "chainstream_human_written":
            return "Human"
        elif generator == "test":
            return "Test"
        elif generator == "chainstream_feedback_0example":
            return "CS-Feedback-0Example"
        elif generator == "chainstream_feedback_1example":
            return "CS-Feedback-1Example"
        elif generator == "chainstream_feedback_1shot_0example_old":
            return "CS-Feedback-1Shot-0Example-old"
        elif generator == "chainstream_feedback_0shot_0example_old":
            return "CS-Feedback-0Shot-0example_old"
        elif generator == "chainstream_feedback_0shot_0example_after_debug":
            return "CS-Feedback-0Shot-0example_new"
        elif generator == "chainstream_feedback_0shot_1example_after_debug":
            return "CS-Feedback-0Shot-1example"
        elif generator == "chainstream_feedback_0shot_3example_after_debug":
            return "CS-Feedback-0Shot-3example"
        elif generator == 'chainstream_feedback_0shot_0example_new':
            return "CS-Feedback-0Shot-0example_new"
        elif generator == 'chainstream_feedback_0shot_1example_new':
            return "CS-Feedback-0Shot-1example_new"
        elif generator == 'chainstream_feedback_0shot_2example_new':
            return "CS-Feedback-0Shot-2example_new"
        elif generator == 'chainstream_feedback_0shot_3example_new':
            return "CS-Feedback-0Shot-3example_new"
        elif generator == 'native_python_zeroshot':
            return "Py-0shot"
        elif generator == 'langchain_zeroshot':
            return "LC-0shot"
        elif generator == 'langchain_oneshot':
            return "LC-0shot"
        elif generator == 'chainstream-0-shot-0-example':
            return "CS_feedback_0shot_0example_old"
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
                f"Gen: {gen_name}, N: {N}, Success Rate: {gen_N_results['success_rate']} ({gen_N_results['success_count']} / {gen_N_results['total_task_count']})")

            for task, task_bool in gen_N_results['success_details'].items():
                if task not in generator_success_rate_for_tasks[gen_name]:
                    generator_success_rate_for_tasks[gen_name][task] = task_bool
                else:
                    generator_success_rate_for_tasks[gen_name][task] = generator_success_rate_for_tasks[gen_name][
                                                                           task] or task_bool

    _draw_avg_success_rate(generator_avg_success_rate)
    _draw_success_rate_for_tasks(generator_success_rate_for_tasks)


def test_task_tag_plot():
    # Example usage with the new data_dict structure
    data_dict = {
        "Subplot 1": {
            "Tag1": {"Gen1": 10, "Gen2": 15, "Gen3": 12},
            "Tag2": {"Gen1": 8, "Gen2": 12, "Gen3": 14}
        },
        "Subplot 2": {
            "Tag1": {"Gen1": 20, "Gen2": 18, "Gen3": 19},
            "Tag2": {"Gen1": 25, "Gen2": 22, "Gen3": 24}
        },
        "Subplot 3": {
            "Tag1": {"Gen1": 5, "Gen2": 7, "Gen3": 6},
            "Tag2": {"Gen1": 9, "Gen2": 11, "Gen3": 10}
        }
    }

    plot_task_tag_histograms(data_dict)


if __name__ == '__main__':
    base_file_path = r'/Users/liou/project/llm/ChainStream/ChainStreamSandBox/report_evaluator/result'
    eval_result = load_all_results(base_file_path)
    # draw_different_generator_score_for_specific_Metric(eval_result, 'code_similarity')

    draw_different_generator_score_for_specific_Metric(eval_result, 'output_similarity')
    draw_different_task_score_for_specific_Metric(eval_result, 'output_similarity')

    draw_success_rate(base_file_path)
