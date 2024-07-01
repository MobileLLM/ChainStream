# All tasks for ChainStreamSandBox

## Task with dataset (> 100 examples)

- email dataset:
  1. emo classification: classify the emotion of an email message (positive, negative, neutral)
  2. date extraction: extract the date of an email message
  3. receiver extraction: extract the receiver of an email message
  4. sender extraction: extract the sender of an email message
  5. subject judgment: Judge the topic of an email message
  6. summarize content:generate a summary of an email message
  7. auto reply: generate an auto reply for an email message
- news dataset:
  1. authors extraction: extract the authors of a news article
  2. description judgment: judge the topics of a news article
  3. category classification: classify the category of a news article: classify the category of a news article
  4. date extraction: extract the date of a news article
  5. link extraction: extract the links of a news article
  6. title extraction: extract the title of a news article
  7. people extraction: extract the people mentioned in a news article
  8. place extraction: extract the places mentioned in a news article
- message dataset:
  1. content judgment: judge the content of a message
  2. emotion classification: classify the emotion of a message
  3. language identification: identify the language of a message
  4. summarize content:generate a summary of a message
  5. time extraction: extract the time of a message
- stock dataset:
  1. information presentation: present the information of stocks
  2. purchase recommendation: recommend the purchase of stocks
  3. sell recommendation: recommend the selling of stocks
  4. type recommendation: recommend the type of stocks that can be bought
- dialogue dataset:
  1. information presentation: present the information of daily dialogues
  2. emotion classification: classify the emotion of people in a daily dialogue
  3. identity identification: identify the identity of people in a daily dialogue
  4. place extraction: extract the places where a daily dialogue takes place
  5. time extraction: extract the time of a daily dialogue
  6. topic summary: summary the topic of a daily dialogue
- arxiv dataset:
  1. abstract extraction: extract the abstract of an arxiv paper
  2. algorithm identification: identify the algorithm used in an arxiv paper
  3. approach identification: identify the approach used in an arxiv paper
  4. authors identification: identify the authors of an arxiv paper
  5. comments extraction: extract the comments of an arxiv paper
  6. date extraction: extract the date of an arxiv paper
  7. implementation identification: identify the implementation used in an arxiv paper
  8. journal reference identification: identify the journal reference id of an arxiv paper
  9. problems extraction: extract the problems to solve of an arxiv paper
  10. stage identification: identify the process stage of an arxiv paper
  11. topic extraction: extract the topic of an arxiv paper
  12. website identification: identify the publication website of the arxiv paper

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
- 