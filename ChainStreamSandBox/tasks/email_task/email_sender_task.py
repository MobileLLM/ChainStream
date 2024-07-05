import csv
import random
import chainstream as cs
from ..task_config_base import SingleAgentTaskConfigBase
from ChainStreamSandBox.raw_data import EmailData

csv.field_size_limit(2 ** 31 - 1)

random.seed(6666)


class EmailSenderConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_emails',"
            "and process the value corresponding to the 'From' and 'Subject' keys in the email dictionary: "
            "Add the email sender's address and subject to the output stream 'cs_emails'."
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
                    email_sender = email["From"]
                    email_subject = email["Subject"]           
                    print(email_subject+" : "+email_sender)
                    self.output_stream.add_item(email_subject+" : "+email_sender)
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


if __name__ == '__main__':
    config = EmailSenderConfig()
