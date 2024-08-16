from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import AirlineTwitterData
from AgentGenerator.io_model import StreamListDescription


class OldTweetTask9(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_tweet_stream = None
        self.input_tweet_stream = None
        self.output_record = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_tweets",
            "description": "A list of twitter information",
            "fields": {
                "airline_sentiment": "The sentiment of the twitter on airline,string",
                "negative_reason": "The reason of negativeness,string",
                "airline": "The name of the airline,string",
                "name": "The name of the user,string",
                "retweet_count": "The number of the retweet,int",
                "text": "The text of the tweet,string",
                "tweet_created": "The time of the tweet,string",
                "tweet_location": "The location of the tweet,string",
                "user_timezone": "The timezone of the twitter user,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "tweets_timezone",
                "description": "A series of statistics on the timezone of the twitter user",
                "fields": {
                    "text": "The text of the tweet,string",
                    "user_timezone": "The timezone of the twitter user,string"
                }
            }
        ])
        self.tweet_data = AirlineTwitterData().get_twitter(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_twitter_agent")
        self.input_stream = cs.get_stream(self,"all_tweets")
        self.output_stream = cs.get_stream(self,"tweets_timezone")
        self.llm = get_model("Text")
    def start(self):
        def process_tweet(tweets):
            user_timezone = tweets["user_timezone"]
            text = tweets["text"]        
            self.output_stream.add_item({
                "text":text,
                "user_timezone":user_timezone
            })
        self.input_stream.for_each(process_tweet)
        '''

    def init_environment(self, runtime):
        self.input_tweet_stream = cs.stream.create_stream(self, 'all_tweets')
        self.output_tweet_stream = cs.stream.create_stream(self, 'tweets_timezone')
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
