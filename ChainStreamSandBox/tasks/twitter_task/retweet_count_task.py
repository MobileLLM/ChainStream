from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import AirlineTwitterData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class TweetTask1(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_tweet_stream = None
        self.input_tweet_stream = None
        self.output_record = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Interpersonal_relationship,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_tweets",
            "description": "A series of twitter information",
            "fields": {
                "retweet_count": "The number of the retweet, int",
                "text": "The text of the tweet, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "retweet_count",
                "description": "A series of tweet texts with the counting numbers of retweet",
                "fields": {
                    "text": "The text of the tweet, string",
                    "retweet_count": "The number of the retweet, int"
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
        self.output_stream = cs.get_stream(self,"retweet_count")
        self.llm = get_model("Text")
    def start(self):
        def process_tweet(tweets):
            retweet_count = tweets["retweet_count"]
            text = tweets["text"]  
            self.output_stream.add_item({
                "text": text,
                "retweet_count": retweet_count
            })
        self.input_stream.for_each(process_tweet)
        '''

    def init_environment(self, runtime):
        self.input_tweet_stream = cs.stream.create_stream(self, 'all_tweets')
        self.output_tweet_stream = cs.stream.create_stream(self, 'retweet_count')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['retweet_count'].append(data)

        self.output_tweet_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        twitter_dict = {'all_tweets': []}
        for info in self.tweet_data:
            self.input_tweet_stream.add_item(info)
            twitter_dict['all_tweets'].append(info)
        return twitter_dict
