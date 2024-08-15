import chainstream as cs
import inspect


class TaskConfigBase(cs.agent.Agent):
    """
    task数据集:
    - task描述，以及最终的output stream
    - 数据源：原始message、email、twitter、image、audio等
    - 人类编写的几个agent例程
    - 需要选择的stream

    - 初始化task函数
    - 流开启函数
    - output stream的评测函数
    """

    def __init__(self):
        super().__init__("TaskConfigBase")
        self.task_id = self.__class__.__name__

        self.task_description = None

        self.need_stream = []
        self.output_stream = []

        self.agent_example = None

    def init_environment(self, runtime):
        raise RuntimeError("Not implemented")

    def start_task(self, runtime) -> dict:
        raise RuntimeError("Not implemented")

    def record_output(self) -> dict:
        raise RuntimeError("Not implemented")


class SingleAgentTaskConfigBase(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = {}

    def record_output(self) -> dict:
        # print(self.output_record)

        # if len(self.output_record) == 0:
        #     return {
        #         "status": "[ERROR] No output message found",
        #         "data": []
        #     }
        # else:
        #     return {
        #         "status": "[OK] Task completed",
        #         "data": self.output_record
        #     }
        for stream_id, record in self.output_record.items():
            if len(record) == 0:
                self.output_record[stream_id] = {
                    "status": "[ERROR] No output message found",
                    "data": []
                }

            else:
                self.output_record[stream_id] = {
                    "status": "[OK] Task completed",
                    "data": record
                }
        return self.output_record
