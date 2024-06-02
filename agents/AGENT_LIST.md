### 目前已经实现的Agent：

System Agents:

- Sensor Interface Agents:
  - PC_CAMERA_AGENT: PC摄像头视频流Agent。
  - MOBILE_CAMERA_AGENT: Android设备摄像头视频流Agent。
  - MOBILE_AUDIO_AGENT: Android设备麦克风音频流Agent。
  - MOBILE_ACCELEROMETER_AGENT: Android设备加速度计Agent。
  - MOBILE_AIR_PRESSURE_AGENT: Android设备气压Agent。
  - MOBILE_AMBIENT_TEMPERATURE_AGENT: Android设备环境温度Agent。
  - MOBILE_DEVICE_EVENT_AGENT: Android设备事件Agent。
  - MOBILE_DEVICE_STATE_AGENT: Android设备状态Agent。
  - MOBILE_GEOLOCATION_AGENT: Android设备地理位置Agent。
  - MOBILE_GRAVITY_AGENT: Android设备重力Agent。
  - MOBILE_GYROSCOPE_AGENT: Android设备陀螺仪Agent。
  - MOBILE_LIGHT_AGENT: Android设备光线Agent。
  - MOBILE_LINEAR_ACCELERATION_AGENT: Android设备线性加速度Agent。
  - MOBILE_RELATIVE_HUMIDITY_AGENT: Android设备相对湿度Agent。
  - MOBILE_ROTATION_VECTOR_AGENT: Android设备旋转向量Agent。
  - MOBILE_STEP_COUNTER_AGENT: Android设备步数Agent。

- Tool Agents:
  - CLOCK_AGENT: 系统时钟Agent。
  - MOBILE_NOTIFICATION_AGENT: 向Android设备发送通知Agent。
  - ACTION_RECOGNITION_AGENT: 动作识别Agent。
  - AUDIO_TRANSCRIPTION_AGENT: 音频转文字Agent。
  - EMOTION_RECOGNITION_AGENT: 情绪识别Agent。
  - FACE_DETECTION_AGENT: 人脸检测Agent。
  - LANGUAGE_RECOGNITION_AGENT: 语言识别Agent。
  - GESTURE_RECOGNITION_AGENT: 手势识别Agent。
  - GOOGLE_SEARCH_AGENT: Google搜索Agent。
  - IMAGE_CAPTIONING_AGENT: 图像字幕Agent。
  - IMAGE_DETECTION_AGENT: 图像检测Agent。
  - IMAGE_GENERATION_AGENT: 图像生成Agent。
  - IMAGE_SEGMENTATION_AGENT: 图像分割Agent。
  - OPTICAL_CHARACTER_RECOGNITION_AGENT: 光学字符识别Agent。
  - VIDEO_GENERATION_AGENT: 视频生成Agent。
  - VIDEO_TRACKING_AGENT: 视频跟踪Agent。

- Admin Agents:
  - NL2DSL_AGENT: 自然语言到DSL转换Agent。

User Agents:
- Daily Life Agents:
  - APP:
    - APP_USAGE_AGENT: 应用使用量Agent。
  - Wearable Glass:
    - RECOGNIZE_PEOPLE_AGENT: 识别见到的人。
    - RECOGNIZE_TOYS_AGENT: 识别看到的玩具。
  - Assistants:
    - WEATHER_AGENT: 根据地理位置查询天气Agent。
    - CLOTHING_RECOMMENDATION_AGENT: 根据日程和天气的服装推荐Agent。

- News Agents:
  - Arxiv:
    - ARXIV_FILTER_AGENT: 筛选arXiv论文结构部分对Agent。
    - ARXIV_TAG_AGENT: 对arXiv论文进行标签分类Agent。
    - ARXIV_DAILY_RECOMMENDATION_AGENT: 每日arXiv推荐Agent。
  - Stock News:
    - FINANCE_NEWS_AGENT: 财经新闻Agent。

- Message Agents:
  - Email:
    - DISTRIBUTE_EMAIL_AGENT: 分发邮件Agent。
    - FILTER_EMAIL_AGENT: 过滤邮件Agent。
    - SUMMARIZE_EMAIL_AGENT: 摘要邮件Agent。
    - TAG_EMAIL_AGENT: 标记邮件Agent。
  - SMS:
    - DISTRIBUTE_SMS_AGENT: 分发短信Agent。
    - FILTER_SMS_AGENT: 过滤短信Agent。
    - SUMMARIZE_SMS_AGENT: 摘要短信Agent。
    - TAG_SMS_AGENT: 标记短信Agent。

- Social Media Agents:
  - Music:
    - MUSIC_RECOMMENDATION_AGENT: 根据兴趣和历史推荐音乐Agent。

### 待实现的Agent：

- System Agents:
  - Tool Agents:
    - PYTHON_COMMAND_AGENT: 执行Python命令Agent。
    - SHELL_COMMAND_AGENT: 执行Shell命令Agent。
  - Admin Agents:
    - STREAM_SELECT_AGENT: 选择Agent。
    - MEMORY_AGENT: 记忆管理Agent。
    - SYS_LOG_AGENT: 系统日志Agent。
    - SYS_MONITOR_AGENT: 系统监控Agent。
    - STREAM_MONITOR_AGENT: 流量监控Agent。
    - AGENT_MANAGER_AGENT: 管理Agent。
    - RESOURCES_OPTIMIZATION_AGENT: 资源优化Agent。
- User Agents:
  - Personal Agents:
    - DAILY_RECORD_AGENT: 记录日常生活Agent。
    - DIET_PLAN_AGENT: 制定饮食计划Agent。
    - HEALTH_MONITOR_AGENT: 健康监测Agent。
    - SCHEDULE_AGENT: 日程管理Agent。
  - Smart Home Agents:
    - PET_MONITOR_AGENT: 宠物监控Agent。
    - HOME_SECURITY_AGENT: 家庭安全Agent。
    - CLEANING_ROBOT_AGENT: 扫地机器人Agent。
    - KITCHEN_ASSISTANT_AGENT: 厨房助手Agent。
  - Smart Office Agents:
    - WORK_RECORD_AGENT: 记录工作Agent。
    - CONFERENCE_ROOM_AGENT: 会议室Agent。