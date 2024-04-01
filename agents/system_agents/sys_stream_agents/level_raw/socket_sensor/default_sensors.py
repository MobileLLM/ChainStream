import chainstream as cs
import threading
import time
from datetime import datetime


class DefaultSensors(cs.agent.Agent):
    is_agent = True
    def __init__(self, agent_id='pc_sensors', video_fps=1, audio_duration=1):
        super().__init__(agent_id)
        self.video_fps = video_fps
        self.audio_duration = audio_duration
        self.front_camera_video = cs.stream.create_stream('front_camera_video')
        self.front_camera_thread = None
        self.microphone_audio = cs.stream.create_stream('microphone_audio')
        self.microphone_thread = None
        self.enabled = True
    
    def start(self):
        self.front_camera_thread = threading.Thread(target=self.capture_images)
        self.front_camera_thread.start()
        self.microphone_thread = threading.Thread(target=self.capture_audio)
        self.microphone_thread.start()

    def capture_images(self):
        import cv2
        cap = cv2.VideoCapture(0)
        sleep_duration = int(1 / self.video_fps)
        while self.enabled:
            time.sleep(sleep_duration)
            ret, frame = cap.read()
            self.front_camera_video.send_item({'timestamp': datetime.now(), 'frame': frame})
        cap.release()

    def capture_audio(self):
        # TODO implement this and other sensors
        pass
    
    def stop(self):
        self.enabled = False


if __name__ == '__main__':
    default_sensors_agent = DefaultSensors()
    default_sensors_agent.start()
    while True:
        cmd = input('> ')
        if cmd == 'q':
            default_sensors_agent.stop()
            break

