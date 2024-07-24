from ChainStreamSandBox.raw_data.three_person_video.sphar import video_list
import os
import PIL.Image as Image

class SpharData:
    def __init__(self):
        self.video_list = video_list
        self.frame_path_base = r"C:\Users\86137\Desktop\chainstream-new\ChainStream\ChainStreamSandBox\raw_data\three_person_video\sphar\video_frame"

        self.video_frame_data = []

        self._check_path()

    def _check_path(self):
        if not os.path.exists(self.frame_path_base):
            raise Exception("Frame path does not exist")

    def __len__(self):
        return len(self.video_list)

    def _load_video_frame(self, video_name):
        video_frame_path = os.path.join(self.frame_path_base, video_name)
        if not os.path.exists(video_frame_path):
            raise Exception("Frame path does not exist")

        frame_list = os.listdir(video_frame_path)
        if len(frame_list) == 0:
            raise Exception("Frame list is empty")

        frame_list.sort()

        frame_data = []
        for frame_name in frame_list:
            frame_path = os.path.join(video_frame_path, frame_name)
            frame = Image.open(frame_path)
            frame_data.append(frame)

        return frame_data

    def _load_frames(self, video_names):
        frame_data = []
        for video_name in video_names:
            frame_data.append(self._load_video_frame(video_name))

        return frame_data

    def load_for_traffic(self):
        video_ids = [
            'livevid_panic0',
            'uccrime_RoadAccidents067_x264'
        ]
        return self._load_frames(video_ids)

    def load_for_violence(self):
        video_ids = [
            'bitint_box_0010',
            'uccrime_Shooting018_x264'
        ]
        return self._load_frames(video_ids)

    def load_for_person_detection(self):
        video_ids = [
            'casia_angleview_p01_crouch_a2',
            'okutama_2'
        ]
        return self._load_frames(video_ids)

if __name__ == '__main__':
    data = SpharData()
    print(data.load_for_traffic())
