from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import StockData

random.seed(6666)


class StockPurchaseConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_stock_stream = None
        self.input_stock_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_stocks'."
            "For each stock item, use LLM to recommend the best day to invest to maximize profit based on received stock market information. "
            "Add the LLM response to the output stream 'cs_stocks'."
        )
        self.stock_data = StockData().get_stocks(10)
        self.agent_example = '''
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
            response = self.llm.query(cs.llm.make_prompt(prompt,str(stocks)))
            self.output_stream.add_item(response)
        self.input_stream.for_each(process_stocks)
        
        '''

    def init_environment(self, runtime):
        self.input_stock_stream = cs.stream.create_stream(self, 'all_stocks')
        self.output_stock_stream = cs.stream.create_stream(self, 'cs_stocks')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_stock_stream.for_each(record_output)

    def start_task(self, runtime):
        stock_list = []
        for stock in self.stock_data:
            self.input_stock_stream.add_item(stock)
            stock_list.append(stock)
        return stock_list


if __name__ == '__main__':
    config = StockPurchaseConfig()
