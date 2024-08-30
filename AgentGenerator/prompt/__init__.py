from AgentGenerator.prompt.mission_prompt import get_mission_prompt
from .command_prompt import get_command_prompt
from AgentGenerator.prompt.framework_doc import get_framework_doc
from AgentGenerator.prompt.feedback_processor import FilterErrorFeedbackProcessor, FilterErrorWithExampleFeedbackProcessor

from typing import Literal

framework_type = Literal['chainstream', 'batch_langchain', "batch_native_python", "stream_langchain", "stream_native_python", "native_gpt"]
mission_type = Literal['batch', 'native_gpt', 'stream']
command_type = Literal['native_gpt', 'cot', 'few_shot', 'feedback_guided_only_start', 'feedback_guided_with_running', 'feedback_guided_with_real_task']


def get_base_prompt(output_stream,
                    input_stream,
                    framework_name: framework_type = None,
                    example_number=None,
                    mission_name: mission_type = None,
                    command_name: command_type = None,
                    need_feedback_example=None, task_now=None):
    tmp_framework_prompt = get_framework_doc(framework_name, example_number, task_now=task_now)
    tmp_mission_prompt = get_mission_prompt(output_stream, input_stream, mission_name, framework_name)
    tmp_command_prompt = get_command_prompt(command_name, need_feedback_example)

    return tmp_framework_prompt + tmp_mission_prompt + tmp_command_prompt


if __name__ == '__main__':
    print("chainstream, stream, few_shot",
          get_base_prompt('output_stream', 'input_stream', 'chainstream', 0, 'stream', 'few_shot'))
    print("chainstream, stream, feedback_guided_only_start",
          get_base_prompt('output_stream', 'input_stream', 'chainstream', 0, 'stream', "feedback_guided_only_start"))
    print("chainstream, stream, feedback_guided_with_running",
          get_base_prompt('output_stream', 'input_stream', 'chainstream', 0, 'stream', "feedback_guided_with_running"))

    print("langchain, batch, batch",
          get_base_prompt('output_stream', 'input_stream', 'langchain', 0, 'batch', 'few_shot'))
    print("langchain, batch, feedback_guided_only_start",
          get_base_prompt('output_stream', 'input_stream', 'langchain', 0, 'batch', "feedback_guided_only_start"))
    print("langchain, batch, feedback_guided_with_running",
          get_base_prompt('output_stream', 'input_stream', 'langchain', 0, 'batch', "feedback_guided_with_running"))

    print("native_python, batch, few_shot",
          get_base_prompt('output_stream', 'input_stream', 'native_python', 0, 'batch', 'few_shot'))
    print("native_python, batch, feedback_guided_only_start",
          get_base_prompt('output_stream', 'input_stream', 'native_python', 0, 'batch', "feedback_guided_only_start"))
    print("native_python, batch, feedback_guided_with_running",
          get_base_prompt('output_stream', 'input_stream', 'native_python', 0, 'batch', "feedback_guided_with_running"))

    print("native_gpt, gpt, cot", get_base_prompt('output_stream', 'input_stream', 'native_gpt', 0, 'gpt', 'few_shot'))
