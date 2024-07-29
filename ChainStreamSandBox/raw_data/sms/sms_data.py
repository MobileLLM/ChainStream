import json
import random

random.seed(42)


def _split_messages(messages):
    received_messages = {}
    for message in messages:
        if message['destination'] is not None and message['destination']['destNumber'] is not None and \
                message['destination']['destNumber']['$'] is not None:
            if message['destination']['destNumber']['$'] == 'unknown':
                continue

            if '$' not in message['text'] or message['text']['$'] is None:
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

    return received_messages


class SMSData:
    def __init__(self):
        self.en_data_path = "archive/smsCorpus_en_2015.03.09_all.json"
        self.zh_data_path = "archive/smsCorpus_zh_2015.03.09.json"

        self.en_data = {}
        self.zh_data = {}

        self._load_data()

    def _load_data(self):
        en_data = json.load(open(self.en_data_path, "r", encoding="utf-8"))['smsCorpus']['message']
        zh_data = json.load(open(self.zh_data_path, "r", encoding="utf-8"))['smsCorpus']['message']

        self.en_data = _split_messages(en_data)
        self.zh_data = _split_messages(zh_data)

    def __len__(self):
        return len(self.en_data) + len(self.zh_data)

    def __getitem__(self, index):
        if index < len(self.en_data):
            return random.choice(self.en_data[index])
        else:
            return random.choice(self.zh_data[index - len(self.en_data)])

    def get_random_message(self, language='en'):
        if language == 'en':
            k = random.choice(list(self.en_data.keys()))
            return self.en_data[k]
        elif language == 'zh':
            k = random.choice(list(self.zh_data.keys()))
            return self.zh_data[k]
        else:
            raise ValueError("Invalid language")


if __name__ == "__main__":
    sms_data = SMSData()
    print(len(sms_data))
    print(sms_data.get_random_message('en'))
    print(sms_data.get_random_message('zh'))
