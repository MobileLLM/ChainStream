from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ActivityData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class OldActivityTask1(SingleAgentTaskConfigBase):
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
            "description": "A series of activities records",
            "fields": {
                "Total_Distance": "The total distance statistic recorded, float",
                "Date": "The date of the activities recorded, string",
                "activity": "The specific activity, string",
                "Calories_Burned": "The calories burned in the activity, float",
                "Fairly_Active_Minutes": "The minutes of the activities, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "distance_over_5k",
                "description": "A series of activities records when more than 5km",
                "fields": {
                    "Date": "the date when exercising more than 5 km, string",
                    "Total_Distance": "The total distance statistic recorded when exercising more than 5 km, string"}
            }
        ])

        self.activity_data = ActivityData().get_random_activity_data()
        self.agent_example = '''
import chainstream as cs

class ActivityDistanceAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("activity_distance_agent")
        self.input_stream = cs.get_stream(self, "all_activities")
        self.output_stream = cs.get_stream(self, "distance_over_5k")

    def start(self):
        def process_activity(activity):
            total_distance = activity.get("Total_Distance", 0)
            if total_distance > 5:
                date = activity.get("Date", "Unknown Date")
                self.output_stream.add_item({                    
                    "Date": date,
                    "Total_distance": total_distance
                })
        self.input_stream.for_each(process_activity)

        '''

    def init_environment(self, runtime):
        self.input_activity_stream = cs.stream.create_stream(self, 'all_activities')
        self.output_activity_stream = cs.stream.create_stream(self, 'distance_over_5k')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['distance_over_5k'].append(data)

        self.output_activity_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        activity_dict = {'all_activities': []}
        for activity in self.activity_data:
            self.input_activity_stream.add_item(activity)
            activity_dict['all_activities'].append(activity)
        return activity_dict
