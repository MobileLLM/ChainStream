# All tasks for ChainStreamSandBox

两大API：
- for_each (Function)：等价于当前的register_listener
- batch (by_time, by_count, by_key, by_func)：分窗API

典型的操作：

- item转换：
  - 字段转化（增加、删除、修改）   定时、转发、buffer
    - 
  - LLM转化（分词、去停用词、翻译等）todo
  - 过滤：字段筛选、复杂条件筛选（数值计算、多文本匹配等）、LLM判断 ok
  - item转向batch：计数、计时、定时、关键词、复杂条件（数值计算，多类型匹配等）计数ok,其它todo
- batch转换：
  - 分组：字段分组、复杂条件分组、LLM分组 ok
  - 聚合：指定字段聚合、复杂聚合（求和、求并等），LLM聚合（摘要、总结等）ok
  - 批转换：反转、排序等 ok
  - batch转向item：聚合、**分组转发**等 
- 多流输入输出：todo
  - 分发：单输入发送至多个流，类似于分组+转发
  - 汇总：多出入汇总，需借助buffer，类似于多数据源+聚合，可以考虑多类型数据匹配（如凑够一个红球和两个蓝球等）
- 当作触发器：todo
  - 定时触发：借助系统时钟流实现定时触发，如每天早上8点发送报告、每周五下午12点发送报告等
  - 事件触发：构造一个事件流，流中的内容代表事件发生，触发后续监听函数中的某个动作（如更新缓存、更新数据库等）
    
  


## Task with dataset (> 100 examples)
Old Task Lists:
- email dataset:
  1. emo classification: classify the emotion of an email message (positive, negative, neutral)【改成“每个月从工作email中总结我的情绪”】ok
  2. date extraction: extract the date of an email message 【分析邮件的时间分布，并将高峰时段的邮件发送者告诉我】
  3. receiver extraction: extract the receiver of an email message 【总结近一个月每个receiver的邮件，主题是跟工作有关的】ok
  4. sender extraction: extract the sender of an email message 【改成“总结每个sender的邮件历史，并且过滤掉广告”】ok
  5. subject judgment: Judge the topic of an email message 【改成“”】
  6. summarize content:generate a summary of an email message 【改成“每周生成跟LLM Agent内容有关的摘要报告”】
  7. auto reply: generate an auto reply for an email message 【对于不是广告的邮件，自动回复已收到，并筛选出发送人】ok
- news dataset:
  1. authors extraction: extract the authors of a news article【改成“按作者生成每月新闻贡献报告”】
  2. description judgment: judge the topics of a news article 【""】
  3. category classification: classify the category of a news article【对近一个月的新闻，按主题分类，统计出每个主题的数量】
  4. date extraction: extract the date of a news article 【"帮我从所有娱乐类新闻中找出其中的主角"】ok
  5. link extraction: extract the links of a news article【改成提取新闻文章中的所有链接，并分析哪个网站频率较高】ok
  6. title extraction: extract the title of a news article【对新闻的主题进行总结，并在每天下午5点告诉我】
  7. people extraction: extract the people mentioned in a news article【从时政新闻中筛选出跟人物有关的对话，并总结其观点】ok
  8. place extraction: extract the places mentioned in a news article【筛选加利福尼亚洲发生的新闻，并进行新闻的分类】ok
- message dataset:
  1. content judgment: judge the content of a message【
  2. emotion classification: classify the emotion of a message【llm划分当前的聊天topic，划分完之后，根据topic进行分类】
  3. language identification: identify the language of a message
  4. summarize content:generate a summary of a message
  5. time extraction: extract the time of a message
- stock dataset:
  1. information presentation: present the information of stocks【从每天的股市信息中关注我买入的股票情况，评价其涨跌幅】ok
  2. purchase recommendation: recommend the purchase of stocks【根据股市的涨跌，在工作日早上八点推荐买入】
  3. sell recommendation: recommend the selling of stocks【根据股市的涨跌，在每日收盘后推荐卖出】
  4. type recommendation: recommend the type of stocks that can be bought[总结感兴趣的板块的整体情况]
