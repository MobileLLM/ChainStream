from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData


class OldNewsTask2(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_news_stream = None
        self.input_news_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_news' and process the values corresponding to the 'headline' and 'category' keys in the news dictionary: "
            "Add the news headline followed by the category to the output stream 'cs_news'."
        )

        self.news_data = NewsData().get_random_articles(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_news_agent")
        self.input_stream = cs.get_stream(self,"all_news")
        self.output_stream = cs.get_stream(self,"cs_news")
        self.llm = get_model("Text")
    def start(self):
        def process_news(news):
            news_headline = news["headline"]
            news_category = news["category"]           
            #print(news_category)
            self.output_stream.add_item(news_headline+" : "+news_category)
        self.input_stream.for_each(process_news)
        '''

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream(self, 'all_news')
        self.output_news_stream = cs.stream.create_stream(self, 'cs_news')
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


