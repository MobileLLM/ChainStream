from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.memory import get_memory, create_memory
from chainstream.llm import get_model, make_prompt
from chainstream.context import TextBuffer


class DistributeMessageBySender(Agent):
    def __init__(self):
        super().__init__("distribute_message_by_sender")
        self.input_stream = get_stream("message_stream")

    def start(self):
        def distribute_message(message):
            sender = message["sender"]
            sender_stream = get_memory(f"user_agents/message/sender_{sender}")
            if sender_stream is None:
                sender_stream = create_memory(f"user_agents/message/sender_{sender}")
            sender_stream.add_item(message)

        self.input_stream.for_each(self, distribute_message)

    def stop(self):
        self.input_stream.unregister_all(self)


class DistributeMessageByTopic(Agent):
    def __init__(self):
        super().__init__("distribute_message_by_topic")
        self.input_stream = get_stream("message_stream")
        self.llm = get_model("text")
        self.topic_memory = create_memory("user_agents/message/topic_memory", type="seq")

    def start(self):
        def distribute_message(message):
            prompt = make_prompt("Choose a topic for this message or type 'new:<topic>' to create a new topic. "
                                 "Existing topics: ", self.topic_memory)
            response = self.llm.generate(prompt)
            if response.startswith("new:"):
                topic = response.split(":")[-1].strip()
                self.topic_memory.add_item(topic)
                topic_stream = get_memory(f"user_agents/message/topic_{topic}")
            else:
                topic_stream = get_memory(f"user_agents/message/topic_{response}")
            topic_stream.add_item(message)

        self.input_stream.for_each(self, distribute_message)

    def stop(self):
        self.input_stream.unregister_all(self)


class DistributeMessageByEmotion(Agent):
    def __init__(self):
        super().__init__("distribute_message_by_emotion")
        self.input_stream = get_stream("message_stream")
        self.llm = get_model("text")
        self.emotion_memory = create_memory("user_agents/message/emotion_memory", type="seq")

    def start(self):
        def distribute_message(message):
            prompt = make_prompt("Choose an emotion for this message: ", ["positive", "negative", "neutral", "other"])
            response = self.llm.generate(prompt)
            emotion = response.strip().lower()
            emotion_stream = get_memory(f"user_agents/message/emotion_{emotion}")
            emotion_stream.add_item(message)

        self.input_stream.for_each(self, distribute_message)

    def stop(self):
        self.input_stream.unregister_all(self)


class DistributeMessageByLanguage(Agent):
    def __init__(self):
        super().__init__("distribute_message_by_language")
        self.input_stream = get_stream("message_stream")
        self.llm = get_model("text")
        self.language_memory = create_memory("user_agents/message/language_memory", type="seq")

    def start(self):
        def distribute_message(message):
            prompt = make_prompt("Choose a language for this message: ", ["English", "Spanish", "Chinese", "French", "Other"])
            response = self.llm.generate(prompt)
            language = response.strip().lower()
            language_stream = get_memory(f"user_agents/message/language_{language}")
            language_stream.add_item(message)

        self.input_stream.for_each(self, distribute_message)

    def stop(self):
        self.input_stream.unregister_all(self)
