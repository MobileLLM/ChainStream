目前的主要例子和实现情况：
- 软件sensor

  - 社交类

    - 聊天内容（短信/微信/QQ/Facebook/钉钉/邮件/等）：

      - 带类别的消息流：工作，家庭，广告，紧急程度（插入）【完成】
      - 女朋友在任何平台给我发的消息/英文的工作消息（过滤）【完成】
      - 根据消息类别转发到不同stream（分发+已有类别memory）【完成】
        - 改例子存在一个问题就是stream的名字不确定，故意做成开放范围的类别分发，所以需要通过memory维护已有哪些类别流。
      - 定时总结（buffer）【完成】
      - 多源头聚合【想不到例子】

    - 朋友圈（ins/twitter/抖音/小红书/朋友圈/QQ空间/youtube）：

      - 和message一样的插入、过滤、分发、记忆、暂存、聚合。【重复的就不写了】

      - 某个主播的视频动态【纯是一个爬虫接口问题，不需要写agent】

      - 超过100个赞的人工智能类的twitter【一个规则的filter，重复就不写了】

      - 某个博主推荐的商品的名称、介绍和亚马逊链接（链接是搜索得到的）【完成】

        - ```markdown
          Several steps:
          1. fetch all items from a platform's (twitter, instagram, youtube etc)
          2. distribute items to different streams based on author
          3. filter etch items containing an advertisement
          4. fetch advertisement products name, description etc. and push to advertisement product stream
          5. find products in Amazons and tag links to them
          ```

  - 资讯类

    - 新闻/短视频/arxiv paper/youtube更新/新歌发布/订阅号：过滤、推荐等

      - 每天帮我总结关于叙利亚的新闻等（过滤+聚合）【重复】

      - 关于LLM agent 的arxiv paper的中文摘要（转换）【重复】

      - 关于芯片板块的每小时的市场情绪报告（聚合）【重复】

      - 每天获得宾州和加州对美国大选的情绪对比【如下，没写】

        - ```markdown
          Several steps:
          1. Get all the news articles.
          2. Filter out the articles related to the election and push them to a new stream.
          3. Filter out the articles based on some criteria (state, party, sentiment analysis, keyword matching, etc.) and push them to a new stream.
          4. Summarize each stream's opinion every day and push it to a new stream.
          5. Listens to the stream from different sources and compares the opinions between them.
          ```

      - 每小时生成各大生鲜市场的价格对比【同上】

      - 和我收藏过的专辑风格类似的新歌（配置类memory）【本体重复，写了个更多余的】

  - App使用类

    - 今天刷的各个平台短视频时间统计【写起来还挺复杂的，完成】
    - 每天看过的资讯的话题时间统计【重复】
    - 每天的通讯类app使用时长统计【重复】
    - 订了什么外卖【重复】

- 硬件sensor【几乎全是改prompt的工作】

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