- dialogue dataset:
  1. information presentation: present the information of daily dialogues
  2. emotion classification: classify the emotion of people in a daily dialogue
  3. identity identification: identify the identity of people in a daily dialogue
  4. place extraction: extract the places where a daily dialogue takes place【根据对话判断出场景，并且
  5. time extraction: extract the time of a daily dialogue
  6. topic summary: summary the topic of a daily dialogue
- arxiv dataset:
  1. abstract extraction: extract the abstract of an arxiv paper【对近一个月有关LLM的arxiv文章进行摘要提取】ok
  2. algorithm identification: identify the algorithm used in an arxiv paper
  3. approach identification: identify the approach used in an arxiv paper【分析近来在cs领域上研究的论文，找出其使用的研究方法】ok
  4. authors identification: identify the authors of an arxiv paper【对Kaiming He的论文进行筛选，并总结其核心观点】ok
  5. comments extraction: extract the comments of an arxiv paper【根据citation对arxiv文章关注量进行排序，给我推荐前5高引的文章】
  6. date extraction: extract the date of an arxiv paper
  7. implementation identification: identify the implementation used in an arxiv paper
  8. journal reference identification: identify the journal reference id of an arxiv paper
  9. problems extraction: extract the problems to solve of an arxiv paper
  10. stage identification: identify the process stage of an arxiv paper
  11. topic extraction: extract the topic of an arxiv paper
  12. website identification: identify the publication website of the arxiv paper
- twitter dataset:
  - airline twitter
  1. airline extraction: extract  the airline information from a twitter message[关于点赞超过100的关于Agent的推特进行筛选发给我]
  2. location extraction: extract the location information from a twitter message
  3. tweet sentiment analysis: analyze the sentiment of a tweet
  4. negative reason analysis: analyze the negative reason behind a tweet
  5. retweet collection:  collect the retweets of a tweet
  6. tweet text presentation: present the text of a tweet
  7. tweet time extraction: extract the time of a tweet
  8. tweet timezone extraction: extract the timezone of a tweet
  9. tweet account extraction: extract the account information of a tweet
- GPS dataset:
  1. GPS capital extraction: extract the capital of a GPS message【根据我的经纬度判断我在哪个国家】ok
  2. GPS continent extraction: extract the continent of a GPS message【我在某城市，告诉我经纬度是多少】(重复？)
  3. GPS country extraction: extract the country of a GPS message
  4. GPS latitude extraction: extract the latitude of a GPS message
  5. GPS longitude extraction: extract the longitude of a GPS message
  6. landmark location identification: identify  the location of a landmark【根据我的街道地址告诉我附近有哪些旅馆】ok
  7. landmark name extraction: extract the name of a landmark【根据我的学校告诉我附近街道的名字】ok
  8. landmark type extraction: extract the type of a landmark【根据我的地址告诉我处在哪个城市】(重复)
  9. landmark time evaluation: evaluate the time of a landmark
  10. landmark neighborhood investigation:investigate the neighborhood of a landmark
  11. landmark floors count: count the floors of a landmark
  12. building electricity count: count the electricity usage of a building
  13. building gas count: count the natural gas usage of a building
  14. building GHGEmissions count: count the GHG emissions of a building
- activity dataset
  1. activity over 5km: remind the activity over 5km of a person【根据IMU传感器判断我的动作？】
  2. activity over 30mins: remind the activity over 30mins of a person
  3. calories most selection: remind the most burned_calories of a person in an activity
  4. steps over 5000: remind the steps over 5000 of a person
