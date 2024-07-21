from ..task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ActivityData

random.seed(6666)


class ActivityTimeConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_activity_stream = None
        self.input_activity_stream = None
        self.task_description = (
            "Retrieve data from the input stream all_activities.Extract the 'Date', 'activity', "
            "and 'Fairly_Active_Minutes' if 'Fairly_Active_Minutes' is greater than 30, and add the formatted string "
            "to the output stream cs_activities. "
        )

        self.activity_data = ActivityData().get_random_activity_data()
        self.agent_example = '''
        import chainstream as cs

        class ActivityDistanceAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("activity_time_agent")
                self.input_stream = cs.get_stream("all_activities")
                self.output_stream = cs.get_stream("cs_activities")

            def start(self):
                def process_activity(activity):
                    Fairly_Active_Minutes = activity.get("Fairly_Active_Minutes", 0)
                    if Fairly_Active_Minutes > 30:
                        date = activity.get("Date", "Unknown Date")
                        motion = activity.get("activity", "Unknown Motion")
                        output = f"Date: {date}, Activity:{motion}, Active_minutes: {Fairly_Active_Minutes}"
                        print(output)
                        self.output_stream.add_item(output)

                self.input_stream.register_listener(self, process_activity)

            def stop(self):
                self.input_stream.unregister_listener(self)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream('all_activities')
        self.output_paper_stream = cs.stream.create_stream('cs_activities')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for activity in self.activity_data:
            self.input_activity_stream.add_item(activity)


if __name__ == '__main__':
    config = ActivityTimeConfig()
