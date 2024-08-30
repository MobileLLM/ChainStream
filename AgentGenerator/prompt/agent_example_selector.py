import random
import os
import ast
import time

# FIXME: this is a temporary solution to import the task instances
from ChainStreamSandBox.tasks.tmp_task_instances import get_all_task_instances
from AgentGenerator.utils.llm_utils import TextGPTModel

CURRENT_CODE_PROMPT = """
The current code provided by the user is: 

{current_code}
"""

EXAMPLE_SELECTOR_WITH_FEEDBACK_BASE_PROMPT = """
Imagine you are a coding assistant tasked with selecting the most relevant example code from a set of provided examples based on the user's error messages or runtime results. You should consider factors such as the similarity between the example and the user's current task, the similarity in the use of APIs, and any other relevant factors.

You have the following examples available, formatted as a JSON list in the format `[{{"example_name": {{"target_stream": "example_code"}}}}]`:

```json
{example_list}
```

The user's current task is to implement a streaming output that meets the following specification: {target_stream}.
{current_code}
Error messages from the current code: {error_msg}  
Output from the current code: {current_output}  
Stdout from the current code: {current_stdout}

Based on the user's task and the given information, provide the most relevant example codes. The output should be in JSON format, specifically as a string of example names in the format `"example_name"`.

Output: 
"""

EXAMPLE_SELECTOR_ONLY_TASK_BASE_PROMPT = """
Imagine you are a coding assistant whose job is to select the most valuable example code from a provided set of examples based on the user's target program. You should consider factors like the similarity between the example and the user's current task, the similarity in the use of APIs, and any other relevant criteria.

You have the following examples available, formatted as a JSON list in the format `[{{"example_name": {{"target_stream": "example_code"}}}}]`:

```json
{example_list}
```

The user's current task is to implement a streaming output that meets the following specification: {target_stream}.

Based on the user's task, directly provide the most relevant example codes. The output should be in JSON format, specifically as a string of example names in the format `"example_name"`.

Output:
"""


class AgentExampleSelector:
    def __init__(self, task_now, max_example_num=3):
        self.task_instance_dict = get_all_task_instances()
        # all_tasks = get_task_with_data_batch()
        # all_tasks = {k: v() for k, v in all_tasks.items()}
        self.agent_example_list = {k: v.agent_example for k, v in self.task_instance_dict.items()}
        self.agent_name_2_target_stream = {k: str(v.output_stream_description) for k, v in self.task_instance_dict.items()}

        self.task_now = task_now

        self.output_stream_description = self.task_instance_dict[task_now].output_stream_description

        if self.task_now not in self.agent_example_list:
            raise ValueError("Task not found in agent example list")
        self.agent_example_list.pop(self.task_now)

        self.llm = TextGPTModel(model="gpt-4o")

        self.selected_example_count = 0
        self.max_example_count = max_example_num

    def _get_agent_example_list_prompt(self) -> str:
        example_list = """"""
        for example_name, example_code in self.agent_example_list.items():
            example_list += f'{{"{example_name}": {{"{self.agent_name_2_target_stream[example_name]}": "{example_code}"}}}}\n'
        example_list = example_list.strip()
        return example_list

    def get_random_agent_example(self):
        if self.selected_example_count >= self.max_example_count:
            raise ValueError("Max example count reached")

        agent_example_list = list(self.agent_example_list.keys())

        milliseconds = int(round(time.time() * 1000))
        random_generator = random.SystemRandom(milliseconds)
        selected_agent_example = random_generator.choice(agent_example_list)
        self.selected_example_count += 1
        example = self.agent_example_list[selected_agent_example]
        self.agent_example_list.pop(selected_agent_example)
        return example

    def get_llm_agent_example(self, feedback: tuple = None, current_code: str = None):
        if self.selected_example_count >= self.max_example_count:
            raise ValueError("Max example count reached")

        if feedback is None:
            prompt = EXAMPLE_SELECTOR_ONLY_TASK_BASE_PROMPT.format(
                example_list=self._get_agent_example_list_prompt(),
                target_stream=self.output_stream_description,
            )
        else:
            err, stdout, output = feedback
            if current_code is None:
                current_code_prompt = ""
            else:
                current_code_prompt = CURRENT_CODE_PROMPT.format(current_code=current_code)
            prompt = EXAMPLE_SELECTOR_WITH_FEEDBACK_BASE_PROMPT.format(
                example_list=self._get_agent_example_list_prompt(),
                target_stream=self.output_stream_description,
                error_msg=err,
                current_code=current_code_prompt,
                current_output=output,
                current_stdout=stdout,
            )
        prompt = prompt.strip()

        prompt = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = self.llm.query(prompt).strip()

        if response.startswith("```json") and response.startswith("```"):
            response = response[7:-3].strip()

        try:
            example_name = ast.literal_eval(response)
            if isinstance(example_name, str):
                example_name = example_name.strip().strip(',')[0]
            if isinstance(example_name, list):
                example_name = example_name[0]
                if isinstance(example_name, list):
                    example_name = example_name[0]
            if example_name not in self.agent_example_list:
                raise ValueError("Invalid example name")
            example = self.agent_example_list[example_name]
            self.agent_example_list.pop(example_name)
            self.selected_example_count += 1
            return example, example_name

        except Exception as e:
            print(f"[AgentExampleSelectorError]: {e}, response: {response}")
            return None, "[AgentExampleSelectorError]: {e}, response: {response}"


if __name__ == "__main__":
    task_now = "EmailTask2"
    task_instance_dict = get_all_task_instances()
    task_instance_dict = {k: v() for k, v in task_instance_dict.items()}
    agent_example_selector = AgentExampleSelector(task_instance_dict, task_now)
    example = agent_example_selector.get_llm_agent_example(("Error message", "Current output", "Current stdout"))
    print(example)
