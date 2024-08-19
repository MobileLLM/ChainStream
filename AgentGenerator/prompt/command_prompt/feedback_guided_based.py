
FEEDBACK_GUIDED_PROMPT_ONLY_START = """Solve a chainstream agent generation task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be two types: 
(1) CODE<<`agent_code`>>, you need to write the agent code in the middel of `<<>>`，and this action will executes the `agent_code` in the sandbox environment and returns the error message and reference document if any.
(2) FINISH<<`finish_message`>>, you need to write the `finish_message` in the middle of `<<>>`, and this action means the mission is finished.

Note that you can only submit one agent code or finish with message per step, and the runtime will return the format error message or the sandbox error message in Observation step, you can't write any code or message in Observation step, even don't write `Observation:` in the end of the response.
"""

FEEDBACK_GUIDED_PROMPT_WITH_RUNNING = """Solve a chainstream agent generation task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be two types: 
(1) CODE<<`agent_code`>>, you need to write the agent code in the middel of `<<>>`，and this action will executes the `agent_code` in the sandbox environment and returns the error message and reference document if any.
(2) INPUT<<`items`>>, You can use this command to verify the correctness of the `agent_code`. You need to specify the `items` in the middle of `<<>>`, each item should be a dict like `{"stream_id": "xxx", "item": {"field1": "value1", "field2": "value2"}`, and this action will send the `items` to the input stream with the `stream_id`, note that the `items` should be a list of item that can be directly passed to `add_item()`. Subsequently, the sandbox will return the output of this code's output stream in the `Observation`, as well as the error message. By analyzing the input and output, you can determine the correctness of the code and decide whether to modify the code using the `CODE` command or submit the code using the `FINISH` command.
(3) FINISH<<`finish_message`>>, you need to write the `finish_message` in the middle of `<<>>`, and this action means the mission is finished.

Note that you can only submit one agent code or finish with message per step, and the runtime will return the format error message or the sandbox error message in Observation step. So system prompt will end with `Thought {i}:` your response should end with `Observation {i}:`.
"""

FEEDBACK_GUIDED_EXAMPLE = """
Here is an examples:

Mission: Your mission is to programme an agent with chainstream framework to get the following output streams:
('streams', [StreamDescription(stream_id='summary_by_sender', description='A list of email summaries grouped by each email sender, excluding ads', fields={'sender': 'name xxx, string', 'summary': 'sum xxx, string'})])
There are multiple input streams available. The agent should select some of them:
('streams', [StreamDescription(stream_id='all_email', description='All email messages', fields={'sender': 'name xxx, string', 'Content': 'text xxx, string'})])
"""

