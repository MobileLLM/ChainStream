from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from ChainStreamSandBox.raw_data import ArxivData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class MultiTask1(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.input_arxiv_stream = None
        self.is_office_event = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard,
                                domain=Domain_Task_tag.Office,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_email",
            "description": "All email messages",
            "fields": {
                "Subject": "the subject of the email, string"
            }
        }, {
            "stream_id": "all_arxiv",
            "description": "all of the arxiv data",
            "fields": {
                "title": "The title of the arxiv article, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "arxiv_recommendation",
                "description": "A stream of arxiv recommendation based on the subject keyword mentioned in the emails",
                "fields": {
                    "title": "the title of the recommended arxiv paper, string"
                }
            }
        ])
        self.arxiv_data = ArxivData().get_random_papers(number)
        self.email_data = EmailData().get_emails(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task_1"):
        super().__init__(agent_id)
        self.email_input = cs.get_stream(self, "all_email")
        self.arxiv_input = cs.get_stream(self, "all_arxiv")
        self.arxiv_output = cs.create_stream(self, "arxiv_recommendation")
        self.arxiv_buffer = Buffer()
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def save_arxiv(arxiv):
            self.arxiv_buffer.append(arxiv)
        self.arxiv_input.for_each(save_arxiv)

        def recommend_arxiv(subject_list):
            subjects = subject_list['item_list']
            arxiv_list = self.arxiv_buffer.pop_all()
            for subject in subjects:
                for arxiv in arxiv_list:
                    if subject in arxiv['title']:
                        self.arxiv_output.add_item({
                            'title':arxiv['title']
                            })
            return subject_list

        def extract_subject(email):
            Subject = email["Subject"]
            return Subject
        self.email_input.for_each(extract_subject).batch(by_count=13).for_each(recommend_arxiv)
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.input_arxiv_stream = cs.stream.create_stream(self, 'all_arxiv')
        self.output_email_stream = cs.stream.create_stream(self, 'arxiv_recommendation')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['arxiv_recommendation'].append(data)

        self.output_email_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.input_arxiv_stream = cs.stream.create_stream(self, 'all_arxiv')

    def init_output_stream(self, runtime):
        self.output_email_stream = cs.stream.get_stream(self, 'arxiv_recommendation')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['arxiv_recommendation'].append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        emails = [
            {
                "Date": "Mon, 23 Aug 2024 09:25:12 -0500 (CDT)",
                "From": "Smith, John",
                "To": "Doe, Jane; Lee, Robert; Wong, Angela; 'alex.jones@techcorp.com'; 'kim.park@innovations.com'",
                "Subject": "Stochastic Optimization",
                "Content": "\n\n\n-----Original Message-----\nSent:\tMonday, August 23, 2024 9:00 AM\n\nI'm organizing a discussion on the latest advancements in stochastic optimization techniques. We will cover several new algorithms and their applications in various fields.\n\nPlease let me know if you are interested and available to participate in the meeting. The session will be held next Friday at 2 PM.\n\nFeel free to invite anyone else who might be interested.\n\n\n-John"
            },
            {
                "Date": "Tue, 24 Aug 2024 10:14:50 -0500 (CDT)",
                "From": "Johnson, Emily",
                "To": "Brown, David; Green, Lisa; Taylor, Michael; 'chris.white@automotive.com'; 'nina.black@engineering.com'",
                "Subject": "Vehicle Localization",
                "Content": "\n\n\n-----Original Message-----\nSent:\tTuesday, August 24, 2024 10:00 AM\n\nWe're planning a workshop on vehicle localization technologies, focusing on both GPS-based and sensor fusion methods. The workshop aims to explore current challenges and future directions in the field.\n\nPlease confirm your availability if you wish to attend. The workshop is scheduled for next Wednesday at 10 AM.\n\nKindly forward this to colleagues who might be interested.\n\n\n-Emily"
            },
            {
                "Date": "Wed, 25 Aug 2024 08:47:35 -0500 (CDT)",
                "From": "Davis, Kevin",
                "To": "Clark, Sarah; King, Thomas; 'peter.baker@mediacorp.com'; 'linda.evans@streaming.com'",
                "Subject": "Video Compression",
                "Content": "\n\n\n-----Original Message-----\nSent:\tWednesday, August 25, 2024 8:30 AM\n\nI wanted to gather input on a new project focused on video compression techniques, particularly in the context of streaming services. We'll discuss the latest codecs and their potential impact on bandwidth and quality.\n\nPlease reply if you're interested in joining the brainstorming session next Thursday at 3 PM.\n\nDon't hesitate to share this with anyone else who might want to participate.\n\n\n-Kevin"
            }
        ]
        self.email_data.extend(emails)
        sent_info = {"all_email": [], "all_arxiv": []}
        for arxiv in self.arxiv_data:
            sent_info["all_arxiv"].append(arxiv)
            self.input_arxiv_stream.add_item(arxiv)
        for email in self.email_data:
            sent_info["all_email"].append(email)
            self.input_email_stream.add_item(email)
        return sent_info
