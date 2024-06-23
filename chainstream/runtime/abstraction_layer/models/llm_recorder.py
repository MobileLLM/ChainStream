import collections

class LLMRecorder:
    def __init__(self):
        self.prompt_token = 0
        self.history = collections.OrderedDict()

    def record_query(self, prompt):
        pass

    def record_response(self, response):
        pass
