from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.memory import get_memory, create_memory
from chainstream.llm import get_model


class GirlFriendMessageFilter(Agent):
    def __init__(self):
        super(GirlFriendMessageFilter, self).__init__("GirlFriendMessageFilter")
        self.message_from = get_stream("all_messages")
        self.girl_friend_message = create_stream("girl_friend_message")

        self.llm = get_model("text")

    def start(self):
        def filter_message(message):
            message_content = message["content"]
            prompt = "Is this message from your girlfriend? Say 'yes' or 'no'."
            response = self.llm.generate(prompt, message_content)
            if response.lower() == "yes":
                self.girl_friend_message.add_item(message)

        self.message_from.for_each(self, filter_message)

    def stop(self):
        self.message_from.defor_each(self)

class FriendMessageFilter(Agent):
    def __init__(self):
        super(FriendMessageFilter, self).__init__("FriendMessageFilter")
        self.message_from = get_stream("all_messages")
        self.friend_message = create_stream("friend_message")

        self.llm = get_model("text")

    def start(self):
        def filter_message(message):
            message_content = message["content"]
            prompt = "Is this message from your friend? Say 'yes' or 'no'."
            response = self.llm.generate(prompt, message_content)
            if response.lower() == "yes":
                self.friend_message.add_item(message)

        self.message_from.for_each(self, filter_message)

    def stop(self):
        self.message_from.defor_each(self)


class WorkMessageFilter(Agent):
    def __init__(self):
        super(WorkMessageFilter, self).__init__("WorkMessageFilter")
        self.message_from = get_stream("all_messages")
        self.work_message = create_stream("work_message")

        self.llm = get_model("text")

    def start(self):
        def filter_message(message):
            message_content = message["content"]
            prompt = "Is this message work-related? Say 'yes' or 'no'."
            response = self.llm.generate(prompt, message_content)
            if response.lower() == "yes":
                self.work_message.add_item(message)

        self.message_from.for_each(self, filter_message)

    def stop(self):
        self.message_from.defor_each(self)


class AdvertisementMessageFilter(Agent):
    def __init__(self):
        super(AdvertisementMessageFilter, self).__init__("AdvertisementMessageFilter")
        self.message_from = get_stream("all_messages")
        self.advertisement_message = create_stream("advertisement_message")

        self.llm = get_model("text")

    def start(self):
        def filter_message(message):
            message_content = message["content"]
            prompt = "Is this message an advertisement? Say 'yes' or 'no'."
            response = self.llm.generate(prompt, message_content)
            if response.lower() == "yes":
                self.advertisement_message.add_item(message)

        self.message_from.for_each(self, filter_message)

    def stop(self):
        self.message_from.defor_each(self)


class EnglishMessageFilter(Agent):
    def __init__(self):
        super(EnglishMessageFilter, self).__init__("EnglishMessageFilter")
        self.message_from = get_stream("all_messages")
        self.english_message = create_stream("english_message")

        self.llm = get_model("text")

    def start(self):
        def filter_message(message):
            message_content = message["content"]
            prompt = "Is this message in English? Say 'yes' or 'no'."
            response = self.llm.generate(prompt, message_content)
            if response.lower() == "yes":
                self.english_message.add_item(message)

        self.message_from.for_each(self, filter_message)

    def stop(self):
        self.message_from.defor_each(self)


class ChineseMessageFilter(Agent):
    def __init__(self):
        super(ChineseMessageFilter, self).__init__("ChineseMessageFilter")
        self.message_from = get_stream("all_messages")
        self.chinese_message = create_stream("chinese_message")

        self.llm = get_model("text")

    def start(self):
        def filter_message(message):
            message_content = message["content"]
            prompt = "Is this message in Chinese? Say 'yes' or 'no'."
            response = self.llm.generate(prompt, message_content)
            if response.lower() == "yes":
                self.chinese_message.add_item(message)

        self.message_from.for_each(self, filter_message)

    def stop(self):
        self.message_from.defor_each(self)


class SpanishMessageFilter(Agent):
    def __init__(self):
        super(SpanishMessageFilter, self).__init__("SpanishMessageFilter")
        self.message_from = get_stream("all_messages")
        self.spanish_message = create_stream("spanish_message")

        self.llm = get_model("text")

    def start(self):
        def filter_message(message):
            message_content = message["content"]
            prompt = "Is this message in Spanish? Say 'yes' or 'no'."
            response = self.llm.generate(prompt, message_content)
            if response.lower() == "yes":
                self.spanish_message.add_item(message)

        self.message_from.for_each(self, filter_message)

    def stop(self):
        self.message_from.defor_each(self)
