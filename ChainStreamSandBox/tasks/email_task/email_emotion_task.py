import json
import os
import csv
import random
import chainstream as cs
from datetime import datetime
from ..task_config_base import TaskConfigBase
import sys
from ChainStreamSandBox.raw_data import EmailData

csv.field_size_limit(2 ** 31 - 1)

random.seed(6666)


class EmailEmotionConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_emails'. "
            "Process each email to extract information from the 'Content' fields in the email dictionary: "
            "Classify the email content into one of the categories (positive, negative, neutral, other) using an LLM."
            "Add the email subject followed by the classification response to the output stream 'cs_emails'."
        )
        self.email_data = EmailData().get_emails(10)
        self.agent_example = '''
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
                    email_content = email["Content"]
                    email_subject = email["Subject"]           
                    prompt = "Classify the following email contents into one of the categories: positive, negative, neutral, other.Choose one and explain"
                    prompt = [
                        {
                            "role": "user",
                            "content": prompt+email_content
                        }
                    ]
                    response = self.llm.query(prompt)
                    print(email_subject+" : "+response)
                    self.output_stream.add_item(email_subject+" : "+response)
                self.input_stream.register_listener(self, process_email)
        
            def stop(self):
                self.input_stream.unregister_listener(self)
        '''
    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream('all_emails')
        self.output_email_stream = cs.stream.create_stream('cs_emails')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_email_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for message in self.email_data:
            self.input_email_stream.add_item(message)

    def record_output(self, runtime):
        print(self.output_stream)
        # json.dump(self.output_stream)
        if len(self.output_record) == 0:
            return False, "No emails found"
        else:
            return True, self.output_stream


if __name__ == '__main__':
    config = EmailEmotionConfig()
