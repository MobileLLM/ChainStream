from ..task_config_base import TaskConfigBase
import os
import json
import random
import chainstream as cs

random.seed(6666)


class WorkSmsTaskConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.task_description = ("Read data from the input stream 'all_sms', define and register a listener function, and classify each SMS message into one of the categories (positive, negative, neutral, other) based on its content. Output the message along with its classification to stream 'cs_sms'."
                                 "and save the results in the output stream.")

        self.sms_data = self._get_sms_data()

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

    def evaluate_task(self, runtime):
        print(self.output_record)
        if len(self.output_record) == 0:
            return False, "No work-related message found"
        else:
            return True, "Work-related message found"


    def _get_sms_data(self):
        data_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "test_data", "sms", "archive",
                                 "smsCorpus_en_2015.03.09_all.json"
                                 )
        data = json.load(open(data_file, "r"))
        messages = data['smsCorpus']['message']

        received_messages = {}
        for message in messages:
            if message['destination'] is not None and message['destination']['destNumber'] is not None and \
                    message['destination']['destNumber']['$'] is not None:
                if message['destination']['destNumber']['$'] == 'unknown':
                    continue

                new_message = {}
                new_message['id'] = message['@id']
                new_message['text'] = message['text']['$']
                new_message['language'] = message['messageProfile']['@language']
                new_message['time'] = message['messageProfile']['@time']

                if message['destination']['destNumber']['$'] not in received_messages:
                    received_messages[message['destination']['destNumber']['$']] = [new_message]
                else:
                    received_messages[message['destination']['destNumber']['$']].append(new_message)

        tmp_del_list = []
        for k, v in received_messages.items():
            if len(v) < 10:
                tmp_del_list.append(k)
        for k in tmp_del_list:
            del received_messages[k]

        return received_messages[random.choice(list(received_messages.keys()))]


if __name__ == '__main__':
    config = WorkSmsTaskConfig()
