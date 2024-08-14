from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
import random
from ChainStreamSandBox.raw_data import EmailData
random.seed(6666)


class OldEmailTask7(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_emails' and process the values corresponding to the 'Subject' and 'Content' keys in the email dictionary: "
            "Use LLM to write a brief summary of the email contents."
            "Add the generated response along with the email subject to the output stream 'cs_emails'."
        )

        self.email_data = EmailData().get_emails(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_email_agent")
        self.input_stream = cs.get_stream(self,"all_emails")
        self.output_stream = cs.get_stream(self,"cs_emails")
        self.llm = get_model("Text")
    def start(self):
        def process_email(email):
            email_content = email["Content"]
            email_subject = email["Subject"]    
            prompt = "Write a brief summary of the following email contents"
            response = self.llm.query(cs.llm.make_prompt(prompt,email_content))
            print(email_subject+" : "+response)
            self.output_stream.add_item(email_subject+" : "+response)
        self.input_stream.for_each(process_email)
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_emails')
        self.output_email_stream = cs.stream.create_stream(self, 'cs_emails')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime):
        email_list = []
        for message in self.email_data:
            self.input_email_stream.add_item(message)
            email_list.append(message)
        return email_list
