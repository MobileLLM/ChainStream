from AgentGenerator.generator.generator_base import FeedbackGuidedAgentGenerator
from AgentGenerator.io_model import StreamListDescription
from AgentGenerator.prompt import get_base_prompt
import ast


class ChainstreamFeedbackGuidedAgentGeneratorForDebugging(FeedbackGuidedAgentGenerator):
    def __init__(self, max_loop=10):
        super().__init__(max_loop=max_loop, sandbox_type="chainstream")
        self.answer = None

    def get_base_prompt(self, output_stream, input_stream) -> str:
        return get_base_prompt(output_stream, input_stream,
                               framework_name='chainstream',
                               example_number=0,
                               mission_name='stream',
                               command_name='feedback_guided_with_running',
                               need_feedback_example=False)

    def process_sandbox_feedback(self, sandbox_feedback, has_input=None):
        if sandbox_feedback['start_agent'] != "[OK]":
            tmp_prompt = f"After starting the code, the sandbox reported: {sandbox_feedback['start_agent']}"
        elif len(sandbox_feedback['error_message']['function_error']) > 0:
            tmp_prompt = f"The code can successfully start in the sandbox, means that the `Agent.__init__` and `Agent.start` are correct. However, when running the agent the sandbox reported register lisenter function error: {error['error_message']['function_error']}. Please check your code and try again."
        else:
            if has_input is None:
                tmp_prompt = f"Your code passed the sandbox test! Please debug your agent code throught the `INPUT` command to see if it can handle the input and output correctly."
            else:
                try:
                    tmp_inandout = {
                        "input_stream_items": sandbox_feedback['input_stream_item'],
                        "output_stream_items": sandbox_feedback['output_stream_output']
                    }
                    tmp_prompt = f"There's your input and output record, please check it: {tmp_inandout}"
                except Exception as e:
                    raise RuntimeError(
                        "Failed to get the input and output record. Please check the code and try again.")
        return tmp_prompt

    def step(self, action, last_code=None) -> (str, bool, str):
        done = False

        code_num = action.count("CODE<<")
        finish_num = action.count("FINISH<<")
        input_num = action.count("INPUT<<")

        if code_num + finish_num + input_num > 1:
            obs = "[FormatError] You can only provide one code, one input or one finish action at a time, please check your response format and try again."
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
                    entity = entity[len("```python"):-3].strip()
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
                stream_id = input.split(",")[0]
                if stream_id.startswith("`") and stream_id.endswith("`"):
                    stream_id = stream_id[1:-1]
                items = input.split(",", 1)[1]
                items = ast.literal_eval(items)
            except Exception as e:
                # obs = f"[FormatError] Invalid input format. The input should be in the format of `stream_id item1 item2...`, you can't provide more than one input stream at a time. Please check your response format and try again."
                obs = f"[INPUTError] get input error: {e}"
            else:
                if last_code is None:
                    obs = "[Error] Can not find your agent code"
                else:
                    obs = self.sandbox_exec(last_code, stream_id, items)

        elif action.startswith("THINK<<") and action.endswith(">>"):
            obs = "Nice thought."
        else:
            obs = "[FormatError] Invalid action format. The action should be in the format of CODE<<`agent_code`>>, INPUT<<`stream_id`, `[item1 item2...]`>>, or FINISH<<`your_answer`>>, you can't provide more than one code or finish action at a time, and also can's provide the Observation in the action format. Please check your response format and try again.".format(
                action)

        return obs, done, tmp_agent_code



if __name__ == '__main__':
    generator = ChainstreamFeedbackGuidedAgentGeneratorForDebugging()
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