- weather dataset
  1. humidity detection: detect the humidity of the weather【根据当前的温度帮我推荐穿衣的搭配】ok
  2. precipitation detection: detect the precipitation of the weather【若当前相对湿度高于70%，提醒我注意湿滑】ok
  3. temperature detection: detect the temperature of the weather【根据当前的降雨量告诉我是否需要穿雨靴】ok
  4. wind speed detection: detect the wind speed of the weather【根据现在的风速判断我阳台的衣服是否需要收下】ok
  5. weather location detection: present the weather location【当前温度高于28度，相对湿度高于60%，提醒我开空调】
  6. weather time detection: present the weather time
- wifi dataset
  1. wifi channel detection: detect the wifi channel【根据wifi的mac地址/vendor/SSID。。。
  2. wifi mac address detection: detect the wifi mac address
  3. wifi signal strength display:display the wifi signal strength
  4. wifi SSID detection: detect the wifi SSID
  5. wifi vendor detection: detect the wifi vendor
- health dataset
  1. activity level rating: rate the activity level of a person【当我的高压大于140mmHg，低压小于90mmHg时，提醒吃点药】ok
  2. blood sugar measurement: measure the blood sugar of a person【当我的血糖值大于8.4mmol/L时，提醒我及时就医】ok
  3. BMI category classification: classify the BMI category of a person【当我的BMI诊断为肥胖时，每天定时提醒我锻炼减肥】ok
  4. body temperature measurement: measure the body temperature of a person【当我的工作心率高于100次/分时，提醒我注意休息】ok
  5. daily steps calculation: calculate the daily steps of a person【统计公司所有程序员的年龄和睡眠时间，给出合理建议】ok
  6. diastolic blood pressure measurement: measure the diastolic blood pressure of a person【当我今天的步数小于3000，提醒我多走几步】
  7. heart rate measurement: measure the heart rate of a person【我将我的体检表交给你，给出身体健康状况评级】
  8. sleep disorder judgment: judge whether a person has sleep disorder
  9. sleep duration measurement: measure the sleep duration of a person
  10. sleep quality measurement: measure the real sleep time of a person
  11. stress level rating: rate the stress level of a person
  12. systolic blood pressure measurement: measure the systolic blood pressure of a person
  13. current emotion judgement: judge the current emotion of a person according to the health data
  14. current occupation estimation: estimate the current occupation of a person according to the health data
  15. health risk evaluation: evaluate the health risk of a person according to the health data


New Task List(Done):
- email dataset:
  1. 每个月从工作email中总结我的情绪
  2. 总结近一个月每个receiver的邮件，主题是跟工作有关的
  3. 总结每个sender的邮件历史，并且过滤掉广告
  4. 对于不是广告的邮件，自动回复已收到，并筛选出发送人
- news dataset:
  1. 帮我从所有娱乐类新闻中找出其中的主角
  2. 提取新闻文章中的所有链接，并分析哪个网站频率较高
  3. 从时政新闻中筛选出跟人物有关的对话，并总结其观点
  4. 筛选加利福尼亚洲发生的新闻，并进行新闻的分类
- arxiv dataset:
  1. 对近一个月有关LLM的arxiv文章进行摘要提取
  2. 分析近来在cs领域上研究的论文，找出其使用的研究方法
  3. 对Kaiming He的论文进行筛选，并总结其核心观点
- stock dataset:
  1. 总结我关注的股票每天的涨跌幅
- sensor dataset:
  - GPS dataset
    1. 根据我的经纬度判断我在哪个国家
    2. 根据我的街道地址告诉我附近有哪些旅馆
    3. 根据我的学校告诉我附近街道的名字
  - weather dataset:
    1. 根据当前的温度帮我推荐穿衣的搭配
    2. 若当前相对湿度较高，提醒步行的我注意湿滑
    3. 根据当前的降雨量告诉我是否需要穿雨靴
    4. 根据现在的风速判断我阳台的衣服是否需要收下
  - health dataset:
    1. 当我的高压大于140mmHg，低压大于90mmHg时，提醒我吃点药
    2. 当我的血糖值大于8.4mmol/L时，提醒我及时就医
    3. 当我的BMI诊断为肥胖时，每天定时提醒我锻炼减肥
    4. 当我工作时的心率高于100次/分钟时，提醒我注意休息
    5. 统计公司所有程序员的年龄和睡眠时间，并逐一给出合理建议
