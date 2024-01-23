import chainstream as cs
import threading
import time
from datetime import datetime
import socketio


class SocketSensors(cs.agent.Agent):
    def __init__(self, agent_id='default_sensors', video_fps=1, audio_duration=1, ip='192.168.43.1', port=6666):
        super().__init__(agent_id)
        self.video_fps = video_fps
        self.audio_duration = audio_duration
        self.front_camera_video = cs.stream.create_stream('socket_front_camera_video')
        self.front_camera_thread = None
        self.microphone_audio = cs.stream.create_stream('socket_microphone_audio')
        self.microphone_thread = None
        self.enabled = True

        self.sio = socketio.Client()
        self.ip = ip
        self.port = port

    def start(self):
        self.front_camera_thread = threading.Thread(target=self.capture_images)
        self.front_camera_thread.start()
        self.microphone_thread = threading.Thread(target=self.capture_audio)
        self.microphone_thread.start()

    def capture_images(self):
        try:
            self.sio.connect("http://{}:{}".format(self.ip, self.port))
            self.sio.emit('video,1')

            @self.sio.event
            def server_response(data):
                self.front_camera_video.send_item({'timestamp': datetime.now(), 'frame': data})
                self.logger.info("Received image from server")

            self.sio.wait()
        except Exception as e:
            self.logger.error(f"Error in capture_images: {e}")

    def capture_audio(self):
        # TODO implement this and other sensors
        pass

    def stop(self):
        self.enabled = False
        self.sio.disconnect()


if __name__ == '__main__':
    default_sensors_agent = SocketSensors()
    default_sensors_agent.start()
    while True:
        cmd = input('> ')
        if cmd == 'q':
            default_sensors_agent.stop()
            break

