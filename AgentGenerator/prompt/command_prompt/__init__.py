if __name__ == '__main__':
    from cot_based import COT_BASED_PROMPT
    from few_shot_based import FEW_SHOT_BASED_PROMPT
    from feedback_guided_based import FEEDBACK_GUIDED_EXAMPLE, FEEDBACK_GUIDED_PROMPT_ONLY_START, \
        FEEDBACK_GUIDED_PROMPT_WITH_RUNNING, FEEDBACK_GUIDED_PROMPT_REAL_TASK, FEEDBACK_GUIDED_FOR_REAL_TASK_EXAMPLE
else:
    from .cot_based import COT_BASED_PROMPT
    from .few_shot_based import FEW_SHOT_BASED_PROMPT
    from .feedback_guided_based import FEEDBACK_GUIDED_EXAMPLE, FEEDBACK_GUIDED_PROMPT_ONLY_START, \
        FEEDBACK_GUIDED_PROMPT_WITH_RUNNING, FEEDBACK_GUIDED_PROMPT_REAL_TASK, FEEDBACK_GUIDED_FOR_REAL_TASK_EXAMPLE
    from .gpt_based import GPT_BASE_PROMPT


def get_command_prompt(command_type, need_example=None):
    if command_type == "cot":
        return COT_BASED_PROMPT
    elif command_type == "few_shot":
        return FEW_SHOT_BASED_PROMPT
    elif command_type == "native_gpt":
        return GPT_BASE_PROMPT
    elif command_type == "feedback_guided_only_start":
        if need_example:
            return FEEDBACK_GUIDED_PROMPT_ONLY_START + FEEDBACK_GUIDED_EXAMPLE
        else:
            return FEEDBACK_GUIDED_PROMPT_ONLY_START
    elif command_type == "feedback_guided_with_running":
        if need_example:
            return FEEDBACK_GUIDED_PROMPT_WITH_RUNNING + FEEDBACK_GUIDED_EXAMPLE
        else:
            return FEEDBACK_GUIDED_PROMPT_WITH_RUNNING
    elif command_type == "feedback_guided_with_real_task":
        if need_example:
            return FEEDBACK_GUIDED_PROMPT_REAL_TASK + FEEDBACK_GUIDED_FOR_REAL_TASK_EXAMPLE
        else:
            return FEEDBACK_GUIDED_PROMPT_REAL_TASK
    else:
        raise ValueError("Invalid command type")


if __name__ == '__main__':
    print(get_command_prompt("cot"), end="\n*************\n")
    print(get_command_prompt("few_shot"), end="\n*************\n")
    print(get_command_prompt("feedback_guided_only_start", False), end="\n*************\n")
    print(get_command_prompt("feedback_guided_with_running", False), end="\n*************\n")