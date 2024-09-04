import matplotlib.pyplot as plt
import numpy as np
import json

from ChainStreamSandBox.tasks import get_task_with_data_batch


def _load_task_tag():
    all_task_class = get_task_with_data_batch()
    task_tag = {}
    for task_name, task_class in all_task_class.items():
        task_tag[task_name] = task_class().task_tag
    return task_tag


def plot_histograms(ax_data):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    colors = ['blue', 'red', 'green']

    for ax, (ax_name, ax_dict), color in zip(axs, ax_data.items(), colors):
        bar_names = list(ax_dict.keys())
        bar_values = list(ax_dict.values())

        colorn = plt.cm.viridis(np.linspace(0, 1, len(bar_values)))
        ax.bar(bar_names, bar_values)
        ax.tick_params(axis='y', labelsize=16)
        ax.set_title(ax_name, fontsize=16)
        # ax.set_xlabel('类别')
        ax.set_ylabel('Number', fontsize=16)

        ax.set_xticklabels(bar_names, rotation=45, ha='right', fontsize=16)

    plt.tight_layout()
    plt.show()


def test_plot_histograms():
    example_data = {
        "diff": {"easy": 10, "中": 15, "难": 5},
        "模态": {"视觉": 20, "听觉": 10, "触觉": 8},
        "场景": {"室内": 12, "室外": 18, "水下": 3}
    }

    # 调用绘图函数
    plot_histograms(example_data)


def draw_task_tag_figure():
    task_tag = _load_task_tag()
    print(task_tag)

    data_dict = {
        "Difficulty": {},
        "Data Type": {},
        "Task Type": {}
    }

    for task_name, task_tag_dict in task_tag.items():
        tmp_difficulty = task_tag_dict.difficulty
        tmp_modality = task_tag_dict.modality
        tmp_scene = task_tag_dict.domain

        if tmp_difficulty not in data_dict["Difficulty"]:
            data_dict["Difficulty"][tmp_difficulty] = 0
        data_dict["Difficulty"][tmp_difficulty] += 1

        new_tmp_modality_list = []
        if tmp_modality[0] == "[":
            tmp_modality_list = tmp_modality.split(",")
            for tmp_modality_item in tmp_modality_list:
                tmp_modality_item = tmp_modality_item.split(":")[-1].split("'")[-2]
                new_tmp_modality_list.append(tmp_modality_item)
        else:
            new_tmp_modality_list = [tmp_modality]
        for tmp_modality_item in new_tmp_modality_list:
            if tmp_modality_item not in data_dict["Data Type"]:
                data_dict["Data Type"][tmp_modality_item] = 0
            data_dict["Data Type"][tmp_modality_item] += 1

        new_tmp_scene_list = []
        if tmp_scene[0] == "[":
            tmp_scene_list = tmp_scene.split(",")
            for tmp_scene_item in tmp_scene_list:
                tmp_scene_item = tmp_scene_item.split(":")[-1].split("'")[-2]
                new_tmp_scene_list.append(tmp_scene_item)
        else:
            new_tmp_scene_list = [tmp_scene]
        for tmp_scene_item in new_tmp_scene_list:
            if tmp_scene_item not in data_dict["Task Type"]:
                data_dict["Task Type"][tmp_scene_item] = 0
            data_dict["Task Type"][tmp_scene_item] += 1

    sorted_difficulty = sorted(data_dict["Difficulty"].items(), key=lambda x: x[1], reverse=True)
    data_dict["Difficulty"] = {item[0]: item[1] for item in sorted_difficulty}
    sorted_modality = sorted(data_dict["Data Type"].items(), key=lambda x: x[1], reverse=True)
    data_dict["Data Type"] = {item[0]: item[1] for item in sorted_modality}
    sorted_scene = sorted(data_dict["Task Type"].items(), key=lambda x: x[1], reverse=True)
    data_dict["Task Type"] = {item[0]: item[1] for item in sorted_scene}
    # 调用绘图函数
    plot_histograms(data_dict)

    a = 1


if __name__ == '__main__':
    draw_task_tag_figure()
    # test_plot_histograms()
