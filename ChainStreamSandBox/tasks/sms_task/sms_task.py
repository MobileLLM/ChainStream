from ..task_config_base import TaskConfigBase
import os
import json
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SMSData

random.seed(6666)


class WorkSmsTaskConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_sms_stream = None
        self.input_sms_stream = None
        self.task_description = ("Read data from the input stream 'all_sms', define and register a listener function, "
                                 "and classify each SMS message into one of the categories (positive, negative, "
                                 "neutral, other) based on its content. Output the message along with its "
                                 "classification to stream 'cs_sms'."
                                 "and save the results in the output stream.")

        self.sms_data = SMSData().get_random_message()

    def init_environment(self, runtime):
        self.input_sms_stream = cs.stream.create_stream('all_sms')
        self.output_sms_stream = cs.stream.create_stream('cs_sms')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_sms_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for message in self.sms_data:
            self.input_sms_stream.add_item(message)

    def record_output(self, runtime):
        print(self.output_record)
        if len(self.output_record) == 0:
            return False, "No work-related message found"
        else:
            return True, "Work-related message found"


if __name__ == '__main__':
    config = WorkSmsTaskConfig()
