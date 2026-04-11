import os
from video_list import video_list


def split_video_frames(video_path, output_dir, split_gap=1):
    # use ffmpeg to split video into frames
    video_id = video_path.split("/")[-1].split(".")[0]
    output_video_dir = os.path.join(output_dir, video_id)
    if not os.path.exists(output_video_dir):
        os.makedirs(output_video_dir)
    cmd = f"ffmpeg -i {video_path} -vf fps=1/{split_gap} {output_video_dir}/%06d.jpg"
    os.system(cmd)


def preparing_video_dataset(raw_video_dir, output_dir, split_gap=1, target_video_list=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for video in video_list:
        video_id = video["video_name"]
        if target_video_list is not None and video_id.split(".")[0] not in target_video_list:
            continue
        video_path = os.path.join(raw_video_dir, f"{video_id}")
        if not os.path.exists(video_path):
            print(f"视频文件 {video_path} 不存在，跳过")
            continue

        # Split video frames
        split_video_frames(video_path, output_dir, split_gap=split_gap)


if __name__ == '__main__':
    preparing_video_dataset('pick_video',
                            'video_frame',
                            split_gap=1,
                            target_video_list=[
                                'okutama_2'
                               ]
                            )
