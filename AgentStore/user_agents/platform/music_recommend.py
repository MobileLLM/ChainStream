from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.memory import get_memory, create_memory
from chainstream.llm import get_model, make_prompt
from chainstream.context import TextBuffer
from chainstream.action import notify_user


class MusicRecommend(Agent):
    '''
    1.Several steps for record preference memory:
        1.1. Get new songs from user's favorites.
        1.2. Add style tag to user's preference memory.

    2.Several steps for music recommendation:
        2.1. Interface today's hot songs as a stream.
        2.2. Check whether a song has been recommended before. If no, push it to a new stream.
        2.3. Check whether to recommend this song to the user.
        2.4. [Select] Get feedback from user and update preference memory.

    we start from 2.3 to demonstrate how to get feedback from user.
    '''
    def __init__(self):
        super().__init__("MusicRecommend")
        self.new_songs = get_stream("new_songs")
        self.music_llm = get_model(['audio', 'text'])
        self.memory_llm = get_memory("text")
        self.preference_memory = get_memory("preference_memory")
        self.wait_feedback_buffer = TextBuffer()
        self.clock = get_stream("clock_every_hour")

    def start(self):
        def update_preference_memory():
            need_feedback_songs = self.wait_feedback_buffer.read()
            feedback = notify_user(self, "Do you like this song that was recommended to you before?" + need_feedback_songs['name'], feedback_type=bool)
            prompt = (f"User has given {feedback} evaluation to this previously recommended song. Please update memory "
                      f"accordingly. Answer in chainstream memory api format")
            response = self.memory_llm.generate(prompt)
            self.preference_memory.exec(response)
        self.clock.for_each(self, update_preference_memory)

        def recommend_songs(song):
            prompt = make_prompt("I prefer music like ", self.preference_memory, ".\nWill you recommend this song to "
                                                                                 "me? Answer yes or no. Here's the "
                                                                                 "song: ", song['audio'])
            response = self.music_llm.generate(prompt)
            if response == "yes":
                notify_user(self, "I recommend this song to you!" + song['audio'])
                self.wait_feedback_buffer.add(song)
        self.new_songs.for_each(self, recommend_songs)

    def stop(self):
        self.clock.unregister_all(self)
        self.new_songs.unregister_all(self)




