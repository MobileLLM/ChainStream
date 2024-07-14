from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.memory import get_memory, create_memory
from chainstream.llm import get_model


class TagMessage(Agent):
    """
    Agent to tag messages with several different tag types.

    """

    def __init__(self):
        super().__init__("tag_message_agent")
        self.message_from = get_stream("all_messages")
        self.message_to = create_stream("all_messages_tagged")
        self.llm = get_model("text")

    def start(self):
        def tag_message(message):
            message_content = message["content"]
            base_tag_prompt = ("Give you a message: %s . What tag would you like to add to this message? Choose from "
                               "the following: ") % message_content
            topic_tags = ['politics', 'finance', 'entertainment', 'health', 'technology', 'travel', 'food', 'education', 'other']
            emotion_tags = ['positive', 'negative', 'neutral', 'other']
            domain_tags = ['home', 'work', 'family', 'friends', 'other']
            prompt_is_advertised = "Is this a tag advertised? Type 'yes' or 'no'."

            prompt_topic = base_tag_prompt + ", ".join(topic_tags)
            prompt_emotion = base_tag_prompt + ", ".join(emotion_tags)
            prompt_domain = base_tag_prompt + ", ".join(domain_tags)

            topic_tag = self.llm.query(prompt_topic)
            emotion_tag = self.llm.query(prompt_emotion)
            domain_tag = self.llm.query(prompt_domain)

            advertised_tag = self.llm.query(prompt_is_advertised)

            new_message = message.copy()
            new_message["tags"] = {"topic": topic_tag, "emotion": emotion_tag, "domain": domain_tag, "advertised": advertised_tag}
            self.message_to.send(new_message)

        self.message_from.for_each(self, tag_message)

    def stop(self):
        self.message_to.unregister_all(self)


class TopicTagger(Agent):
    """
    Agent to tag messages with topic tags.
    """

    def __init__(self):
        super().__init__("topic_tagger")
        self.message_from = get_stream("all_messages")
        self.message_to = create_stream("topic_tagged_messages")
        self.llm = get_model("text")

    def start(self):
        def tag_topic(message):
            message_content = message["content"]
            base_tag_prompt = ("Give you a message: %s . What topic tag would you like to add to this message? Choose "
                               "from the following: ") % message_content
            topic_tags = ['politics', 'finance', 'entertainment', 'health', 'technology', 'travel', 'food', 'education',
                          'other']

            prompt_topic = base_tag_prompt + ", ".join(topic_tags)

            topic_tag = self.llm.query(prompt_topic)

            new_message = message.copy()
            new_message["tags"] = {"topic": topic_tag}
            self.message_to.send(new_message)

        self.message_from.for_each(self, tag_topic)

    def stop(self):
        self.message_to.unregister_all(self)


class EmotionTagger(Agent):
    """
    Agent to tag messages with emotion tags.
    """

    def __init__(self):
        super().__init__("emotion_tagger")
        self.message_from = get_stream("all_messages")
        self.message_to = create_stream("emotion_tagged_messages")
        self.llm = get_model("text")

    def start(self):
        def tag_emotion(message):
            message_content = message["content"]
            base_tag_prompt = (
                                  "Give you a message: %s . What emotion tag would you like to add to this message? Choose from "
                                  "the following: ") % message_content
            emotion_tags = ['positive', 'negative', 'neutral', 'other']

            prompt_emotion = base_tag_prompt + ", ".join(emotion_tags)

            emotion_tag = self.llm.query(prompt_emotion)

            new_message = message.copy()
            new_message["tags"] = {"emotion": emotion_tag}
            self.message_to.send(new_message)

        self.message_from.for_each(self, tag_emotion)

    def stop(self):
        self.message_to.unregister_all(self)


class DomainTagger(Agent):
    """
    Agent to tag messages with domain tags.
    """

    def __init__(self):
        super().__init__("domain_tagger")
        self.message_from = get_stream("all_messages")
        self.message_to = create_stream("domain_tagged_messages")
        self.llm = get_model("text")

    def start(self):
        def tag_domain(message):
            message_content = message["content"]
            base_tag_prompt = (
                                  "Give you a message: %s . What domain tag would you like to add to this message? Choose from "
                                  "the following: ") % message_content
            domain_tags = ['home', 'work', 'family', 'friends', 'other']

            prompt_domain = base_tag_prompt + ", ".join(domain_tags)

            domain_tag = self.llm.query(prompt_domain)

            new_message = message.copy()
            new_message["tags"] = {"domain": domain_tag}
            self.message_to.send(new_message)

        self.message_from.for_each(self, tag_domain)

    def stop(self):
        self.message_to.unregister_all(self)
