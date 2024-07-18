from .generator_base import ReactAgentGenerator
from ..io_model import StreamListDescription
from ..utils import TextGPTModel
from ..prompt import REACT_PROMPT
from ..prompt import PromptSelector


class ReactPlusGenerator(ReactAgentGenerator):
    def __init__(self, max_loop=10):
        super().__init__()
        self.llm = TextGPTModel()

        self.max_loop = max_loop

    def generate_agent_impl(self, base_prompt, react_prompt=None) -> str:
        if react_prompt is None:
            react_prompt = REACT_PROMPT

        prompt = f"{base_prompt}\n{react_prompt}"

        n_calls = 0
        n_badcalls = 0
        for i in range(self.max_loop):
            n_calls += 1
            thought_action = self.llm.query(prompt + f"Thought {i}:", stop=[f"\nSandbox Error {i}:"])

            try:
                thought, action = thought_action.strip().split(f"\nAction {i}: ")
            except:
                print('ohh...', thought_action)
                n_badcalls += 1
                n_calls += 1
                thought = thought_action.strip().split('\n')[0]
                action = self.llm.query(prompt + f"Thought {i}: {thought}\nAction {i}:", stop=[f"\n"]).strip()

            error_prompt, done = self.step(action[0].lower() + action[1:])

            error = error_prompt.replace('\\n', '')
            step_str = f"Thought {i}: {thought}\nAction {i}: {action}\nSandbox Error {i}:: {error}\n"
            prompt += step_str

            if done:
                break
        if not done:
            error_prompt, done = self.step("finish[]")

    def step(self, action) -> (str, bool):
        action = action.strip()
        if action.startswith("code[") and action.endswith("]"):
            entity = action[len("search["):-1]
            self.sandbox_exec(entity)
        elif action.startswith("finish[") and action.endswith("]"):
            answer = action[len("finish["):-1]
            self.answer = answer
            done = True
            self.obs = f"Episode finished, reward = {reward}\n"
        elif action.startswith("think[") and action.endswith("]"):
            self.obs = "Nice thought."
        else:
            self.obs = "Invalid action: {}".format(action)

        pass

    def sandbox_exec(self, agent_code):
        pass


if __name__ == '__main__':
    generator = ReactPlusGenerator()
    agent_code = generator.generate_agent(
        StreamListDescription(streams=[{
                "stream_id": "summary_by_sender",
                "description": "A list of email summaries for each email sender, excluding ads",
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

