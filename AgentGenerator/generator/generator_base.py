from ChainStreamSandBox import get_sandbox_class
from AgentGenerator.io_model import StreamListDescription
from AgentGenerator.stream_selector import StreamSelectorBase
from AgentGenerator.utils.llm_utils import TextGPTModel
from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
from chainstream.stream import create_stream, get_stream
import datetime


class AgentGeneratorBase:
    """
    Three mode of generator:
    1. work as a part of a running Runtime, serve for a real system, select input stream and agents and other information from the Runtime.
    2. work alone with stream and agent information, usually for sandbox testing or other purposes, need to provide input stream and other information manually.
    3. [Default] work alone without any information, need to provide input stream and agent information in the generate_dsl function manually.
    """

    def __init__(self, runtime=None, model_name="gpt-4o"):
        self.runtime = runtime
        self.stream_selector = StreamSelectorBase()

        self.output_description = None
        self.input_description = None

        self.model_name = model_name
        self.llm = TextGPTModel(model_name)

    def generate_agent(self, output_description, input_description=None, use_selector=False) -> (str, int):
        self.output_description = output_description
        self.input_description = input_description

        self.stream_selector.set_all_stream_list(input_description)

        # Do not specify input_description, let llm make up the input stream
        if input_description is None:
            output_stream, input_stream = self.stream_selector.select_stream(output_description, select_policy='none')
            # return self.generate_agent_impl(None, output_description)
        else:
            if not use_selector:
                # Specify input_description, use all input streams
                output_stream, input_stream = self.stream_selector.select_stream(output_description,
                                                                                 select_policy='all')
                # return self.generate_agent_impl(input_description, output_description)
            else:
                # Specify input_description, use llm to select input streams
                output_stream, input_stream = self.stream_selector.select_stream(output_description,
                                                                                 select_policy='llm')

        # basic_prompt = f"{chainstream_chinese_doc}\n{input_and_output_prompt}"

        start_time = datetime.datetime.now()
        code = self.generate_agent_impl(output_stream, input_stream)
        end_time = datetime.datetime.now()

        return code, (end_time - start_time).total_seconds(), self.get_llm_token_count()

    # def generate_agent_impl(self, input_description: [StreamListDescription, None], output_description:
    # StreamListDescription) -> str: raise NotImplementedError("Agent generator must implement generate_agent_impl
    # function.")

    def generate_agent_impl(self, output_stream, input_stream) -> str:
        raise NotImplementedError("Agent generator must implement generate_agent_impl function.")

    def get_base_prompt(self, output_stream, input_stream) -> str:
        raise NotImplementedError("Agent generator must implement get_base_prompt function.")

    def generate_agent_for_runtime(self, output_description: StreamListDescription):
        if self.runtime is None or self.stream_selector is None:
            raise ValueError("Runtime and stream selector must be provided for agent generation in runtime mode.")

        # TODO: this API is still under development
        stream_list = self.runtime.get_stream_description_list()

        agent, _, _ = self.generate_agent(output_description, input_description=stream_list, use_selector=True)

        return agent

    def get_llm_token_count(self):
        if hasattr(self, "llm"):
            return self.llm.get_token_count()
        return None


class DirectAgentGenerator(AgentGeneratorBase):
    def __init__(self):
        super().__init__()

    def generate_agent_impl(self, output_stream, input_stream) -> str:
        prompt = self.get_base_prompt(output_stream, input_stream)

        print(f"Prompt: {prompt}")

        prompt = [
            {
                "role": "system",
                "content": prompt
            }
        ]

        response = self.llm.query(prompt)
        return response.replace("'''", " ").replace("```", " ").replace("python", "")

    def get_base_prompt(self, output_stream, input_stream) -> str:
        raise NotImplementedError("Agent generator must implement get_base_prompt function.")


