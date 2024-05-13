chinese_task_prompt_base = '''
向你介绍ChainStream，一个python编写的流式LLM Agent开发框架，其主要目的是编写LLM为主的处理流式的传感器数据并完成感知任务的Agent。传感器包括硬件传感器和软件传感器，硬件传感器包括常见的气温、气压、加速度计等常见传感器，而软件传感器则范围更广，比如app、网络api、截屏等都算软件传感器的范围。感知任务则主要是借助LLM的能力更好的理解物理世界的过程，不同于传统方法使用定制模型解决定制任务，ChainStream更注重借助LLM的通用能力去更好的理解物理世界，当然如果需要的话也可以使用各种小模型作为工具来帮助感知。

物理世界的传感器大多是长时间开启的，所以我们使用流式结构来组织数据。每个数据都在一个流中传递，比如IMU传感器每时每刻都在向流中推送当前数据。而每个流上都可以有监听着的函数，接收流中的数据、做处理并向新的流中推送新数据。

我们正在给ChainStream构造一些作为例子的任务，比如已有这些例子：
- 软件sensor
  - 社交类
    - 社交软件的聊天内容：
      - 为原始消息打上类别标签：工作，家庭，广告，紧急程度（插入）
      - 女朋友在任何平台给我发的消息（过滤+多数据源）
      - 英文的工作消息（双重过滤）
    - 社交平台：（朋友圈/ins/twitter/抖音/小红书/朋友圈/QQ空间/youtube/音乐）
      - 某个主播的视频动态（过滤）
      - 超过100个赞的人工智能类的twitter（多重过滤）
      - 某个博主推荐的商品的名称、介绍和亚马逊链接（链接要通过搜索得到）
  - 资讯类
    - 每天帮我总结关于叙利亚的新闻等（聚合）
    - 关于LLM agent 的每篇arxiv paper的中文摘要（转换）
    - 关于芯片板块的每小时的市场情绪报告（聚合）
    - 每天获得宾州和加州对美国大选的情绪对比（多流汇总）
    - 每小时生成各大生鲜市场的价格对比（多流汇总）
    - 和我收藏过的专辑风格类似的新歌（配置类memory）
  - App使用类（通过截屏等方法做屏幕分析）
    - 今天刷的各个平台短视频时间统计
    - 每天看过的资讯的话题时间统计
    - 每天的通讯类app使用时长统计
    - 收集我订过五次以上外卖商家的促销广告
- 硬件sensor
  - 视觉
    - 摄像头中有什么东西/有什么人/有谁
    - 人的动作/物体的颜色/物体的种类/人的表情和情绪
    - 物体的状态/门有没有关/会议室有没有人/货架是不是空了/水烧开了吗/猫粮吃完没有
    - 所处环境/位置/场所/场合
  - 听觉
    - 什么声音/风声/下雨/杯子打碎了/打雷/狗叫/汽车发动/敲门声/高跟鞋走路/有人唱歌/打呼噜
    - 谁在说话/对话的内容/语气/目的/对话场合
    - 根据声音判断位置/场合/场景
  - 传感器（简化一些）
    - 定位/环境/场景/场合/在家还是公司
    - 动作/速度/是否在运动
    - 光照/温度/湿度
    - 有传感器的物体状态：水位高低/门是否关着/冰箱温度

你能否再多补充一些例子，需要注意的是：例子尽量贴近生活，尽可能丰富。例子任务不要太复杂。请按照一定格式有序列举各个例子，并对每个例子给出解释，解释包含例子来源于哪些传感器数据、大概包含的处理步骤等等。
'''


english_task_prompt_base = '''
Introducing ChainStream, a Python-written streaming LLM Agent development framework. Its main purpose is to write agents primarily based on LLM to process streaming sensor data and accomplish perception tasks. Sensors include both hardware sensors and software sensors. Hardware sensors consist of common sensors such as temperature, pressure, and accelerometers, while software sensors have a broader range, including apps, network APIs, screenshots, etc. Perception tasks mainly leverage the capabilities of LLM to better understand processes in the physical world. Unlike traditional methods that use custom models to solve specific tasks, ChainStream focuses more on leveraging the general capabilities of LLM to better understand the physical world. Of course, if needed, various small models can also be used as tools to aid perception.

Most sensors in the physical world are continuously active, so we use a streaming structure to organize data. Each piece of data is passed in a stream, for example, an IMU sensor continuously pushes current data into the stream. And there can be functions listening on each stream, receiving data from the stream, processing it, and pushing new data into new streams.

We are currently constructing some example tasks for ChainStream, such as:
- Software sensor
  - Social category
    - Chat content from social software:
      - Categorize original messages: work, family, advertisement, urgency level (insertion)
      - Messages from my girlfriend across any platform (filtering + multiple data sources)
      - English work messages (double filtering)
    - Social platforms: (Friends' circle/ins/twitter/Douyin/Little Red Book/friends' circle/QQ space/youtube/music)
      - Videos of a certain anchor (filtering)
      - AI-related tweets with over 100 likes (multiple filtering)
      - Names, descriptions, and Amazon links of products recommended by a certain blogger (links obtained through search)
  - News category
    - Summarize daily news about Syria for me (aggregation)
    - Chinese abstracts of each arxiv paper about LLM agent (conversion)
    - Hourly market sentiment reports for the chip sector (aggregation)
    - Daily mood comparison between Pennsylvania and California for the US election (multi-stream summary)
    - Hourly comparison of prices in major fresh markets (multi-stream summary)
    - New songs similar in style to albums I've collected (configuration-based memory)
  - App usage category (screen analysis and other methods)
    - Time statistics of short videos from various platforms watched today
    - Time statistics of topics in news watched daily
    - Daily usage time statistics of communication apps
    - Collect promotional ads from takeaway merchants I've ordered from more than five times
- Hardware sensor
  - Vision
    - What's in the camera/who's there/who is present
    - Human actions/object colors/object types/facial expressions and emotions
    - Status of objects/whether the door is closed/whether there are people in the meeting room/whether the shelf is empty/whether the water is boiling/whether the cat food is finished
    - Environment/location/place/occasion
  - Audition
    - What sounds/wind/rain/glass breaking/thunder/dog barking/car starting/knocking on the door/high heels walking/someone singing/snoring
    - Who is speaking/content of the conversation/tone/purpose/occasion of the conversation
    - Determine location/occasion/scene based on sound
  - Sensors (simplified)
    - Position/environment/scene/occasion/at home or at work
    - Motion/speed/whether in motion
    - Illuminance/temperature/humidity
    - Status of objects with sensors: water level, whether the door is closed, refrigerator temperature

Could you please provide a few more examples? The examples should be close to daily life and as diverse as possible. The tasks in the examples should not be too complex. Please list various examples in an ordered format, and provide an explanation for each example, including which sensor data the example originates from and the approximate processing steps involved.
'''