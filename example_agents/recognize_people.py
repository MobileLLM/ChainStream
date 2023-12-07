import chainstream as cs
from chainstream.agent import Agent


class PeopleRecognitionAgent(Agent):
    def __init__(self):
        self._source1 = cs.get_stream('glass_camera_video_01')  # instance of Stream
        self._source2 = cs.get_stream('glass_microphone')
        self.known_people = cs.memory.fetch('known_people')['face', 'name']
        self._llm = cs.llm.get_llm('ChatGPT')  # default LLM
        self.video_buffer = cs.context.VideoBuffer(duration=10)
        self.audio_buffer = cs.context.AudioBuffer(duration=10)
        self.talking_to_people = cs.create_stream('talking_to_people')

    def start(self):
        def handle_new_frame(frame):
            self.video_buffer.save(frame)

        def handle_new_audio(audio):
            self.audio_buffer.save(audio)
            prompt = cs.llm.make_prompt([self.video_buffer, self.audio_buffer, 'is there a person talking to the user?'])
            response = self._llm.query(prompt)   # detect whether there is a talking people with LLM
            is_talking = cs.llm.parse_response(response, ['yes', 'no']) == 'yes'
            if is_talking:   # if detected, create a new event to the 'talking_to_people' stream
                self.talking_to_people.add_item({'video': self.video_buffer.snapshot(), 'audio': self.audio_buffer.snapshot()})

        def recognize_person(talking_event):
            video = talking_event['video']
            prompt = cs.llm.make_prompt([self.known_people, video.last_frame(), 'who is the person in the image?'])
            face_name = cs.llm.parse_response(self._llm.query(prompt))
            cs.action.notify_user(self, face_name)  # tell the user who is talking

        self._source1.register_listener(self, handle_new_frame)
        self._source2.register_listener(self, handle_new_audio)
        self.talking_to_people.register_listener(self, recognize_person)

    def pause(self):
        self._source1.pause_listener(self)
        self._source2.pause_listener(self)

    def stop(self):
        self._source1.remove_listener(self)
        self._source2.remove_listener(self)