- ego4D dataset:
  1. 简单检测我此刻在做什么
  2. 如果我在厨房，请帮我检测是否会有不安全用火引起的风险
  3. 当我在会议室时，自动记录会议的呈现的内容
- three person dataset:
  1. 判断此刻路面上是否有建筑物倒塌或车祸
  2. 从城镇监控摄像头中判断是否有暴力事件发生
  3. 从秘密基地摄像头判断是否有人闯入
- desktop-ui dataset:
  1. 办公时帮我记录我所使用的软件是什么
- github
  1. 给我推荐stars数量最高的10个项目,并告诉我有多少watchers
  2. 推荐最近一年以来commit数量最多的10个项目
  3. 筛选出带license的项目，并告诉我fork数量前5的项目
  4. 筛选出pull-request数量最多的5个项目，告诉我涉及到哪些语言编写
- multi-stream
  1. 若stock暴跌，message提醒我
  2. 从科创板块news中sum各创业公司CEO的观点保存到本地
  ~~3. 如果下雨，message至朋友不出去吃饭了~~
  4. gps检测到我在办公室,且ui检测我在摸鱼超过0.5h，message提醒我及时工作
  ~~5. one-person检测到我在运动，自动监测我的心率并给出建议~~
  6. 当我一个人开车上班时，播报个人新闻，当我一个人开车下班时，播放音乐
  ~~7. github若有PR,email自动回复~~
  8. dialogue中聊到游玩计划时，提前帮我看定位和天气（有点难了）
  ~~9. 检测到我的血压异常，自动帮我找附近的医院~~
  10. 检测到我在家，帮我自动回复不是ads的email
  11. 当我不在家，我的猫没猫粮时（监测其它），自动短信提醒我
  12. 当我超过一段时间没浇水，提醒我浇水
  13. 检查无人时厨房煤气灶是否开着，若是，发出报警
  14. 如果用户在工作时并且即将刮风下雨，则自动关闭门窗
  15. 如果检测到驾驶员疲劳程度在50-80分之间，则播放摇滚音乐提醒其保持清醒。如果高于80分则发出警告。
  ~~16. 如果小孩在商场离开家属超过10分钟，通知工作人员~~
  17. 如果我在家中看书，若天色渐暗，帮我自动调节室内灯光（可以有data）
  18. 关掉不用房间的灯光（有data，可以假设每个房间都有监控）
  19. 如果候诊人数超过1人，且诊室医生不在超过20分钟，则自动短信提醒医生
  20. 在营业时间段，如果超市货架空缺，提醒商家补货 （模拟时钟，保证顺序正确）
  ~~21. 冰箱食物存量不足时，结合用户的饮食偏好自动生成购物清单并发送到手机~~
  22. 用户在旅游且听歌时，根据天气情况选择合适风格的歌曲 （需求比较奇怪）
  ~~23. 如果土壤湿度过低/发现病虫害/牲畜离开圈养地，通知农民并自动开启灌溉系统~~ 

Task修改：
- 共性问题：
  - 所有description要完整，description内容要有意义，不能太简单，fields描述要完整，不要有xxx
  - 不要保留print，注释掉也不行
  - 所有内容必须能从description中得到
  - 命名要合理
  - 没有用的东西不要有
  - 英语语法要规范
  - agent_id要有意义
  - input stream描述讲清楚来源、内容等细节信息
  - 所有代码符合PEP8规范
- activity_task描述没更新
- arxiv task:
  - task1：batch by_count=2 来的没有根据
  - task2：和1没有区别
