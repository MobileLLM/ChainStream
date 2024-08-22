class FeedbackProcessorBase:
    def __init__(self):
        pass

    def process_feedback(self, sandbox_feedback):
        raise NotImplementedError('Subclasses of FeedbackProcessorBase must provide a process_feedback function')

    def __call__(self, sandbox_feedback):
        return self.process_feedback(sandbox_feedback)


class FilterErrorFeedbackProcessor(FeedbackProcessorBase):
    def __init__(self):
        super().__init__()

    def process_feedback(self, sandbox_feedback):
        if sandbox_feedback['start_agent'] != "[OK]":
            feedback = f"After starting the code, the sandbox reported: {sandbox_feedback['start_agent']}."
            if "stdout" in sandbox_feedback and "starting" in sandbox_feedback["stdout"] and sandbox_feedback["stdout"][
                "starting"] is not None:
                if sandbox_feedback["stdout"]["starting"] in [" ", "\n", ""]:
                    feedback += f" The stdout is empty."
                else:
                    feedback += f" And the stdout is: {sandbox_feedback['stdout']['starting']}"
            return feedback
        else:
            err_msg = {}
            for err_name, err_value in sandbox_feedback["error_message"].items():
                if err_value is not None and err_value != []:
                    err_msg[err_name] = err_value
            if len(err_msg) == 0:
                tmp_error = "Your code can run without any error. "
            else:
                tmp_error = "After running the code, the sandbox reported: " + str(err_msg) + ". "

            feedback = tmp_error + f"The output of the code is: {sandbox_feedback['output_stream_items']}"
            if "stdout" in sandbox_feedback and "running" in sandbox_feedback["stdout"] and sandbox_feedback["stdout"][
                "running"] is not None:
                if sandbox_feedback["stdout"]["running"] in [" ", "\n", ""]:
                    feedback += f" The stdout is empty."
                else:
                    feedback += f" And the stdout is: {sandbox_feedback['stdout']['running']}"
            return feedback
