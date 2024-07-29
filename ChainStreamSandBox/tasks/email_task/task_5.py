from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class EmailTask5(SingleAgentTaskConfigBase):
    def __init__(self, email_number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_email_stream = None
        self.input_email_stream = None

        self.eos_gap = eos_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_reply",
                "description": "Replied list of emails,excluding ads",
                "fields": {
                    "content": "xxx, string",
                    "tag": "Received, string"
                }
            }
        ])

        self.email_data = EmailData().get_emails(email_number)
        self.agent_example = '''
from chainstream.agent import Agent
from chainstream.stream import get_stream, Stream
from chainstream.llm import get_model, make_prompt

class EmailSummaryAgent(Agent):
    def __init__(self, agent_id: str="email_summary_agent"):
        super().__init__(agent_id)
        self.input_stream = get_stream("all_email")
        self.llm_model = get_model(["text"])
        
    def start(self) -> None:
        self.input_stream.batch(by_count=10).for_each(self, self.summarize_emails)
        
    def summarize_emails(self, email_batch):
        summaries_by_sender = {}
        for email in email_batch['item_list']:
            sender = email['sender']
            content = email['Content']
            if "ads" not in content.lower():
                summary_prompt = make_prompt(f"Summarize this email: {content}")
                summary = self.llm_model.query(summary_prompt)
                if sender not in summaries_by_sender:
                    summaries_by_sender[sender] = []
                summaries_by_sender[sender].append(summary)
        
        summarized_list = [{"sender": sender, "summary": " ".join(summaries)} for sender, summaries in summaries_by_sender.items()]
        summary_stream = get_stream("summary_by_sender")
        summary_stream.add_item(summarized_list)
        
    def stop(self) -> None:
        self.input_stream.unregister_all(self)

        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.output_email_stream = cs.stream.create_stream(self, 'auto_reply')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.email_data:
            # message['sender'] = message['From']
            # print("adding message", message)
            sent_messages.append(message)
            self.input_email_stream.add_item(message)
        return sent_messages





