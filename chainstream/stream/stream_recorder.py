import datetime


class StreamRecorder:
    def __init__(self, streamMetaData, queue, analysis_pre_min=10):
        self.streamMetaData = streamMetaData

        self.analysis_gap = analysis_pre_min

        self.tot_item_count = 0

        self.item_log = []
        self.item_pre_gap_min = []

        self.item_to_listener_count = {}

        self.queue = queue
        self.queue_len_log = []
        self.queue_len_pre_gap_min = []

        self.listener_log = []
        self.listener_pre_gap_min = []

    def record_new_item(self):
        self.tot_item_count += 1

        tmp_item_log = datetime.datetime.now()

        if self.item_pre_gap_min[-1][0] > tmp_item_log - datetime.timedelta(minutes=self.analysis_gap):
            self.item_pre_gap_min.append((tmp_item_log, len(self.item_log) / self.analysis_gap))
            self.queue_len_pre_gap_min.append(sum(self.queue_len_log) / len(self.queue_len_log))
            self.item_log = []
            self.queue_len_log = []

        self.item_log.append(tmp_item_log)
        self.queue_len_log.append(len(self.queue))

    def record_listener_change(self, listener_count):
        tmp_listener_log = datetime.datetime.now()

        if self.listener_pre_gap_min[-1][0] > tmp_listener_log - datetime.timedelta(minutes=self.analysis_gap):
            self.listener_pre_gap_min.append((tmp_listener_log, sum(self.listener_log) / len(self.listener_log)))
            self.listener_log = []

        self.listener_log.append(listener_count)

    def record_send_item(self, agent_id):
        if agent_id not in self.item_to_listener_count:
            self.item_to_listener_count[agent_id] = 1
        else:
            self.item_to_listener_count[agent_id] += 1

    def get_record_data(self):
        return {
            "record_time": datetime.datetime.now(),
            "stream_id": self.streamMetaData.stream_id,
            "tot_item_count": self.tot_item_count,
            "item_pre_gap_min": self.item_pre_gap_min,
            "queue_len_pre_gap_min": self.queue_len_pre_gap_min,
            "item_to_listener_count": self.item_to_listener_count,
            "listener_pre_gap_min": self.listener_pre_gap_min
        }
