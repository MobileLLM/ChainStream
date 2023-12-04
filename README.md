# ChainStream

The development framework and runtime system for mobile agents.

## Install

Clone this repo, change directory to the repo folder, and install with pip:

```bash
pip install -e .
```

## Build an agent

Building an agent with ChainStream involves following steps.

1. Determine the data-source streams.
2. Define the transformations to transform the stream to the wanted format.
3. Listen to the stream and take actions when needed.

Example:

```python
import chainstream as cs

class PeopleRecognitionAgent(StreamAgent):
    def __init__(self):
        ...
        self._source1 = cs.get_stream('glass_camera_video_01')  # instance of Stream
        self._source2 = cs.get_stream('glass_microphone')
        self._llm = cs.get_llm()  # default LLM
        self.video_cache = cs.data.VideoCache(duration=10)
        self.audio_cache = cs.data.AudioCache(duration=10)
        self.talking_to_people = cs.create_stream('talking_to_people')

    def start(self):
        def handle_new_frame(frame):
            self.video_cache.save(frame)

        def handle_new_audio(audio):
            self.audio_cache.save(frame)
            prompt = cs.make_prompt([self.video_cache, self.audio_cache, 'is there a person talking to the user?'])
            response = self._llm.query(prompt)   # detect whether there is a talking people with LLM
            is_talking = cs.parse_llm_response(response, ['yes', 'no']) == 'yes'
            if is_talking:   # if detected, create a new event to the 'talking_to_people' stream
                self.talking_to_people.send_event({'video': self.video_cache.snapshot(), 'audio': self.audio_cache.snapshot()})

        def recognize_person(talking_event):
            video = talking_event['video']
            contacts_memory = cs.memory.known_people['face', 'name']
            prompt = cs.make_prompt([video.last_frame(), contacts_memory, 'who is the person in the image?'])
            face_name = cs.parse_llm_response(self._llm.query(prompt))
            cs.actions.notify_user(self, face_name)  # tell the user who is talking

        self._source1.register_listener(self, handle_new_frame)
        self._source2.register_listener(self, handle_new_audio)
        self.talking_to_people.register_listener(self, recognize_person)

    def pause(self):
        self._source1.pause_listener(self)
        self._source2.pause_listener(self)

    def destory(self):
        self._source1.remove_listener(self)
        self._source2.remove_listener(self)

```