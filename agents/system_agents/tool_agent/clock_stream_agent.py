import chainstream as cs
import schedule
import time
import datetime
import threading


class ClockStreamAgent(cs.agent.Agent):
    is_agent = True

    def __init__(self, agent_id='clock_stream_agent'):
        super().__init__(agent_id)
        self.clock_stream = cs.stream.create_stream('clock_hours_stream')
        self.thread = None
        self.enabled = True

    def start(self):
        schedule.every().hour.at(":00").do(self.log_time)
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def log_time(self):
        self.clock_stream.add_item(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def _run(self):
        while self.enabled:
            time.sleep(60)
            schedule.run_pending()

    def stop(self):
        self.enabled = False
