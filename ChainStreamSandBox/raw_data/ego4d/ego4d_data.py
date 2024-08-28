from ChainStreamSandBox.raw_data.ego4d.video_list import video_list
import os
import PIL.Image as Image
import random

random.seed(42)


class Ego4DData:
    def __init__(self):
        self.video_list = video_list

        self.frame_path_base = os.path.join(os.path.dirname(__file__), "video_frame")

        self.video_frame_data = []

        self._check_path()

    def _check_path(self):
        if not os.path.exists(self.frame_path_base):
            raise ValueError("Frame path does not exist")

    def __len__(self):
        return len(self.video_list)

    def _load_video_frame(self, video_id):
        frame_path = os.path.join(self.frame_path_base, video_id)
        if not os.path.exists(frame_path):
            raise ValueError("Frame path does not exist for video id: {}".format(video_id))
        frame_list = os.listdir(frame_path)
        if len(frame_list) == 0:
            raise ValueError("No frame found for video id: {}".format(video_id))
        frame_list.sort()
        frame_path_list = [os.path.join(frame_path, frame) for frame in frame_list]
        frame_list = [Image.open(frame_path) for frame_path in frame_path_list]
        return frame_list

    def _load_frames(self, video_ids):
        frame_list = []
        for video_id in video_ids:
            frame_list.append(self._load_video_frame(video_id))
        return frame_list

    def load_for_action(self):
        video_ids = [
            '03d4c383-b80e-4095-9328-c964f2803a26',
            '8dfb9329-a70c-4a5a-85c2-39dae4caf3f0',
            '03d4c383-b80e-4095-9328-c964f2803a26'
        ]
        return self._load_frames(video_ids)

    def load_for_indoor_and_outdoor(self):
        video_ids = [
            '146d77cc-be02-48cc-8c95-afd7566edfae',
            '8dfb9329-a70c-4a5a-85c2-39dae4caf3f0',
            '03d4c383-b80e-4095-9328-c964f2803a26'
        ]
        return self._load_frames(video_ids)

    def load_for_person_detection(self):
        video_ids = [
            '9ffdb530-718d-4898-aeba-1f7832a4c13b',
            'b513c72d-8b77-4bee-96b6-b5f57977a3eb',
            '35384a66-1837-4f9f-ba43-0f72c63597f4'
        ]
        return self._load_frames(video_ids)

    def load_for_object_detection(self):
        video_ids = [
            '03d4c383-b80e-4095-9328-c964f2803a26',
            '9ffdb530-718d-4898-aeba-1f7832a4c13b',
            '1efb20de-7aca-4798-a7c2-0e4dc34fb687'
        ]
        return self._load_frames(video_ids)

    def load_for_traffic(self):
        video_ids = [
            '03d4c383-b80e-4095-9328-c964f2803a26'
        ]
        return self._load_frames(video_ids)

    def load_for_meeting(self):
        video_ids = [
            'b513c72d-8b77-4bee-96b6-b5f57977a3eb'
        ]
        return self._load_frames(video_ids)
