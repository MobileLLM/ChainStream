from AgentGenerator.generator.generator_base import FeedbackGuidedAgentGeneratorWithoutTask
from AgentGenerator.io_model import StreamListDescription
from AgentGenerator.prompt import get_base_prompt


class ChainstreamFeedbackGuidedGeneratorForStarting(FeedbackGuidedAgentGeneratorWithoutTask):
    """
        React with sandbox starting error ability
    """

    def __init__(self, max_loop=10, sandbox_type='chainstream'):
        super().__init__(max_loop=max_loop, sandbox_type=sandbox_type)
        self.answer = None

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(output_stream, input_stream,
                               framework_name='chainstream',
                               example_number=0,
                               mission_name="stream",
                               command_name="feedback_guided_only_start",
                               need_feedback_example=False
                               )

    def process_sandbox_feedback(self, sandbox_feedback, has_input=None):
        return f"After executing the code, the sandbox reported: {sandbox_feedback['start_agent']}"

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
        elif action.startswith("THINK<<") and action.endswith(">>"):
            obs = "Nice thought."
        else:
            obs = "[FormatError] Invalid action format. The action should be in the format of CODE<<`agent_code`>>, THINK<<`your_thought`>>, or FINISH<<`your_answer`>>, you can't provide more than one code or finish action at a time, and also can's provide the Observation in the action format. Please check your response format and try again.".format(
                action)

        return obs, done, tmp_agent_code


if __name__ == '__main__':
    generator = ChainstreamFeedbackGuidedGeneratorForStarting()
    agent_code, latency, tokens = generator.generate_agent(
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
    print(latency)
    print(tokens)
