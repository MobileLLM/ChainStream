from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import ActivityData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
import time

random.seed(6666)


class ActivityTask5(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_activity_stream = None
        self.input_activity_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Activity,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_activities",
            "description": "A stream of activities records",
            "fields": {
                "activity": "The specific activity, string",
                "user": "The user id, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "activity_for_each_user",
                "description": "A stream of activities grouped by each user, with batches packaged every 10 seconds",
                "fields": {
                    "users_activities": "A record of the activities grouped by each user, string"}
            }
        ])

        self.activity_data = ActivityData().get_random_activity_data()
        self.agent_example = '''
import chainstream as cs

class ActivityDistanceAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("activity_distance_agent")
        self.input_stream = cs.get_stream(self, "all_activities")
        self.output_stream = cs.create_stream(self, "activity_for_each_user")

    def start(self):
        def group_by_user(activities_list):
            activities = activities_list['item_list']
            user_group = {}
            for activity in activities:
                if activity['user'] not in user_group:
                    user_group[activity['user']] = [activity['activity']]
                else:
                    user_group[activity['user']].append(activity['activity'])
            self.output_stream.add_item({
                "users_activities": str(user_group)
            })
            return list(user_group.values())
            
        self.input_stream.batch(by_time=10).for_each(group_by_user)

        '''

    def init_environment(self, runtime):
        self.input_activity_stream = cs.stream.create_stream(self, 'all_activities')
        self.output_activity_stream = cs.stream.create_stream(self, 'activity_for_each_user')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['activity_for_each_user'].append(data)

        self.output_activity_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_activity_stream = cs.stream.create_stream(self, 'all_activities')

    def init_output_stream(self, runtime):
        self.output_activity_stream = cs.stream.get_stream(self, 'activity_for_each_user')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['activity_for_each_user'].append(data)

        self.output_activity_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        activity_dict = {'all_activities': []}
        for activity in self.activity_data:
            self.input_activity_stream.add_item(activity)
            activity_dict['all_activities'].append(activity)
            time.sleep(1)
        return activity_dict
