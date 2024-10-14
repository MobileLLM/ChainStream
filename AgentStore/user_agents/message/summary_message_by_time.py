from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.memory import get_memory, create_memory
from chainstream.llm import get_model, make_prompt
from chainstream.context import TextBuffer


class SummaryMessageEveryDay(Agent):
    def __init__(self):
        super().__init__("summary_message_every_day")
        self.clock = get_stream("clock_every_day")
        self.input_stream = get_stream("all_message")
        self.output_stream = create_stream("summaryd_message_every_day")
        self.llm = get_model("text")
        self.message_buffer = TextBuffer()

    def start(self):
        def receive_message(message):
            self.message_buffer.add(message)

        def summary_message_every_day(new_day):
            prompt = make_prompt(self.message_buffer, "summarize the messages you received today: ")
            summary = self.llm.query(prompt)
            self.output_stream.add_item({"summary": summary, "timestamp": new_day})

        self.clock.for_each(self, summary_message_every_day)
        self.input_stream.for_each(self, receive_message)

    def stop(self):
        self.clock.unregister_all(self)
        self.input_stream.unregister_all(self)


class SummaryMessageEveryHour(Agent):
    def __init__(self):
        super().__init__("summary_message_every_hour")
        self.clock = get_stream("clock_every_hour")
        self.input_stream = get_stream("all_message")
        self.output_stream = create_stream("summaryd_message_every_hour")
        self.llm = get_model("text")
        self.message_buffer = TextBuffer()

    def start(self):
        def receive_message(message):
            self.message_buffer.add(message)

        def summary_message_every_hour(new_hour):
            prompt = make_prompt(self.message_buffer, "summarize the messages you received this hour: ")
            summary = self.llm.query(prompt)
            self.output_stream.add_item({"summary": summary, "timestamp": new_hour})

        self.clock.for_each(self, summary_message_every_hour)
        self.input_stream.for_each(self, receive_message)

    def stop(self):
        self.clock.unregister_all(self)
        self.input_stream.unregister_all(self)


class SummaryMessageEveryMonth(Agent):
    def __init__(self):
        super().__init__("summary_message_every_month")
        self.clock = get_stream("clock_every_month")
        self.input_stream = get_stream("all_message")
        self.output_stream = create_stream("summaryd_message_every_month")
        self.llm = get_model("text")
        self.message_buffer = TextBuffer()

    def start(self):
        def receive_message(message):
            self.message_buffer.add(message)

        def summary_message_every_month(new_month):
            prompt = make_prompt(self.message_buffer, "summarize the messages you received this month: ")
            summary = self.llm.query(prompt)
            self.output_stream.add_item({"summary": summary, "timestamp": new_month})

        self.clock.for_each(self, summary_message_every_month)
        self.input_stream.for_each(self, receive_message)

    def stop(self):
        self.clock.unregister_all(self)
        self.input_stream.unregister_all(self)
