from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import AirlineTwitterData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class OldTweetTask8(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_tweet_stream = None
        self.input_tweet_stream = None
        self.output_record = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Interpersonal_relationship,
                                scene=Scene_Task_tag.Other, modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_tweets",
            "description": "A list of twitter information",
            "fields": {
                "airline_sentiment": "The sentiment of the twitter on airline, string",
                "negative_reason": "The reason of negativeness, string",
                "airline": "The name of the airline, string",
                "name": "The name of the user, string",
                "retweet_count": "The number of the retweet, int",
                "text": "The text of the tweet, string",
                "tweet_created": "The time of the tweet, string",
                "tweet_location": "The location of the tweet, string",
                "user_timezone": "The timezone of the twitter user, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "tweets_time",
                "description": "A series of statistics on the sending time of the twitter",
                "fields": {
                    "text": "The text of the tweet, string",
                    "time_created": "The time of the tweet message, string"
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
        self.output_stream = cs.get_stream(self,"tweets_time")
        self.llm = get_model("Text")
    def start(self):
        def process_tweet(tweets):
            tweet_created = tweets["tweet_created"]
            text = tweets["text"]        
            self.output_stream.add_item({
                "text": text,
                "time_created": tweet_created
            })
        self.input_stream.for_each(process_tweet)
        '''

    def init_environment(self, runtime):
        self.input_tweet_stream = cs.stream.create_stream(self, 'all_tweets')
        self.output_tweet_stream = cs.stream.create_stream(self, 'tweets_time')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['tweets_time'].append(data)

        self.output_tweet_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        twitter_dict = {'all_tweets': []}
        for info in self.tweet_data:
            self.input_tweet_stream.add_item(info)
            twitter_dict['all_tweets'].append(info)
        return twitter_dict
