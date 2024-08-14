from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ActivityData

random.seed(6666)


class OldActivityTask4(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_activity_stream = None
        self.input_activity_stream = None
        self.task_description = (
            "Retrieve data from the input stream all_activities.Extract the 'Date', 'activity', and 'Steps' if "
            "'Steps' is greater than 5000, and add the formatted string to the output stream cs_activities. "
        )

        self.activity_data = ActivityData().get_random_activity_data()
        self.agent_example = '''
import chainstream as cs

class ActivityDistanceAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("activity_steps_agent")
        self.input_stream = cs.get_stream(self,"all_activities")
        self.output_stream = cs.get_stream(self,"cs_activities")

    def start(self):
        def process_activity(activity):
            Steps = activity.get("Steps", 0)
            if Steps > 5000:
                date = activity.get("Date", "Unknown Date")
                motion = activity.get("activity", "Unknown Motion")
                output = f"Date: {date}, Activity:{motion}, Steps: {Steps}"
                print(output)
                self.output_stream.add_item(output)

        self.input_stream.for_each(process_activity)
        '''

    def init_environment(self, runtime):
        self.input_activity_stream = cs.stream.create_stream(self, 'all_activities')
        self.output_activity_stream = cs.stream.create_stream(self, 'cs_activities')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_activity_stream.for_each(record_output)

    def start_task(self, runtime):
        activity_list = []
        for activity in self.activity_data:
            self.input_activity_stream.add_item(activity)
            activity_list.append(activity)
        return activity_list

