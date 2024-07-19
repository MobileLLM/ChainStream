from AgentGenerator.generator.generator_base import ReactAgentGenerator
from AgentGenerator.io_model import StreamListDescription
from AgentGenerator.utils import TextGPTModel
from AgentGenerator.prompt import REACT_PROMPT
from AgentGenerator.prompt import PromptSelector


class ReactPlusGenerator(ReactAgentGenerator):
    def __init__(self, max_loop=10):
        super().__init__()
        self.answer = None
        self.llm = TextGPTModel()

        self.max_loop = max_loop

    def generate_agent_impl(self, chainstream_chinese_doc, input_and_output_prompt, react_prompt=None) -> str:
        if react_prompt is None:
            react_prompt = REACT_PROMPT

        prompt = f"Doc: {chainstream_chinese_doc}\nMission: {input_and_output_prompt}\nInstructions: {react_prompt}\n"

        n_calls = 0
        n_badcalls = 0

        done = False

        # print(f"First Prompt: {prompt}")

        for i in range(self.max_loop):
            n_calls += 1
            thought_action = self._query_llm(prompt + f"Thought {i}:", stop=[f"\nSandboxObservation {i}:"])

            try:
                thought, action = thought_action.strip().split(f"\nAction {i}: ")
            except:
                print('ohh...', thought_action)
                n_badcalls += 1
                n_calls += 1
                thought = thought_action.strip().split('\n')[0]
                action = self._query_llm(prompt + f"Thought {i}: {thought}\nAction {i}:", stop=[f"\n"]).strip()

            error_prompt, done = self.step(action)

            error = error_prompt.replace('\\n', '')
            step_str = f"Thought {i}: {thought}\nAction {i}: {action}\nSandboxObservation {i}: {error}\n"
            prompt += step_str
            print(f"Step: {i}, prompt: {prompt}")

            if done:
                break
        if not done:
            error_prompt, done = self.step("finish[]")

    def _query_llm(self, prompt, stop=None):
        prompt = [
            {
                "role": "system",
                "content": prompt,
                "stop": stop
            }
        ]
        response = self.llm.query(prompt)
        return response

    def step(self, action) -> (str, bool):
        done = False

        action = action.strip()
        if action.startswith("CODE<<") and action.endswith(">>"):
            entity = action[len("CODE<<"):-2]
            obs = self.sandbox_exec(entity)
        elif action.startswith("FINISH<<") and action.endswith(">>"):
            answer = action[len("FINISH<<"):-2]
            self.answer = answer
            done = True
            obs = f"Episode finished. The answer is: {answer}"
        elif action.startswith("THINK<<") and action.endswith(">>"):
            obs = "Nice thought."
        else:
            obs = "Invalid action: {}".format(action)

        return obs, done

    def sandbox_exec(self, agent_code) -> str:
        return "[SandboxObservation {test}]"


if __name__ == '__main__':
    generator = ReactPlusGenerator()
    agent_code = generator.generate_agent(
        StreamListDescription(streams=[{
                "stream_id": "summary_by_sender",
                "description": "A list of email summaries grouped by each email sender, excluding ads",
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

