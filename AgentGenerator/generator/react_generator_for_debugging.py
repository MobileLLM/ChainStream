from AgentGenerator.generator.generator_base import ReactAgentGenerator
from AgentGenerator.io_model import StreamListDescription
from AgentGenerator.utils import TextGPTModel
from AgentGenerator.prompt import REACT_PROMPT_WITH_RUNNING
from AgentGenerator.prompt import PromptSelector
from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import datetime


class FakeTaskConfig(SingleAgentTaskConfigBase):
    def __init__(self, runtime, input_description=None, output_description=None):
        super().__init__()
        self.input_stream = None
        self.output_stream = None
        self.input_description = input_description
        self.output_description = output_description
        self.input_items = None
        self.runtime = runtime

    def set_input_items(self, items):
        """
        items = {
            "stream_id": "stream_id",
            "items": []
        }
        :param items:
        :return:
        """
        self.input_items = items

    def init_environment(self, runtime):
        self.input_stream = self.runtime.create_stream(self, self.input_description['stream_id'])
        self.output_stream = self.runtime.create_stream(self, self.output_description['stream_id'])

        self.output_records = []

        def record_output(record):
            self.output_records.append(record)

        self.output_stream.for_each(record_output)

    def start_task(self, runtime):
        for item in self.input_items:
            try:
                tmp_input_stream = self.runtime.get_stream(item['stream_id'])
            except Exception as e:
                raise Exception(f"Can not find input stream {item['stream_id']}, error: {e}")
            for i in item['items']:
                tmp_input_stream.add_item(i)

        return self.input_items


