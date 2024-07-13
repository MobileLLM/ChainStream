from tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class ArxivTask1(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None

        self.output_stream_description = StreamListDescription(output_description=[
            {
                "stream_id": "summary_by_sender",
                "description": "A list of email summaries for each email sender, excluding ads",
                "fields": {
                    "sender": "name xxx, string",
                    "summary": "sum xxx, string"
                }
            }
        ])

        self.paper_data = ArxivData().get_random_papers(paper_number)
        self.agent_example = '''
        ### Agent code with new API
class Agent(Agent):
  def __init__(self):
    self.email_input = cs.get_stream("all_email")

    self.email_output = cs.create({
      "stream_id": "summary_by_sender",
      "description": "A list of email summaries for each email sender, excluding ads",
      "fields": {
        "sender": "name xxx, string",
        "summary": "sum xxx, string"
      }
    })

    # tmp stream, no fields defination.
    self.buffer = cs.buffer()

  def start():
    def filter_ads(email):
        prompt = "is this email an ads? answer y or n"
      res = self.llm.query(make_prompt(email, prompt))
      if res == 'n':
        return email

    # EOS as a trigger
    def group_by_sender(email_list):
      sender_group = {}
      for email in email_list:
        if email['sender'] not in sender_group:
          sender_group[email['sender']] = [email]
        else:
          sender_group[email['sender']].append(email)

      return sender_group

    def sum_by_sender(sender_email):
      sender = sender_email[0]['sender']
      prompt = "sum these all email here"
      res = self.llm.query(make_prompt([x['content'] for x in sender_email], prompt))

      self.email_output.add_item({
        "sender": sender,
        "sum": res
      })

    self.email_input.for_each(filter_ads).batch(by_key="EOS").for_each(group_by_sender).for_each(sum_by_sender)

        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream('all_arxiv')
        self.output_paper_stream = cs.stream.create_stream('cs_arxiv')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(self, record_output)

    def start_task(self, runtime):
        for message in self.paper_data:
            self.input_paper_stream.add_item(message)


if __name__ == '__main__':
    config = ArxivTask1()
