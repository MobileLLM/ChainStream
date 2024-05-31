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
            prompt = "Based on the information received on several stock markets, please recommend the best day to invest in which stock to maximize profit.Just tell me the date and the symbol of the stock"
            prompt = [
                {
                    "role": "user",
                    "content": prompt+str(stocks)
                }
            ]
            response = self.llm.query(prompt)
            print(response)
            self.output_stream.add_item(response)
        self.input_stream.register_listener(self, process_stocks)

    def stop(self):
        self.input_stream.unregister_listener(self)

    '''
    oj = OJ(StockTaskConfig(), agent_file)
    oj.start_test_agent()