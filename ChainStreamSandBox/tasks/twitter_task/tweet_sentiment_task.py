from ..task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import AirlineTwitterData


class TweetSentimentConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_twitter_stream = None
        self.input_twitter_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_tweets' and process the values corresponding to the 'airline_sentiment' key in the tweets dictionary: "
            "Add the airline sentiment value to the output stream 'cs_tweets'."
        )
        self.tweet_data = AirlineTwitterData().get_twitter(10)
        self.agent_example = '''
        import chainstream as cs
        from chainstream.llm import get_model
        class testAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("test_twitter_agent")
                self.input_stream = cs.get_stream("all_tweets")
                self.output_stream = cs.get_stream("cs_tweets")
                self.llm = get_model(["text"])
            def start(self):
                def process_tweet(tweets):
                    airline_sentiment = tweets["airline_sentiment"]        
                    self.output_stream.add_item(airline_sentiment)
                self.input_stream.register_listener(self, process_tweet)

            def stop(self):
                self.input_stream.unregister_listener(self)
        '''

    def init_environment(self, runtime):
        self.input_tweet_stream = cs.stream.create_stream('all_tweets')
        self.output_tweet_stream = cs.stream.create_stream('cs_tweets')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_tweet_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for info in self.tweet_data:
            self.input_tweet_stream.add_item(info)


if __name__ == '__main__':
    config = TweetSentimentConfig()
