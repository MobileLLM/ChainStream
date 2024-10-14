
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

FEEDBACK_GUIDED_PROMPT_REAL_TASK = """
Task: Solve a chainstream agent generation task by alternating between Thought, Code, Observation and Finish steps.

Thought: In this step, the model will reason about the current situation, considering the previous Observation and planning the next Code step.
Code: In this step, the model will submit the agent code in the sandbox environment. Note that the model can only submit one code block at a time, using "```python" format.
Observation: In this step, the sandbox environment will return any error messages or reference documents based on the submitted code.
Finish: In this step, the model will submit the final message to indicate that the mission is finished.

The Thought step should always end with "Thought {i}:", and the model's response should end with "Observation {i}:". When the model is done, the Finish step should be used to submit the final message.
"""

FEEDBACK_GUIDED_FOR_REAL_TASK_EXAMPLE = """
Here is an example of how to generate an agent code with feedback guided mode:

`some previous prompt about the background here`

Thought 0: 
To solve this task, I need to write an agent that xxx.

Code 0: 
```python
# agent code here
```

Observation 0: 
The sandbox return the following error message: xxx

Thought 1: 
I need to verify the correctness of the agent code.

Code 1: 
```python
# new agent code here
```

Observation 1:
Your code can run without any error. The output of the code is: xxx

Thought 2: 
The code seems forget to handle the case where there is xxx. I need to modify the code.

Code 2: 
```python
# modified agent code here
```

Observation 2:
The modified code can run without any error. The output of the code is: xxx

Thought 3: 
The modified code seems to be correct. I can submit the code for review.

Code 3: 
```python
# final agent code here
```

Finish. 

Example end. Now let's begin to solve this mission.

"""

FEEDBACK_GUIDED_EXAMPLE = """
Here is an examples:

Mission: Your mission is to programme an agent with chainstream framework to get the following output streams:
('streams', [StreamDescription(stream_id='summary_by_sender', description='A list of email summaries grouped by each email sender, excluding ads', fields={'sender': 'name xxx, string', 'summary': 'sum xxx, string'})])
There are multiple input streams available. The agent should select some of them:
('streams', [StreamDescription(stream_id='all_email', description='All email messages', fields={'sender': 'name xxx, string', 'Content': 'text xxx, string'})])
"""

