
class TaskConfigBase:
    '''
    task数据集:
    - task描述，以及最终的output stream
    - 数据源：原始message、email、twitter、image、audio等
    - 人类编写的几个agent例程
    - 需要选择的stream

    - 初始化task函数
    - 流开启函数
    - output stream的评测函数
    '''
    def __init__(self):
        self.task_description = None

        self.need_stream = []
        self.output_stream = []

        self.agent_example = None

    def init_enviroment(self):
        raise RuntimeError("Not implemented")
    
    def start_stream(self):
        raise RuntimeError("Not implemented")

    def evaluate_stream(self):
        raise RuntimeError("Not implemented")



