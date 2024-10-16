import datetime


class AgentRecorder:
    """
    This class is used to record the data of the agent during the analysis.
    """
    def __init__(self, agentMetaData, analysis_pre_min=10):
        self.start_time = datetime.datetime.now()

        self.total_item_count = 0
        self.item_log = []
        self.item_pre_gap = []
