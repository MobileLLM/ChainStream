import collections


class LLMRecorder:
    def __init__(self):
        self.prompt_token = 0
        self.history = collections.OrderedDict()

    def record_query(self, prompt):
        pass

    def record_response(self, response, prompt_tokens, completion_tokens):
        pass

    def record_start(self):
        pass

    def record_stop(self):
        pass
