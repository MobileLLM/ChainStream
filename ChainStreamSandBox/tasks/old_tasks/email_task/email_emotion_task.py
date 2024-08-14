from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
import random
from ChainStreamSandBox.raw_data import EmailData

random.seed(6666)


class OldEmailTask2(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_email_stream = None
        self.input_email_stream = None
        # self.task_description = (
        #     "Retrieve data from the input stream 'all_emails'. "
        #     "Process each email to extract information from the 'Content' fields in the email dictionary: "
        #     "Classify the email content into one of the categories (positive, negative, neutral, other) using an LLM."
        #     "Add the email subject followed by the classification response to the output stream 'cs_emails'."
        # )
        self.input_description = [
                {
                    "stream_id": "all_emails",
                    "description": "The input stream 'all_emails' contains a list of dictionaries, where each dictionary represents an email. The dictionary contains the fields 'Subject' and 'Content'.",
                    "fields": ["Subject", "Content"],
                }
            ]

        self.output_description = [{
            "stream_id": "cs_emails",
            "description": "A list of email summaries for each email sender, excluding ads",
            "fields": {
                "sender": "The email sender, string",
                "summary": "The summary of previous emails of the sender, string"
            }
        }]
        self.output_description = "The output stream 'cs_emails' will contain the email subject followed by the classification response."
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
            prompt = "Classify the following email contents into one of the categories: positive, negative, neutral, other.Choose one and explain"
            response = self.llm.query(cs.llm.make_prompt(prompt,email_content))
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
