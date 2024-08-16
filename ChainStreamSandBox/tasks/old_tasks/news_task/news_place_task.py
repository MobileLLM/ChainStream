from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData
from AgentGenerator.io_model import StreamListDescription


class OldNewsTask7(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_news_stream = None
        self.input_news_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_news",
            "description": "A list of news information",
            "fields": {
                "headline": "The headline of the news,string",
                "short_description": "The short description of the news,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "news_place",
                "description": "A list of the location extracted from the news based on the news short description",
                "fields": {
                    "headline": "The headline of the news,string",
                    "news_place": "The location where the news took place,string"
                }
            }
        ])

        self.news_data = NewsData().get_random_articles(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_news_agent")
        self.input_stream = cs.get_stream(self,"all_news")
        self.output_stream = cs.get_stream(self,"news_place")
        self.llm = get_model("Text")
    def start(self):
        def process_news(news):
            news_headline = news["headline"]
            news_short_description = news["short_description"]       
            prompt = "Now you have received some news,please tell me where the news happened"          
            response = self.llm.query(cs.llm.make_prompt(prompt,news_short_description))
            self.output_stream.add_item({
            "headline":news_headline,
            "news_place":response})
        self.input_stream.for_each(process_news)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')
        self.output_news_stream = cs.stream.create_stream(self, 'news_place')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_news_stream.for_each(record_output)

    def start_task(self, runtime):
        news_list = []
        for message in self.news_data:
            self.input_news_stream.add_item(message)
            news_list.append(message)
        return news_list
