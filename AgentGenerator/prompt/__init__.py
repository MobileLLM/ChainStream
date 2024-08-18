from .prompt_selector import PromptSelector
from .mission_prompt import get_mission_prompt
from .command_prompt import get_command_prompt
from .framework_doc import get_framework_doc

from typing import Literal

framework_type = Literal['chainstream', 'langchain', "native_python", "native_gpt"]
mission_type = Literal['batch', 'gpt', 'stream']
command_type = Literal['cot', 'few_shot', 'feedback_guided_only_start', 'feedback_guided_with_running']


def get_base_prompt(output_stream,
                    input_stream,
                    framework_name: framework_type = None,
                    example_number=None,
                    mission_name: mission_type = None,
                    command_name: command_type = None,
                    need_feedback_example=None):

    tmp_framework_prompt = get_framework_doc(framework_name, example_number)
    tmp_mission_prompt = get_mission_prompt(output_stream, input_stream, mission_name, framework_name)
    tmp_command_prompt = get_command_prompt(command_name, need_feedback_example)

    return tmp_framework_prompt + tmp_mission_prompt + tmp_command_prompt
