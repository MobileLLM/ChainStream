if __name__ == "__main__":
    from tasks import ALL_TASKS

    EmailTaskConfig = ALL_TASKS['EmailTask']

    agent_file = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_email_agent")
        self.input_stream = cs.get_stream("all_emails")
        self.output_stream = cs.get_stream("cs_emails")
        self.llm = get_model(["text"])
    def start(self):
        def process_email(email):
            email_content = email["Content"]#[:500]            
            prompt = "Classify the following email content into one of the categories: positive, negative, neutral, other,choose one and explain"
            prompt = [
                {
                    "role": "user",
                    "content": prompt+email_content
                }
            ]
            response = self.llm.query(prompt)
            print(response)
            self.output_stream.add_item(response)
        self.input_stream.register_listener(self, process_email)

    def stop(self):
        self.input_stream.unregister_listener(self)

    '''
    oj = OJ(EmailTaskConfig(), agent_file)
    oj.start_test_agent()