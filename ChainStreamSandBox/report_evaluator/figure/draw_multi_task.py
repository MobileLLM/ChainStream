import matplotlib.pyplot as plt
import numpy as np


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
    elif name == "gpt-4-new":
        return "GPT-4-new"
    elif name == "langchain_oneshot":
        return "LangChain (1-shot)"
    elif name == "langchain_zeroshot":
        return "LangChain (0-shot)"
    elif name == "native_python_zeroshot":
        return "Python (0-shot)"
    elif name == "native_python_oneshot":
        return "Python (1-shot)"
    elif name == "chainstream_feedback_0example_without_stdout":
        return "Ours (0-example, no stdout)"
    elif name == "chainstream_feedback_0example_without_output":
        return "Ours (0-example, no output)"
    elif name == "chainstream_feedback_0example_without_err":
        return "Ours (0-example, no err)"
    else:
        raise ValueError(f"Invalid name {name}")


def draw_multi_task():
    data = {
        'Multi-step': {
            'result-native_python_zeroshot': 0.28344002669028623,
            'result-native_python_oneshot': 0.4871506402465984,
            'result-langchain_zeroshot': 0.3794637966038796,
            'result-langchain_oneshot': 0.5175526171808759,
            'result-gpt-4o': 0.48820028095433193,
            'result-gpt-4': 0.497282605852734,
            'result-chainstream_fewshot_0shot': 0.3974406476122624,
            'result-chainstream_fewshot_1shot': 0.5711072904488976,
            'result-chainstream_fewshot_3shot': 0.6559591675088805,
            'result-chainstream_feedback_0shot_0example_old': 0.6011951112202499,
            'result-chainstream_feedback_0shot_1example_new': 0.6497322684100684,
            'result-chainstream_feedback_0shot_2example_new': 0.6858021028517473,
            'result-chainstream_feedback_0shot_3example_new': 0.6883455436238475,
        },
        'Single-step': {
            'result-native_python_zeroshot': 0.549767428190233,
            'result-native_python_oneshot': 0.507128281214598,
            'result-langchain_zeroshot': 0.37551691750588806,
            'result-langchain_oneshot': 0.5306993396445602,
            'result-gpt-4o': 0.5483717244508668,
            'result-gpt-4': 0.4300488307293081,
            'result-chainstream_fewshot_0shot': 0.5981038332718117,
            'result-chainstream_fewshot_1shot': 0.6476366397578858,
            'result-chainstream_fewshot_3shot': 0.6707811379374662,
            'result-chainstream_feedback_0shot_0example_old': 0.6579165596628807,
            'result-chainstream_feedback_0shot_1example_new': 0.7239588107245074,
            'result-chainstream_feedback_0shot_2example_new': 0.7450820397666319,
            'result-chainstream_feedback_0shot_3example_new': 0.7347956629217223,
        }
    }


    multi_step_labels = list(data['Multi-step'].keys())
    multi_step_labels = [_rename(name.split("result-")[-1]) for name in multi_step_labels]
    multi_step_values = list(data['Multi-step'].values())
    single_step_labels = list(data['Single-step'].keys())
    single_step_labels = [_rename(name.split("result-")[-1]) for name in single_step_labels]
    single_step_values = list(data['Single-step'].values())

    # Set positions for the bars
    multi_step_x = np.arange(len(multi_step_labels))
    single_step_x = np.arange(len(single_step_labels)) + len(multi_step_labels) + 1  # Add space between groups

    # Create a color map for the bars
    # unique_keys = set([name.split("_")[0] for name in ["Ours", "Ours without iteration", "Python", "LangChain", "GPT"]])
    unique_keys = set([name.split("_")[0] for name in multi_step_labels + single_step_labels])
    color_map = {key: plt.cm.tab20(i / len(unique_keys)) for i, key in enumerate(unique_keys)}

    # Get colors for each bar based on the mapping
    multi_step_colors = [color_map[name.split("_")[0]] for name in multi_step_labels]
    single_step_colors = [color_map[name.split("_")[0]] for name in single_step_labels]

    fig, ax = plt.subplots(figsize=(14, 8))

    # Draw bars with assigned colors
    ax.bar(multi_step_x, multi_step_values, width=0.7, label='Multi-step', color=multi_step_colors)
    # ax.bar(multi_step_x, multi_step_values, width=0.7, label='Multi-step', color=multi_step_colors, hatch='//')
    # ax.bar(multi_step_x, multi_step_values, width=0.7, label='Multi-step', color=multi_step_colors, hatch='//')
    # ax.bar(multi_step_x, multi_step_values, width=0.7, label='Multi-step', color=multi_step_colors, hatch='//')
    ax.bar(single_step_x, single_step_values, width=0.7, label='Single-step', color=single_step_colors, hatch='//')

    # Add labels, title and ticks
    ax.set_ylabel('Scores')
    ax.set_title('Scores by task type and method')
    ax.set_xticks(np.concatenate((multi_step_x, single_step_x)))
    ax.set_xticklabels(multi_step_labels + single_step_labels, rotation=45, ha='right')
    ax.legend()

    fig.tight_layout()
    plt.show()


draw_multi_task()
