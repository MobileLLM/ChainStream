import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
from video_list import video_list


def split_video_frames(video_path, output_dir, split_gap=1):
    # use ffmpeg to split video into frames
    video_id = video_path.split("/")[-1].split(".")[0]
    output_video_dir = os.path.join(output_dir, video_id)
    if not os.path.exists(output_video_dir):
        os.makedirs(output_video_dir)
    cmd = f"ffmpeg -i {video_path} -vf fps=1/{split_gap} {output_video_dir}/%06d.jpg"
    os.system(cmd)


def preparing_video_dataset(raw_video_dir, output_dir, split_gap=1):
    for video in video_list:
        video_id = video["video_id"]
        if video_id != "03d4c383-b80e-4095-9328-c964f2803a26":
            continue
        video_description = video["video_description"]

        video_path = os.path.join(raw_video_dir, f"{video_id}")
        if not os.path.exists(video_path):
            print(f"视频文件 {video_path} 不存在，跳过")
            continue

        # Split video frames
        split_video_frames(video_path, output_dir, split_gap=split_gap)


# def split_video_frames(video_path, output_dir, split_gap=1):
#     # use ffmpeg to split video into frames
#     video_id = video_path.split("/")[-1].split(".")[0]
#     cmd = f"ffmpeg -i {video_path} -vf fps=1/{split_gap} {output_dir}/{video_id}/%06d.jpg"
#     os.system(cmd)
#
#
# def preparing_video_dataset(raw_video_dir, output_dir, split_gap=1):
#     for video in video_list[:1]:
#         video_id = video["video_id"]
#         video_description = video["video_description"]
#
#         video_path = os.path.join(raw_video_dir, f"{video_id}")
#         if not os.path.exists(video_path):
#             print(f"视频文件 {video_path} 不存在，跳过")
#             continue
#
#         # 创建输出目录
#         output_video_dir = os.path.join(output_dir, video_id)
#         os.makedirs(output_video_dir, exist_ok=True)
#
#         # 切割视频帧
#         split_video_frames(video_path, output_video_dir, split_gap=split_gap)


def download_video_from_preview(video_id, save_path):
    """
    need key and secret to access ego4d-data.org
    :param video_id:
    :param save_path:
    :return:
    """
    # 设置Chrome选项
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 初始化WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # 构建预览页面的URL
    preview_url = f"https://visualize.ego4d-data.org/{video_id}"
    driver.get(preview_url)

    try:
        # 等待视频元素加载完成
        wait = WebDriverWait(driver, 20)  # 最长等待时间20秒
        video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))

        if video_element:
            video_url = video_element.get_attribute('src')

            # 下载视频文件
            video_response = requests.get(video_url, stream=True)
            if video_response.status_code == 200:
                with open(save_path, 'wb') as file:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"视频已成功下载并保存到 {save_path}")
            else:
                print(f"无法下载视频，HTTP状态码: {video_response.status_code}")
        else:
            print("无法找到视频标签")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭浏览器
        driver.quit()


if __name__ == '__main__':
    preparing_video_dataset('./raw_video', './video_frame', split_gap=5)
