from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ActivityData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class ActivityTask2(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_activity_stream = None
        self.input_activity_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Activity,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_activities",
            "description": "A stream of activities records",
            "fields": {
                "Date": "The date of the activities recorded, string",
                "activity": "The specific activity, string",
                "Fairly_Active_Minutes": "The minutes of the activities, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "activity_over_30min",
                "description": "A stream of records when the activities are more than 30 minutes",
                "fields": {
                    "Date": "the date when exercising more than 30 minutes, string",
                    "activity": "The specific activity, string",
                    "Fairly_Active_Minutes": "The minutes of the exercise, float"}
            }
        ])

        self.activity_data = ActivityData().get_random_activity_data()
        self.agent_example = '''
import chainstream as cs

class ActivityDistanceAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("activity_time_agent")
        self.input_stream = cs.get_stream(self, "all_activities")
        self.output_stream = cs.create_stream(self, "activity_over_30min")

    def start(self):
        def process_activity(activity):
            Fairly_Active_Minutes = activity.get("Fairly_Active_Minutes", 0)
            if Fairly_Active_Minutes > 30:
                date = activity.get("Date", "Unknown Date")
                motion = activity.get("activity", "Unknown Motion")
                self.output_stream.add_item({
                    "Date": date,
                    "activity": motion,
                    "Fairly_Active_Minutes": Fairly_Active_Minutes
                })

        self.input_stream.for_each(process_activity)
        '''

    def init_environment(self, runtime):
        self.input_activity_stream = cs.stream.create_stream(self, 'all_activities')
        self.output_activity_stream = cs.stream.create_stream(self, 'activity_over_30min')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['activity_over_30min'].append(data)

        self.output_activity_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_activity_stream = cs.stream.create_stream(self, 'all_activities')

    def init_output_stream(self, runtime):
        self.output_activity_stream = cs.stream.get_stream(self, 'activity_over_30min')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['activity_over_30min'].append(data)

        self.output_activity_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        activity_dict = {'all_activities': []}
        for activity in self.activity_data:
            self.input_activity_stream.add_item(activity)
            activity_dict['all_activities'].append(activity)
        return activity_dict
