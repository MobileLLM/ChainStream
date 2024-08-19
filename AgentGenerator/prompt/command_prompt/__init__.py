from .cot_based import COT_BASED_PROMPT
from .few_shot_based import FEW_SHOT_BASED_PROMPT
from .feedback_guided_based import FEEDBACK_GUIDED_EXAMPLE, FEEDBACK_GUIDED_PROMPT_ONLY_START, \
    FEEDBACK_GUIDED_PROMPT_WITH_RUNNING


def get_command_prompt(command_type, need_example=None):
    if command_type == "cot":
        return COT_BASED_PROMPT
    elif command_type == "few_shot":
        return FEW_SHOT_BASED_PROMPT
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
    else:
        raise ValueError("Invalid command type")
