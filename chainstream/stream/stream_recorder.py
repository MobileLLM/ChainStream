import datetime


class EdgeRecoder:
    def __init__(self, stream_id, agent_file_path=None, func_id=None, agent_id=None, type='agent_to_queue',
                 analysis_pre_min=10):
        self.stream_id = stream_id
        self.agent_file_path = agent_file_path
        self.func_id = func_id
        self.analysis_pre_min = analysis_pre_min

        if type not in ['agent_to_queue', 'queue_to_agent']:
            raise ValueError("type should be 'agent_to_queue' or 'queue_to_agent'")
        self.type = type

        if self.type == 'agent_to_queue':
            self.agent_file_path = agent_file_path
            self.func_id = func_id
        elif self.type == 'queue_to_agent':
            self.agent_id = agent_id

        self.tot = 0
        self.log = []
        self.gap_log = []
        self.statistics = []

    def record_new_item(self):
        self.tot += 1
        time_now = datetime.datetime.now()
        self.log.append(time_now)
        if self.statistics != [] and self.statistics[-1][0] > time_now - datetime.timedelta(
                minutes=self.analysis_pre_min):
            self.statistics.append(
                (time_now, len(self.gap_log) / self.analysis_pre_min))
            self.gap_log = []
        self.gap_log.append(time_now)

    def get_log(self):
        if self.type != 'agent_to_queue':
            return self.log
        return self.log

    def get_statistics(self):
        if self.type != 'agent_to_queue':
            if not self.statistics:
                return (datetime.datetime.now(), len(self.gap_log) / self.analysis_pre_min)
            return self.statistics
        return self.statistics if self.statistics != [] else (
            datetime.datetime.now(), len(self.gap_log) / self.analysis_pre_min)

    def get_total_count(self):
        return self.tot


class QueueRecoder:
    def __init__(self, stream_id, queue, analysis_pre_min=10):
        self.stream_id = stream_id
        self.queue = queue
        self.analysis_pre_min = analysis_pre_min

        self.tot = 0
        self.len_gap_log = []
        self.len_statistics = []

    def record_new_item(self):
        self.tot += 1
        time_now = datetime.datetime.now()
        if self.len_statistics != [] and self.len_statistics[-1][0] > time_now - datetime.timedelta(
                minutes=self.analysis_pre_min):
            self.len_statistics.append(
                (time_now, sum(self.len_gap_log) / len(self.len_gap_log) / self.analysis_pre_min))
        self.len_gap_log.append(self.queue.qsize())

    def get_queue_statistics(self):
        return self.len_statistics if self.len_statistics != [] else (
            datetime.datetime.now(), sum(self.len_gap_log) / len(self.len_gap_log) / self.analysis_pre_min)


class StreamRecorder:
    def __init__(self, streamMetaData, queue, analysis_pre_min=10):
        self.streamMetaData = streamMetaData

        self.analysis_gap = analysis_pre_min

        self.agent_file_func_to_queue_recorder = {}
        self.queue_to_agent_id_func_recorder = {}
        self.queue_recorder = QueueRecoder(streamMetaData.stream_id, queue, analysis_pre_min)

        self.listener_pre_gap_min = []
        self.listener_log = []

    def record_new_item(self, from_file, from_function):
        if (from_file, from_function) not in self.agent_file_func_to_queue_recorder:
            self.agent_file_func_to_queue_recorder[(from_file, from_function)] = EdgeRecoder(
                self.streamMetaData.stream_id, agent_file_path=from_file, func_id=from_function, type='agent_to_queue',
                analysis_pre_min=self.analysis_gap)
        self.agent_file_func_to_queue_recorder[(from_file, from_function)].record_new_item()
        self.queue_recorder.record_new_item()

    def record_listener_change(self, listener_count):
        tmp_listener_log = datetime.datetime.now()

        if self.listener_pre_gap_min != [] and self.listener_pre_gap_min[-1][0] > tmp_listener_log - datetime.timedelta(
                minutes=self.analysis_gap):
            self.listener_pre_gap_min.append((tmp_listener_log, sum(self.listener_log) / len(self.listener_log)))
            self.listener_log = []

        self.listener_log.append(listener_count)

    def record_send_item(self, agent_id, func_id):
        if (agent_id, func_id) not in self.queue_to_agent_id_func_recorder:
            self.queue_to_agent_id_func_recorder[(agent_id, func_id)] = EdgeRecoder(
                self.streamMetaData.stream_id, agent_id=agent_id, type='queue_to_agent',
                analysis_pre_min=self.analysis_gap)
        self.queue_to_agent_id_func_recorder[(agent_id, func_id)].record_new_item()

    def get_record_data(self, need_log=False):
        return {
            "record_time": datetime.datetime.now(),
            "stream_id": self.streamMetaData.stream_id,
            "analysis_gap": self.analysis_gap,
            "agent_to_queue": {
                (k[0], k[1]): {
                    "statistics": v.get_statistics(),
                    "tot": v.get_total_count(),
                    "log": v.get_log() if need_log else None
                } for k, v in self.agent_file_func_to_queue_recorder.items()

            },
            "queue_to_agent": {
                (k[0], k[1]): {
                    "statistics": v.get_statistics(),
                    "tot": v.get_total_count(),
                    "log": v.get_log() if need_log else None
                } for k, v in self.queue_to_agent_id_func_recorder.items()
            },
            "queue_statistics": self.queue_recorder.get_queue_statistics(),
            "listener_statistics": self.listener_pre_gap_min if self.listener_pre_gap_min != [] else [
                (datetime.datetime.now(), sum(self.listener_log))]
        }
