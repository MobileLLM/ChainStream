## 数据源：
1. image：
    - 第一人称视角图像（未完成）
    - 第三人称视角图像（未完成）
      - 室内
      - 室外
    - 截屏（未完成）
      - PC端
      - 手机端
2. audio（以文本代替，假装是音频）
    - daily_dialog数据集
3. text 
   - chat message
       - smsCorpus数据集 
   - email history
       - enron_email数据集 
   - daily arxiv paper
       - 日常arxiv论文
   - stock
       - stock股票数据集
   - news
       - 新闻数据集
4. IMU（未完成）
   - 加速度计
   - 陀螺仪
   - 重力
   - 线性加速度计
   - 旋转向量
   - 气压
   - 气温
   - 光照
   - 湿度
   - GPS

## 收集的数据集：
image:
1. 第一人称视角图像: Ego4D选一点视频抽帧

audios:
- daily_dialog 数据集

email:
- enron_mail 数据集

sms:
- smsCorpus 数据集

twitter：
- https://huggingface.co/datasets/strombergnlp/broad_twitter_corpus

pc screenshot:
- https://github.com/waltteri/desktop-ui-dataset

web ui：
- https://uimodeling.github.io/