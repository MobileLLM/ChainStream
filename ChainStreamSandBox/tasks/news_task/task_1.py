from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class NewsTask1(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None

        self.eos_gap = eos_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "summary_from_dialogue",
                "description": "A summary of the dialogues in conference from the news",
                "fields": {
                    "conference": "name xxx, string",
                    "summary": "sum xxx, string"
                }
            }
        ])

        self.paper_data = NewsData().get_random_articles(paper_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForNewsTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_news_task_1"):
        super().__init__(agent_id)
        self.news_input = cs.get_stream(self, "all_news")
        self.news_output = cs.get_stream(self, "summary_from_dialogue")
        # self.email_output = cs.create_stream(self, {
        #     "stream_id": "summary_from_dialogue",
        #     "description": "A list of email summaries for each email sender, excluding ads",
        #     "fields": {
        #         "sender": "name xxx, string",
        #         "summary": "sum xxx, string"
        #     }
        # })

        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_politics(email):
            email_type = email['category']
            if email_type == 'POLITICS':
                return email
        def extract_dialogues(email):
            prompt = "is this news on conference? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(email['headline'], prompt))
            print("filter_conference", res)
            if res.lower() == 'y':
                return email
        # def group_by_sender(email_list):
        #     email_list = email_list['item_list']
        #     sender_group = {}
        #     for email in email_list:
        #         if email['sender'] not in sender_group:
        #             sender_group[email['sender']] = [email]
        #         else:
        #             sender_group[email['sender']].append(email)
        # 
        #     print("group_by_sender", list(sender_group.values()))
        #     return list(sender_group.values())

        def sum_by_dialogues(news):
            date = news[0]['date']
            prompt = "Summarize the main idea of the dialogues in the conference"
            print("sum_by_dialogues: query", [x['short_description'] for x in news], prompt)
            print("sum_by_sender", res)
            self.email_output.add_item({
                "conference_date": date,
                "summary": res
            })

        self.news_input.for_each(filter_politics).for_each(extract_dialogues).batch(by_count=2).for_each(sum_by_dialogues)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_news')
        self.output_paper_stream = cs.stream.create_stream(self, 'summary_from_dialogue')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.paper_data:
            # message['sender'] = message['From']
            # print("adding message", message)
            sent_messages.append(message)
            self.input_paper_stream.add_item(message)
        return sent_messages





