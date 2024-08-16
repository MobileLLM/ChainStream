from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ActivityData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class OldActivityTask2(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_activity_stream = None
        self.input_activity_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_activities",
            "description": "A list of activities records",
            "fields": {
                "Total_Distance": "The total distance statistic recorded,float",
                "Date": "The date of the activities recorded,string",
                "activity": "The specific activity,string",
                "Calories_Burned": "The calories burned in the activity,float",
                "Fairly_Active_Minutes": "The minutes of the activities,float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "activity_over_30min",
                "description": "A list of records when the activities are more than 30 minutes",
                "fields": {
                    "Date": "the date when doing activities more than 30 minutes,string",
                    "Activity": "The specific activity,string",
                    "Active_minutes": "The minutes of the activities,float"}
            }
        ])

        self.activity_data = ActivityData().get_random_activity_data()
        self.agent_example = '''
import chainstream as cs

class ActivityDistanceAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("activity_time_agent")
        self.input_stream = cs.get_stream(self,"all_activities")
        self.output_stream = cs.get_stream(self,"activity_over_30min")

    def start(self):
        def process_activity(activity):
            Fairly_Active_Minutes = activity.get("Fairly_Active_Minutes", 0)
            if Fairly_Active_Minutes > 30:
                date = activity.get("Date", "Unknown Date")
                motion = activity.get("activity", "Unknown Motion")
                self.output_stream.add_item({
                    "Date":date,
                    "Activity":motion,
                    "Active_minutes": Fairly_Active_Minutes
                })

        self.input_stream.for_each(process_activity)
        '''

    def init_environment(self, runtime):
        self.input_activity_stream = cs.stream.create_stream(self, 'all_activities')
        self.output_activity_stream = cs.stream.create_stream(self, 'activity_over_30min')
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
