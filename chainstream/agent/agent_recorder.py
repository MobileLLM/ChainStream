import datetime


class AgentRecorder:
    def __init__(self, agentMetaData, analysis_pre_min=10):
        self.start_time = datetime.datetime.now()

        self.total_item_count = 0
        self.item_log = []
        self.item_pre_gap = []
