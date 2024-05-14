### task数据集:
- task描述，以及最终的output stream
- 数据源：原始message、email、twitter、image、audio等
- 人类编写的几个agent例程
- 需要选择的stream
- output stream的评测函数

### 评测指标:
- 运行成功率：挂载成功率
- 数据源选取正确率：监听的数据源是否正确，需规定每个任务的最少监听数据源
- output正确性：肉眼比较、标准答案比较
- prompt正确性：多次执行同一段代码的一致性
- 代码评测：和人类例程的差别

### 数据源：
1. camera image：
    - 第一人称视角图像
    - 监控视角图像
2. microphone audio
    - 可以直接使用文本假装我们前面完成了转录工作
3. chat message
    - 聊天记录
4. email history
    - 邮件历史记录
5. daily arxiv paper
    - 日常arxiv论文
6. screen snapshot
    - 屏幕快照

### 评测环境：
- 需要有一个运行着的Runtime，并且该Runtime打开了评测模式，可以监控测试agent的动作
- 监控的动作包括：
    1. get_stream、create_stream、register_listener
    2. get_model、make_prompt、query
    3. stream.add_item
- 评测流程：
    1. 初始化Runtime，设置所使用的task和agent
    2. 加载task的配置文件，初始化该task环境
    3. 启动agent，配置各动作监听
    4. 启动task数据源
    5. 数据源结束后收集测试结果，存档并调用评测函数

### TODO list：
- runtime增加评测模式
- 编写OJ
- 编写task配置文件
- 完善nl2dsl prompt
- 编写评测函数
- 撰写一大堆task，并收集多模态原始数据