## ChainStream SandBox

用于评测ChainStream的agent，主要评测流程如下：

1. 选定待评测的Agent
2. 选择或者新建一个Task。
   - 若创建新task，需继承task_config_base.py的TaskConfig类，覆写三个方法：
       - init_environment：初始化task环境，创建测试用的agent和stream
       - start_stream： 启动源头stream，并收集output stream数据
       - evaluate_stream：对output stream数据进行评测，返回评测结果
3. 通过sandbox类启动评测

### task数据集:
- batch_simulation_scripts: batch test generator
- task描述，以及最终的output stream
- 数据源：原始message、email、twitter、image、audio等
- 人类编写的几个agent例程
- 需要选择的stream
- output stream的评测函数

### 评测指标:
 1. 运行成功率：agent start后能不能不报错
2. 输入输出选取正确性：input、output stream是否正确选取
3. 静态评测：生成代码与人类例程的差别
4. 动态评测：生成代码与人类例程output stream的差别

### 评测环境：
- 需要有一个运行着的Runtime，并且该Runtime打开了评测模式，可以监控测试agent的动作
- 监控的动作包括：
    1. get_stream、create_stream、for_each
    2. get_model、make_prompt、query
    3. stream.add_item
- 评测流程：
    1. 初始化Runtime，设置所使用的task和agent
    2. 加载task的配置文件，初始化该task环境
    3. 启动agent，配置各动作监听
    4. 启动task数据源
    5. 数据源结束后收集测试结果，存档并调用评测函数

