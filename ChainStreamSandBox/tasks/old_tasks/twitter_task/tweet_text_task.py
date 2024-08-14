from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import AirlineTwitterData


class OldTweetTask7(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_tweet_stream = None
        self.input_tweet_stream = None
        self.output_record = None
        self.task_description = (
            "Retrieve data from the input stream 'all_tweets' and process the values corresponding to the 'text' key in the tweets dictionary: "
            "Add the twitter text to the output stream 'cs_tweets'."
        )
        self.tweet_data = AirlineTwitterData().get_twitter(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_twitter_agent")
        self.input_stream = cs.get_stream(self,"all_tweets")
        self.output_stream = cs.get_stream(self,"cs_tweets")
        self.llm = get_model("Text")
    def start(self):
        def process_tweet(tweets):
            tweets_text = tweets["text"]        
            self.output_stream.add_item(tweets_text)
        self.input_stream.for_each(process_tweet)
        '''

    def init_environment(self, runtime):
        self.input_tweet_stream = cs.stream.create_stream(self, 'all_tweets')
        self.output_tweet_stream = cs.stream.create_stream(self, 'cs_tweets')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_tweet_stream.for_each(record_output)

    def start_task(self, runtime):
        twitter_list = []
        for info in self.tweet_data:
            self.input_tweet_stream.add_item(info)
            twitter_list.append(info)
        return twitter_list


if __name__ == '__main__':
    config = TweetTextConfig()
