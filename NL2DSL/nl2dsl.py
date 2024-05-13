from .query_openai import TextGPTModel


class NL2DSL:
    def __init__(self, model_name="gpt-3.5-turbo-1106"):
        self.model = TextGPTModel(model_name)
        self.max_token_len = 4096

    def generate_dsl(self, task):
        prompt  = [
            {
                "role": "system",
                "content": self._get_system_prompt(task)
            },
            {
                "role": "user",
                "content": self._get_user_prompt(task)
            }
        ]
        response = self.model.generate_response(prompt)
        return response
    

    def _get_system_prompt(self, task):
        pass

    def _get_user_prompt(self, task):
        pass