- desktop ui：task太简单，而且为什么要输入xml
- ego4d：
  - task1: input描述没有字段，还有其他共性问题
  - task2: 两个问题连着问的意义是什么，得到的结果没有处理直接推流的意义是什么
  - task3: “Automatically record xxx this morning”，this morning是哪个morning？想一想这种agent写出来怎么用
- email：
  - 不要所有都是by_count=2，这没什么意义
  - task4回复email没有用处，task5是啥
- first person：task描述没更新
- github：
  - task1: by_count之后只有10个了，再sort取10个太奇怪了。

TODO

- Ego4d dataset: 20个
  - 活动类：当前是否在 跳绳/开会/做饭/看书，3-5个
  - 环境识别类：当前是否在 室内外/家/厨房/傍晚 3-5个
  - 物体类：视野内是否有 人/自行车/哆啦A梦玩偶 3-5个
- 第三人称视频： 20个有data的，再多的没有data
  - 室内
    - 电梯：有人没人/有没有电动车
    - 办公室：当前在工作还是在讨论/工作的情绪/玩手机的次数
    - 会议室：是否在开会/是否关门
    - 卧室：有没有睡觉工作/猫粮有没有吃完
    - 厨房：水龙头有没有常开/煤气灶在没人的时候有没有开
    - 任何场景：灯关了没有/着火了没有/有没有人摔倒/有没有人打架/有没有关窗/有没有恐怖分子
    - 超市：有没有客人进来/货架上有没有空位/排队长度有没有超标
    - 医院：x光室工作时门口有没有人/通往急诊的通道有没有障碍物/有没有医生在诊室
    - 学校：教室在不在上课/讨论室内有没有人在讨论/图书馆食堂人多不多/幼儿园小朋友有没有摔倒
    - 实验室：使用某些工作台时必须开通风厨/放射性物质暴露时必须穿防护服
    - 车内：驾驶员有没有睡觉/后座的儿童有没有离开儿童座椅/行车记录仪看到美丽的晚霞帮我自动录像/判断车上的氛围是独自一人还是朋友出游还是工作
  - 室外
    - 任何场景：天气怎么样/白天还是夜晚/季节
    - 农业：庄稼有没有大面积倒伏/有没有野猪群/养鸡场饲料够不够/养鸡场鸡有没有下蛋/粮仓有没有漏雨
    - 操场：有没有人在打篮球
    - 公共场所
      - 高铁/飞机：有没有管制刀具/跑道上有没有人和物体/有没有其他人拿走我放在角落的行李箱
      - 公园：有没有人落水/冰面有没有开裂
      - 交通：有没有车祸/有没有汽车自燃/地铁上有没有人抽烟/有没有人打架/有没有井没有盖/有没有树倒下
- 截屏：10个有data的，其他没有data
  - 手机截屏
    - 当前在哪个App/在不在聊天/在不在通话/在不在打游戏
    - 在看什么类型的视频/在听什么音乐/在聊什么话题/点了什么外卖/导航去哪里
    - 手机壁纸是什么/社交媒体头像是什
  - PC截屏
    - 在写代码还是在写文档/桌面有什么软件/代码语言是什么
- Sensor：20-30个有data，dataset纯随机生成
  - GPS：我们行李箱有没有离我超过50米远/我在哪个国家/在哪个城市/在家还是在单位
  - 运动传感器：在走路还是跑步
  - 生物传感器：心率和工作内容和环境判断用户情绪
  - 温湿度：温度决定是否开空调
  - 参考privacy-stream的例子
  - 非AI的Agent：筛选、分类、聚合、总结。。。
- 文本：20个
  - twitter：帮我找到高赞推文/找到AI Agent相关推文/找到评论区讨论丰富的推文
  - 身份关系：医患对话间的疫病名字感知/师生对话间的学习情况或者任务感知/同事对话间的工作计划总结
  - 生成类：在sms中找到新的日程/在email中找到新的任务
## Task Without dataset (200 - 500 examples)
- email dataset:
  - ....
  - 记得将所有的descript_list写好
- 