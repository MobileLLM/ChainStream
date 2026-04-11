from AgentGenerator.prompt import get_base_prompt, FilterErrorFeedbackProcessor
from AgentGenerator.generator.generator_base import AgentGeneratorBase
from AgentGenerator.io_model import StreamListDescription
from ChainStreamSandBox import get_sandbox_class
import datetime
import json
import re


class ChainStreamChatGeneratorPythonFeedback(AgentGeneratorBase):
    """
    Chat-based agent generator with feedback-guided refinement capabilities.
    Combines the chat interface from ChainStreamChatGeneratorPython with the 
    iterative feedback mechanism from feedback-guided generators.
    """

    def __init__(self, framework_example_number=0, base_prompt_example_select_policy='random', 
                 max_loop=20, sandbox_type='chainstream', only_print_last=False):
        super().__init__()
        
        self.example_number = framework_example_number
        self.base_prompt_example_select_policy = base_prompt_example_select_policy
        
        # Feedback-guided properties
        self.max_loop = max_loop
        self.sandbox_type = sandbox_type
        self.sandbox_class = get_sandbox_class(sandbox_type)
        self.feedback_processor = FilterErrorFeedbackProcessor()
        
        self.loop_count = 0
        self.history = None
        self.only_print_last = only_print_last
        self.last_agent_code = None
        
    def get_base_prompt(self, output_stream, input_stream, message=None) -> str:
        if message is None:
            raise ValueError("Message is required for chainstream chat generator")
        return get_base_prompt(output_stream, input_stream,
                               framework_name="chainstream",
                               example_number=self.example_number,
                               mission_name="chat",
                               command_name="chat",
                               need_feedback_example=True,
                               task_now=self.task.__class__.__name__ if self.task else "ChatTask",
                               example_select_policy=self.base_prompt_example_select_policy,
                               chat_message=message,
                               target_language="python"
                               )

    def process_response(self, response) -> str:
        """
        Process the LLM response which should be in JSON format.
        Expected JSON structure:
        {
            "new_code": "...",
            "new_history": "...",
            "message_to_user": "..."
        }
        """
        # Try to extract JSON from response (in case there's extra text)
        json_match = re.search(r'\{[\s\S]*"new_code"[\s\S]*\}', response)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = response.strip()
        
        try:
            result = json.loads(json_str)
            # Store the additional fields for backend to use
            self._last_new_history = result.get('new_history', '')
            self._last_message_to_user = result.get('message_to_user', '')
            # Return the new_code as the main output
            return result.get('new_code', '')
        except json.JSONDecodeError as e:
            # Fallback: if JSON parsing fails, return the response as-is (but cleaned)
            self._last_new_history = ''
            self._last_message_to_user = f'Warning: Failed to parse JSON response. Error: {e}'
            return response.replace("'''", " ").replace("```", " ").replace("python", "").strip()

    def get_last_response_metadata(self):
        """Return the last new_history and message_to_user from process_response"""
        return {
            'new_history': getattr(self, '_last_new_history', ''),
            'message_to_user': getattr(self, '_last_message_to_user', '')
        }

    def _query_llm(self, prompt, stop=None):
        """Query LLM with feedback context"""
        prompt_list = [
            {
                "role": "system",
                "content": prompt,
                "stop": stop
            }
        ]
        response = self.llm.query(prompt_list)
        
        if self.verbose:
            if self.only_print_last:
                print(f"Loop: {self.loop_count}")
            else:
                print(
                    f"####################################\nQuerying LLM at {datetime.datetime.now()}\n"
                    f"Response: {response}\n#######Testing Code: {self.loop_count-1}#######\n")
        return response

    def process_sandbox_feedback(self, sandbox_feedback):
        """Process sandbox feedback through feedback processor"""
        return self.feedback_processor(sandbox_feedback)

    def step(self, code) -> (str, bool):
        """
        Execute code in sandbox and get feedback.
        Returns: (feedback_prompt, done)
        """
        done = False
        
        try:
            entity = code.strip()
            if entity.startswith("```python") and entity.endswith("```"):
                entity = entity[len("```python"):-3].strip()
            obs = self.sandbox_exec(entity, use_real_task=False)
        except Exception as e:
            obs = f"[SandboxError] {e}"
        
        return obs, done

    def sandbox_exec(self, agent_code, stream_items=None, use_real_task=False):
        """Execute code in sandbox and return feedback"""
        from AgentGenerator.generator.generator_base import FakeTaskConfig
        
        if stream_items is None and use_real_task is False:
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
            if use_real_task:
                tmp_task = self.task
            else:
                tmp_task = FakeTaskConfig(input_description=self.input_description,
                                        output_description=self.output_description)
                if stream_items is not None:
                    tmp_task.set_input_items(stream_items)
            
            sandbox = self.sandbox_class(tmp_task, agent_code, save_result=False)
            sandbox_feedback = sandbox.start_test_agent()
        
        feedback_prompt = self.process_sandbox_feedback(sandbox_feedback)
        return feedback_prompt

    def generate_agent_chat_with_feedback(self, message, output_description, input_description=None, 
                                          use_selector=False, task=None) -> (str, int):
        """
        Generate agent code with chat message and feedback-guided refinement.
        Returns: (code, latency, tokens) or (code, latency, tokens, loop_count, history)
        """
        self.task = task
        self.output_description = output_description
        self.input_description = input_description
        
        self.stream_selector.set_all_stream_list(input_description)
        
        # Do not specify input_description, let llm make up the input stream
        if input_description is None:
            output_stream, input_stream = self.stream_selector.select_stream(output_description, select_policy='none')
        else:
            if not use_selector:
                # Specify input_description, use all input streams
                output_stream, input_stream = self.stream_selector.select_stream(output_description,
                                                                                 select_policy='all')
            else:
                # Specify input_description, use llm to select input streams
                output_stream, input_stream = self.stream_selector.select_stream(output_description,
                                                                                 select_policy='llm')
        
        start_time = datetime.datetime.now()
        code = self.generate_agent_impl_with_feedback(output_stream, input_stream, message)
        end_time = datetime.datetime.now()
        
        latency = (end_time - start_time).total_seconds()
        tokens = self.get_llm_token_count()
        
        return code, latency, tokens, self.loop_count, self.history

    def generate_agent_impl_with_feedback(self, output_stream, input_stream, message=None) -> str:
        """
        Generate agent with iterative feedback refinement.
        Supports user message for context-aware generation.
        """
        all_prompt = self.get_base_prompt(output_stream, input_stream, message)
        print(f"Initial Prompt:\n{all_prompt}\n{'='*50}")
        n_calls = 0
        n_badcalls = 0
        done = False
        self.last_agent_code = None
        
        for i in range(self.max_loop):
            n_calls += 1
            self.loop_count += 1
            
            # Query LLM for thought and code
            thought_code = self._query_llm(all_prompt + f"Thought {i}:", stop=[f"\nObservation {i}:", f"\nFinish."])
            
            if f"\nObservation {i}:" in thought_code:
                thought_code = thought_code.strip().split(f"\nObservation {i}:")[0].strip()
            
            try:
                # Check if LLM decided to finish
                if thought_code.endswith(f"Finish."):
                    tmp_thought_code = thought_code.strip()[:-len(f"Finish.")]
                    if f"\nCode {i}:" in tmp_thought_code:
                        thought, code = tmp_thought_code.strip().split(f"\nCode {i}:")
                        code = code.strip()
                        actual_python_code = self.process_response(code).strip()
                        if actual_python_code.startswith("```python") and actual_python_code.endswith("```"):
                            actual_python_code = actual_python_code[len("```python"):-len("```")].strip()
                        self.last_agent_code = actual_python_code
                    all_prompt += thought_code.strip()
                    self.history = all_prompt
                    done = True
                    break
                
                if thought_code.endswith(f"Observation {i}:"):
                    thought_code = thought_code.strip()[:-len(f"Observation {i}:")]
                
                thought, code = thought_code.strip().split(f"\nCode {i}:")
            
            except Exception as e:
                if self.verbose:
                    print(f'Failed to parse thought_code: {thought_code}')
                n_badcalls += 1
                n_calls += 1
                thought = thought_code.strip().split('\n')[0]
                code = self._query_llm(all_prompt + f"Thought {i}: {thought}\nCode {i}:", stop=[f"\n"]).strip()
            
            code = code.strip()
            actual_python_code = self.process_response(code).strip()
            if actual_python_code.startswith("```python") and actual_python_code.endswith("```"):
                actual_python_code = actual_python_code[len("```python"):-len("```")].strip()
            elif actual_python_code.startswith("```") and actual_python_code.endswith("```"):
                actual_python_code = actual_python_code[len("```"):-len("```")].strip()
            
            self.last_agent_code = actual_python_code
            
            # Execute code and get feedback
            error_prompt, done_step = self.step(actual_python_code)
            
            error = error_prompt.replace('\\n', '')
            step_str = f"Thought {i}: {thought}\nCode {i}: {code}\nObservation {i}: {error}\n"
            all_prompt += step_str
            
            self.history = all_prompt
            
            if done_step:
                break
        
        if not done:
            error_prompt, done = self.step("Finish.")
        
        self.last_agent_code = self.last_agent_code.strip()
        if self.last_agent_code.startswith("```python") and self.last_agent_code.endswith("```"):
            self.last_agent_code = self.last_agent_code[len("```python"):-len("```")].strip()
        
        if self.only_print_last and self.verbose:
            print(self.history.split("Thought 0:")[-1])
        
        return self.last_agent_code

    def process_response(self, response) -> str:
        """
        Process LLM response - can be overridden by subclasses for custom JSON handling.
        """
        # Try to extract JSON from response (in case there's extra text)
        json_match = re.search(r'\{[\s\S]*"new_code"[\s\S]*\}', response)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = response.strip()
        
        try:
            result = json.loads(json_str)
            # Store the additional fields for backend to use
            self._last_new_history = result.get('new_history', '')
            self._last_message_to_user = result.get('message_to_user', '')
            # Return the new_code as the main output
            return result.get('new_code', '')
        except json.JSONDecodeError as e:
            # Fallback: if JSON parsing fails, return the response as-is (but cleaned)
            self._last_new_history = ''
            self._last_message_to_user = f'Warning: Failed to parse JSON response. Error: {e}'
            return response.replace("'''", " ").replace("```", " ").replace("python", "").strip()


if __name__ == "__main__":
    agent_generator = ChainStreamChatGeneratorPythonFeedback(max_loop=5)
    result = agent_generator.generate_agent_chat_with_feedback(
        message="Create an agent that summarizes emails by sender",
        output_description=StreamListDescription(streams=[{
            "stream_id": "summary_by_sender",
            "description": "A list of email summaries grouped by each email sender for first 3 emails, excluding advertisement emails",
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
    
    agent_code, latency, tokens, loop_count, history = result
    print("Generated Agent Code:")
    print(agent_code)
    print(f"\nLatency: {latency}s")
    print(f"Tokens: {tokens}")
    print(f"Loop Count: {loop_count}")
    print(f"\nGeneration History (last 500 chars):")
    print(history[-500:] if history else "No history")
