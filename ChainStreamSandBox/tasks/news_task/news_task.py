from ..task_config_base import TaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import NewsData


class NewsTaskConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_news_stream = None
        self.input_news_stream = None
        self.task_description = (
            "Read data from the input stream 'all_news', where each item is a dictionary with at least the keys "
            "'headline' and 'date'.Extract the values of the 'headline' and 'date' keys. Generate a string combining "
            "the headline and date, and output this string to the stream 'cs_news'."
            "and save the results in the output stream.")

        self.news_data = NewsData().get_random_articles(10)

    def init_environment(self, runtime):
        self.input_news_stream = cs.stream.create_stream('all_news')
        self.output_news_stream = cs.stream.create_stream('cs_news')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_news_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for message in self.news_data:
            self.input_news_stream.add_item(message)

    def record_output(self, runtime):
        print(self.output_record)
        if len(self.output_record) == 0:
            return False, "No news messages found"
        else:
            return True, "News messages found"


if __name__ == '__main__':
    config = NewsTaskConfig()
