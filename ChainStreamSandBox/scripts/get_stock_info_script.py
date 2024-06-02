if __name__ == "__main__":
    from tasks import ALL_TASKS

    StockTaskConfig = ALL_TASKS['StockTask']

    agent_file = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_news_agent")
        self.input_stream = cs.get_stream("all_stocks")
        self.output_stream = cs.get_stream("cs_stocks")
        self.llm = get_model(["text"])
    def start(self):
        def process_stocks(stocks):
            # stocks_index = stocks["symbol"]
            # stocks_date = stocks["date"]           
            # #print(news_category)
            self.output_stream.add_item(stocks)
        self.input_stream.register_listener(self, process_stocks)

    def stop(self):
        self.input_stream.unregister_listener(self)

    '''
    oj = OJ(StockTaskConfig(), agent_file)
    oj.start_test_agent()