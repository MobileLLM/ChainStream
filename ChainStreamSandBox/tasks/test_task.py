from ChainStreamSandBox.tasks import ALL_TASKS
from ChainStreamSandBox.sandbox.chainstream_sandbox import ChainStreamSandBox


def test_task(task_id, agent=None):
    task = ALL_TASKS[task_id]()
    sandbox = ChainStreamSandBox(task, task.agent_example if agent is None else agent, save_path=None)

    report = sandbox.start_test_agent(return_report_path=False)

    print(report["output_stream_items"])
    print(report['stdout'])



if __name__ == '__main__':
    agent = """
import chainstream
from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.llm import get_model, make_prompt
from typing import Dict, Union, List

class NewsSummaryAgent(Agent):
    def __init__(self, agent_id: str = "news_summary_agent"):
        super().__init__(agent_id)
        # Get the input stream
        self.all_news_stream = get_stream(self, "all_news")
        # Retrieve the existing output stream
        self.summary_stream = get_stream(self, "summary_from_dialogue")
        # Get the large language model for summarization
        self.llm = get_model(["text"])

    def start(self) -> None:
        # Define the listener function to process the news items
        def filter_and_summarize_news(items: Dict) -> Union[Dict, None]:
            print(f"Processing batch: {items}")  # Debug print
            summaries = []
            for item in items['item_list']:
                if item['category'].lower() == 'politics':
                    # Create a prompt for the LLM to summarize the dialogues
                    prompt = make_prompt({
                        "task": "Summarize the dialogues in the conference from the following news item:",
                        "news_item": item['short_description']
                    })
                    print(f"Generated prompt: {prompt}")  # Debug print
                    summary = self.llm.query(prompt)
                    print(f"Generated summary: {summary}")  # Debug print
                    summaries.append({
                        'conference_date': item['date'],
                        'summary': summary
                    })
            return summaries if summaries else None
        
        # Register the listener function with batch processing
        self.all_news_stream.batch(by_count=2).for_each(filter_and_summarize_news, to_stream=self.summary_stream)

    def stop(self) -> None:
        # Unregister all listeners
        self.all_news_stream.unregister_all(self)
        """
    test_task("NewsTask1", agent=agent)