class FakeTaskConfig(SingleAgentTaskConfigBase):
    def __init__(self, input_description=None, output_description=None):
        super().__init__()
        from chainstream.runtime import cs_server_core
        self.input_stream = {}
        self.output_stream = {}
        self.input_description = input_description
        self.output_description = output_description
        self.input_items = None
        self.runtime = cs_server_core

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
        for stream in self.input_description.streams:
            self.input_stream[stream.stream_id] = create_stream(self, stream.stream_id)
        for stream in self.output_description.streams:
            self.output_stream[stream.stream_id] = create_stream(self, stream.stream_id)

        # self.input_stream = create_stream(self, self.input_description.stream_id)
        # self.output_stream = create_stream(self, self.output_description.stream_id)

        self.output_record = {x.stream_id: [] for x in self.output_description.streams}

        def get_record_func(stream_id):
            tmp_record = self.output_record[stream_id]

            def record_output(record):
                tmp_record.append(record)

            return record_output

        for stream in self.output_stream.values():
            stream.for_each(get_record_func(stream.stream_id))

    def start_task(self, runtime):
        all_input_items = {}
        for item in self.input_items:
            try:
                tmp_input_stream = get_stream(self, item['stream_id'])
                if item['stream_id'] not in all_input_items:
                    all_input_items[item['stream_id']] = []
            except Exception as e:
                raise Exception(f"Can not find input stream {item['stream_id']}, error: {e}")
            for i in item['items']:
                tmp_input_stream.add_item(i)
                all_input_items[item['stream_id']].append(i)

        return all_input_items


class FeedbackGuidedAgentGenerator(AgentGeneratorBase):
    def __init__(self, runtime=None, max_loop=20, sandbox_type="chainstream"):
        super().__init__(runtime)
        self.sandbox_type = sandbox_type
        self.sandbox_class = get_sandbox_class(sandbox_type)

        self.max_loop = max_loop

        self.history = None

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
        raise NotImplementedError("Agent generator must implement step() function.")

    def generate_agent_impl(self, output_stream, input_stream) -> str:
        all_prompt = self.get_base_prompt(output_stream, input_stream)

        n_calls = 0
        n_badcalls = 0
        done = False

        last_agent_code = None

        for i in range(self.max_loop):
            n_calls += 1
            thought_action = self._query_llm(all_prompt + f"Thought {i}:", stop=[f"\nObservation {i}:"])

            try:
                if thought_action.strip().endswith("Observation:"):
                    thought_action = thought_action.strip()[:-len("Observation:")]
                thought, action = thought_action.strip().split(f"\nAction {i}: ")

            except Exception as e:
                print('ohh...', thought_action)
                n_badcalls += 1
                n_calls += 1
                thought = thought_action.strip().split('\n')[0]
                action = self._query_llm(all_prompt + f"Thought {i}: {thought}\nAction {i}:", stop=[f"\n"]).strip()

            error_prompt, done, entity = self.step(action, last_code=last_agent_code)
            if entity is not None:
                last_agent_code = entity

            error = error_prompt.replace('\\n', '')
            step_str = f"Thought {i}: {thought}\nAction {i}: {action}\nObservation {i}: {error}\n"
            all_prompt += step_str

            self.history = all_prompt

            # print(f"Step: {i}, prompt: {prompt}")

            if done:
                break
        if not done:
            error_prompt, done, entity = self.step("FINISH<<Maximum loop limit reached>>")
            if entity is not None:
                last_agent_code = entity

        return last_agent_code

    def sandbox_exec(self, agent_code, stream_items=None):
        if stream_items is None:
            sandbox = self.sandbox_class(None, agent_code, only_init_agent=True, save_result=False)

            try:
                if self.sandbox_type == "chainstream":
                    for stream in self.input_description.streams:
                        sandbox.create_stream(stream)
                    for stream in self.output_description.streams:
                        sandbox.create_stream(stream)
            except Exception as e:
                print(f"Error creating streams: {e}")
                raise e

            sandbox_feedback = sandbox.start_test_agent()

        else:
            tmp_task = FakeTaskConfig(input_description=self.input_description,
                                      output_description=self.output_description)
            # tmp_task.set_input_items([{
            #     "stream_id": stream_id,
            #     "items": items
            # }])

            tmp_task.set_input_items(stream_items)

            sandbox = self.sandbox_class(tmp_task, agent_code, save_result=False)

            sandbox_feedback = sandbox.start_test_agent()

        feedback_prompt = self.process_sandbox_feedback(sandbox_feedback, has_input=True if stream_items is not None else False)

        return feedback_prompt

    def get_base_prompt(self, output_stream, input_stream) -> str:
        raise NotImplementedError("Agent generator must implement get_base_prompt function.")

    def process_sandbox_feedback(self, sandbox_feedback, has_input=None):
        raise NotImplementedError("Agent generator must implement process_sandbox_feedback() function.")