class ReactGeneratorForDebugging(ReactAgentGenerator):
    """
        React with sandbox starting error ability
    """

    def __init__(self, max_loop=10):
        super().__init__()
        self.answer = None
        self.llm = TextGPTModel()

        self.max_loop = max_loop

    def generate_agent_impl(self, chainstream_doc, input_and_output_prompt, react_prompt=None) -> str:
        if react_prompt is None:
            react_prompt = REACT_PROMPT_WITH_RUNNING

        prompt = f"Doc: {chainstream_doc}\nMission: {input_and_output_prompt}\nInstructions: {react_prompt}\n"

        n_calls = 0
        n_badcalls = 0

        done = False

        # print(f"First Prompt: {prompt}")

        last_agent_code = None
        for i in range(1, self.max_loop):
            n_calls += 1
            thought_action = self._query_llm(prompt + f"Thought {i}:", stop=[f"\nObservation {i}:"])

            try:
                thought, action = thought_action.strip().split(f"\nAction {i}: ")
            except Exception as e:
                print('ohh...', thought_action)
                n_badcalls += 1
                n_calls += 1
                thought = thought_action.strip().split('\n')[0]
                action = self._query_llm(prompt + f"Thought {i}: {thought}\nAction {i}:", stop=[f"\n"]).strip()

            error_prompt, done, entity = self.step(action, last_code=last_agent_code)
            if entity is not None:
                last_agent_code = entity

            error = error_prompt.replace('\\n', '')
            step_str = f"Thought {i}: {thought}\nAction {i}: {action}\nObservation {i}: {error}\n"
            prompt += step_str
            # print(f"Step: {i}, prompt: {prompt}")

            if done:
                break
        if not done:
            error_prompt, done, entity = self.step("FINISH<<>>")
            if entity is not None:
                last_agent_code = entity

        return last_agent_code

    def _query_llm(self, prompt, stop=None):

        prompt = [
            {
                "role": "system",
                "content": prompt,
                "stop": stop
            }
        ]
        response = self.llm.query(prompt)

        print(
            f"####################################\nQuerying LLM at {datetime.datetime.now()} with prompt: {prompt[0]['content']}\nResponse: {response}\n##############\n")
        return response

    def step(self, action, last_code=None) -> (str, bool, str):
        done = False

        code_num = action.count("CODE<<")
        finish_num = action.count("FINISH<<")

        if code_num + finish_num > 1:
            obs = "[FormatError] You can only provide one code or one finish action at a time, please check your response format and try again."
            return obs, done, None

        tmp_agent_code = None
        action = action.strip()
        if action.startswith("CODE<<") and action.endswith(">>"):
            entity = action[len("CODE<<"):-2]
            if entity == "agent_code":
                obs = "[FormatError] Note that you must provide the agent code in the CODE<<`agent_code`>> format.We can't find your agent code, please check your response format and try again."
            else:
                entity = entity.strip()
                if entity.startswith("```python") and entity.endswith("```"):
                    entity = entity[len("```python"):-3]
                tmp_agent_code = entity
                obs = self.sandbox_exec(entity)
        elif action.startswith("FINISH<<") and action.endswith(">>"):
            answer = action[len("FINISH<<"):-2]
            self.answer = answer
            done = True
            obs = f"Episode finished. The answer is: {answer}"
        elif action.startswith("INPUT<<") and action.endswith(">>"):
            input = action.strip()[len("INPUT<<"):-2]
            try:
                stream_id = input.split()[0]
                if stream_id.startswith("`") and stream_id.endswith("`"):
                    stream_id = stream_id[1:-1]
                items = input.split()[1:]
            except Exception as e:
                obs = f"[FormatError] Invalid input format. The input should be in the format of `stream_id item1 item2...`, you can't provide more than one input stream at a time. Please check your response format and try again."
            else:
                if last_code is None:
                    obs = "[Error] Can not find your agent code"
                else:
                    obs = self.sandbox_exec(last_code, stream_id, items)

        elif action.startswith("THINK<<") and action.endswith(">>"):
            obs = "Nice thought."
        else:
            obs = "[FormatError] Invalid action format. The action should be in the format of CODE<<`agent_code`>>, THINK<<`your_thought`>>, or FINISH<<`your_answer`>>, you can't provide more than one code or finish action at a time, and also can's provide the Observation in the action format. Please check your response format and try again.".format(
                action)

        return obs, done, tmp_agent_code

    def sandbox_exec(self, agent_code, stream_id=None, items=None) -> str:
        if stream_id is None:
            sandbox = self.sandbox_class(None, agent_code, only_init_agent=True, save_result=False)

            try:
                for stream in self.input_description.streams:
                    sandbox.create_stream(stream)
                for stream in self.output_description.streams:
                    sandbox.create_stream(stream)
            except Exception as e:
                print(f"Error creating streams: {e}")
                raise e

            error = sandbox.start_test_agent()

        else:
            tmp_task = FakeTaskConfig(self.runtime, input_description=self.input_description, output_description=self.output_description)
            tmp_task.set_input_items([{
                "stream_id": stream_id,
                "items": items
            }])

            sandbox = self.sandbox_class(tmp_task, agent_code, save_result=False)

            error = sandbox.start_test_agent()

        # del sandbox
        # if error['start_agent']：
        if error['start_agent'] != "[OK]":
            tmp_prompt = f"After starting the code, the sandbox reported: {error['start_agent']}"
        elif len(error['error_message']['function_error']) > 0:
            tmp_prompt = f"The code can successfully start in the sandbox, means that the `Agent.__init__` and `Agent.start` are correct. However, when running the agent the sandbox reported register lisenter function error: {error['error_message']['function_error']}. Please check your code and try again."
        else:
            if stream_id is None:
                tmp_prompt = f"Your code passed the sandbox test! Please debug your agent code throught the `INPUT` command to see if it can handle the input and output correctly."
            else:
                tmp_inandout = {
                    "input_stream_items": error['input_stream_item'],
                    "output_stream_items": error['output_stream_output']
                }
                tmp_prompt = f"There's your input and output record, please check it: {tmp_inandout}"

        return tmp_prompt


if __name__ == '__main__':
    generator = ReactGeneratorForDebugging()
    agent_code = generator.generate_agent(
        StreamListDescription(streams=[{
            "stream_id": "summary_by_sender",
            "description": "A list of email summaries grouped by each email sender for pre 3 emails, excluding advertisement emails",
            "fields": {
                "sender": "name xxx, string",
                "summary": "sum xxx, string"
            }
        }]),
        input_description=StreamListDescription(streams=[{
            "stream_id": "all_email",
            "description": "All email messages",
            "fields": {
                "sender": "name xxx, string",
                "Content": "text xxx, string"
            }
        }])
    )

    print(agent_code)
