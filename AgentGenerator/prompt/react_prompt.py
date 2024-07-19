
REACT_PROMPT = """Solve a chainstream agent generation task with interleaving Thought, Action, SandboxObservation steps. Thought can reason about the current situation, and Action can be two types: 
(1) Code[agent_code], which executes the agent code in the sandbox environment and returns the error message and reference document if any.
(2) Finish[agent_code], which returns the final agent code and finishes the task.
"""
