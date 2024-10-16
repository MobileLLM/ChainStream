from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import AirlineTwitterData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class TweetTask9(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_tweet_stream = None
        self.input_tweet_stream = None
        self.output_record = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Interpersonal_relationship,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_tweets",
            "description": "A stream of twitter information",
            "fields": {
                "text": "The text of the tweet, string",
                "user_timezone": "The timezone of the twitter user, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "tweets_timezone",
                "description": "A stream of tweet texts with the statistics on the timezone of the twitter user",
                "fields": {
                    "text": "The text of the tweet, string",
                    "user_timezone": "The timezone of the twitter user, string"
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
        self.output_stream = cs.create_stream(self,"tweets_timezone")
        self.llm = get_model("Text")
    def start(self):
        def process_tweet(tweets):
            user_timezone = tweets["user_timezone"]
            text = tweets["text"]        
            self.output_stream.add_item({
                "text": text,
                "user_timezone": user_timezone
            })
        self.input_stream.for_each(process_tweet)
        '''

    def init_environment(self, runtime):
        self.input_tweet_stream = cs.stream.create_stream(self, 'all_tweets')
        self.output_tweet_stream = cs.stream.create_stream(self, 'tweets_timezone')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['tweets_timezone'].append(data)

        self.output_tweet_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_tweet_stream = cs.stream.create_stream(self, 'all_tweets')

    def init_output_stream(self, runtime):
        self.output_tweet_stream = cs.stream.get_stream(self, 'tweets_timezone')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['tweets_timezone'].append(data)

        self.output_tweet_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        twitter_dict = {'all_tweets': []}
        for info in self.tweet_data:
            self.input_tweet_stream.add_item(info)
            twitter_dict['all_tweets'].append(info)
        return twitter_dict
