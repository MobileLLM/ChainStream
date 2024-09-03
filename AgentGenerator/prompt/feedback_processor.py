from AgentGenerator.prompt.agent_example_selector import AgentExampleSelector


class FeedbackProcessorBase:
    def __init__(self):
        pass

    def process_feedback(self, sandbox_feedback, last_code=None):
        raise NotImplementedError('Subclasses of FeedbackProcessorBase must provide a process_feedback function')

    def __call__(self, sandbox_feedback, last_code=None):
        return self.process_feedback(sandbox_feedback, last_code=last_code)


class FilterErrorFeedbackProcessor(FeedbackProcessorBase):
    def __init__(self):
        super().__init__()

    def process_feedback(self, sandbox_feedback, last_code=None):
        if sandbox_feedback['start_agent'] != "[OK]":
            feedback = f"After starting the code, the sandbox reported: {sandbox_feedback['start_agent']}."
            if "stdout" in sandbox_feedback and "starting" in sandbox_feedback["stdout"] and sandbox_feedback["stdout"][
                "starting"] is not None:
                if sandbox_feedback["stdout"]["starting"] in [" ", "\n", ""]:
                    feedback += f" The stdout is empty."
                else:
                    feedback += f" And the stdout is: {sandbox_feedback['stdout']['starting'][:1000]}"
                    if len(sandbox_feedback["stdout"]["starting"]) > 1000:
                        feedback += "... "
                    else:
                        feedback += ". "
            return feedback
        else:
            err_msg = {}
            for err_name, err_value in sandbox_feedback["error_message"].items():
                if err_value is not None and err_value != []:
                    err_msg[err_name] = err_value
            if len(err_msg) == 0:
                tmp_error = "Your code can run without any error. "
            else:
                err_msg = str(err_msg)
                tmp_error = "After running the code, the sandbox reported: " + str(err_msg[:1000])
                if len(err_msg) > 1000:
                    tmp_error += "... "
                else:
                    tmp_error += ". "

            feedback = tmp_error + f"The output of the code is: {sandbox_feedback['output_stream_items']}"
            if "stdout" in sandbox_feedback and "running" in sandbox_feedback["stdout"] and sandbox_feedback["stdout"][
                "running"] is not None:
                if sandbox_feedback["stdout"]["running"] in [" ", "\n", ""]:
                    feedback += f" The stdout is empty."
                else:
                    feedback += f" And the stdout is: {sandbox_feedback['stdout']['running'][:1000]}"
                    if len(sandbox_feedback["stdout"]["running"]) > 1000:
                        feedback += "... "
                    else:
                        feedback += ". "

            feedback += " You can debug your code by using print statements and checking the stdout message. Do not use loggers in your code because log messages will not be visible in the sandbox output.\n"
            return feedback


class FilterErrorWithExampleFeedbackProcessor(FeedbackProcessorBase):
    def __init__(self, task_now=None, feedback_example_num=3, feedback_example_select_policy="llm"):
        super().__init__()

        if feedback_example_select_policy not in ['llm', 'random']:
            raise ValueError(f"Invalid select_policy: {feedback_example_select_policy}, select_policy should be 'llm' or 'random'.")
        self.feedback_example_select_policy = feedback_example_select_policy

        self.agent_example_selector = AgentExampleSelector(task_now, max_example_num=feedback_example_num)

    def process_feedback(self, sandbox_feedback, last_code=None):
        str_err = "No error message."
        str_output = "No output message."
        str_stdout = "No stdout message."

        if sandbox_feedback['start_agent'] != "[OK]":
            feedback = f"After starting the code, the sandbox reported: {sandbox_feedback['start_agent']}."
            if "stdout" in sandbox_feedback and "starting" in sandbox_feedback["stdout"] and sandbox_feedback["stdout"][
                "starting"] is not None:
                if sandbox_feedback["stdout"]["starting"] in [" ", "\n", ""]:
                    feedback += f" The stdout is empty."
                else:
                    feedback += f" And the stdout is: {sandbox_feedback['stdout']['starting'][:1000]}"
                    if len(sandbox_feedback["stdout"]["starting"]) > 1000:
                        feedback += "... "
                    else:
                        feedback += ". "
            return feedback, None
        else:
            err_msg = {}
            for err_name, err_value in sandbox_feedback["error_message"].items():
                if err_value is not None and err_value != []:
                    err_msg[err_name] = err_value
            if len(err_msg) == 0:
                tmp_error = "Your code can run without any error. "
            else:
                err_msg = str(err_msg)
                tmp_error = "After running the code, the sandbox reported: " + str(err_msg[:1000])
                str_err = str(err_msg)[:1000]
                if len(err_msg) > 1000:
                    tmp_error += "... "
                else:
                    tmp_error += ". "

            feedback = tmp_error + f"The output of the code is: {sandbox_feedback['output_stream_items']}"
            str_output = str(sandbox_feedback['output_stream_items'])[:1000]
            if "stdout" in sandbox_feedback and "running" in sandbox_feedback["stdout"] and sandbox_feedback["stdout"][
                "running"] is not None:
                if sandbox_feedback["stdout"]["running"] in [" ", "\n", ""]:
                    feedback += f" The stdout is empty."
                else:
                    feedback += f" And the stdout is: {sandbox_feedback['stdout']['running'][:1000]}"
                    str_stdout = str(sandbox_feedback['stdout']['running'])[:1000]
                    if len(sandbox_feedback["stdout"]["running"]) > 1000:
                        feedback += "... "
                    else:
                        feedback += ". "

            example_name = None
            try:
                example_code = None
                if self.feedback_example_select_policy == "llm":
                    example_code, example_name = self.agent_example_selector.get_llm_agent_example(
                        (str_err, str_stdout, str_output), current_code=last_code)
                elif self.feedback_example_select_policy == "random":
                    example_code, example_name = self.agent_example_selector.get_random_agent_example()

                if example_code is not None:
                    example_prompt = f"\nHere is an example code may help you solve the problem, example name: {example_name}, target_stream: {self.agent_example_selector.get_target_stream_by_name(example_name)}.\n```python\n{example_code}```\n"
                    feedback = f"{feedback}\n{example_prompt}"
            except Exception as e:
                print(f"[FeedbackProcessorExampleSelector] Error in getting example code: {str(e)}")

            feedback += " You can debug your code by using print statements and checking the stdout message. Do not use loggers in your code because log messages will not be visible in the sandbox output.\n"
            return feedback, example_name
