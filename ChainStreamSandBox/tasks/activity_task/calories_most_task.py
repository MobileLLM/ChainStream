from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ActivityData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class OldActivityTask3(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_activity_stream = None
        self.input_activity_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Activity,
                                scene=Scene_Task_tag.Exercise, modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_activities",
            "description": "A list of activities records (every five copies of activities data are packaged as a "
                           "batch)",
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
                "stream_id": "calories_burned_most",
                "description": "A list of records of the most calories-burned activities",
                "fields": {
                    "Date": "The date of the activities recorded, string",
                    "Activity": "The specific activity, string",
                    "Calories_Burned": "The calories burned in the activity, float"
                }
            }
        ])

        self.activity_data = ActivityData().get_random_activity_data()
        self.agent_example = '''
import chainstream as cs
class ActivityDistanceAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("calories_agent")
        self.input_stream = cs.get_stream(self, "all_activities")
        self.output_stream = cs.get_stream(self, "calories_burned_most")

    def start(self):
        def process_activity(activity_dict):
            activity_list = activity_dict['item_list']
            sorted_list = sorted(activity_list, key=lambda x: x['Calories_Burned'], reverse=True)
            for activity in sorted_list:
                date = activity.get("Date", "Unknown Date")
                motion = activity.get("activity", "Unknown Motion")
                calories_burned = activity.get("Calories_Burned", 0)
                self.output_stream.add_item({
                    "Date": date,
                    "Activity": motion,
                    "Calories_Burned": calories_burned
                })
        
        self.input_stream.batch(by_count=5).for_each(process_activity)
        '''

    def init_environment(self, runtime):
        self.input_activity_stream = cs.stream.create_stream(self, 'all_activities')
        self.output_activity_stream = cs.stream.create_stream(self, 'calories_burned_most')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['calories_burned_most'].append(data)

        self.output_activity_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        activity_dict = {'all_activities': []}
        for activity in self.activity_data:
            self.input_activity_stream.add_item(activity)
            activity_dict['all_activities'].append(activity)
        return activity_dict
