# from ..task_config_base import TaskConfigBase
import os
import json
import tqdm

# get ../../data/sms_data/ by os
sms_data_base_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'test_data','sms', 'archive')

sms_en_file = 'smsCorpus_en_2015.03.09_all.json'
sms_zh_file = 'smsCorpus_zh_2015.03.09.json'

# class SmsTaskConfigBase(TaskConfigBase):
#     def __init__(self, task_description):
#         super().__init__()
#         self.task_description = task_description
#
#         self.need_stream = ['sms_message']
#
#     def init_enviroment(self):
#         pass

if __name__ == '__main__':
    file_path = os.path.join(sms_data_base_path, sms_en_file)
    data = json.load(open(file_path, 'r'))
    print(data['smsCorpus']['message'][0])
    messages = data['smsCorpus']['message']
    userID = {}
    receiverID = {}
    for message in messages:
        if message['source'] is not None and message['source']['userProfile'] is not None and message['source']['userProfile']['userID']['$'] is not None:
            if message['source']['userProfile']['userID']['$'] == 'unknown':
                continue
            if message['source']['userProfile']['userID']['$'] not in userID:
                userID[message['source']['userProfile']['userID']['$']] = 1
            else:
                userID[message['source']['userProfile']['userID']['$']] += 1
        if message['destination'] is not None and message['destination']['destNumber'] is not None and message['destination']['destNumber']['$'] is not None:
            if message['destination']['destNumber']['$'] == 'unknown':
                continue
            if message['destination']['destNumber']['$'] not in receiverID:
                receiverID[message['destination']['destNumber']['$']] = 1
            else:
                receiverID[message['destination']['destNumber']['$']] += 1


    print(max(userID.values()))
    print(max(receiverID.values()))

    senderMessage = {}
    receiverMessage = {}
    for message in messages:
        if message['source'] is not None and message['source']['userProfile'] is not None and message['source']['userProfile']['userID']['$'] is not None:
            if message['source']['userProfile']['userID']['$'] == 'unknown':
                continue
            if message['source']['userProfile']['userID']['$'] not in senderMessage:
                senderMessage[message['source']['userProfile']['userID']['$']] = [message['text']['$']]
            else:
                senderMessage[message['source']['userProfile']['userID']['$']].append(message['text']['$'])
        if message['destination'] is not None and message['destination']['destNumber'] is not None and message['destination']['destNumber']['$'] is not None:
            if message['destination']['destNumber']['$'] == 'unknown':
                continue
            if message['destination']['destNumber']['$'] not in receiverMessage:
                receiverMessage[message['destination']['destNumber']['$']] = [message]
            else:
                receiverMessage[message['destination']['destNumber']['$']].append(message)

    print(len(senderMessage))
    print(len(receiverMessage))

    del_list = []
    # for k, v in userID.items():
    #     if v < 20:
    #         del_list.append(k)
    # for k in del_list:
    #     del userID[k]
    message_between_user = {}
    seen_user = set()
    for user1, v in tqdm.tqdm(userID.items()):
        for user2, v2 in userID.items():
            if user1 == user2 or (user1, user2) in seen_user or (user2, user1) in seen_user:
                continue
            seen_user.add((user1, user2))
    message_between_user = {(user1, user2): [] for user1, user2 in seen_user}
    for message in messages:
        if message['source'] is not None and message['source']['userProfile'] is not None and \
                message['source']['userProfile']['userID']['$'] is not None and message['source']['userProfile']['userID']['$'] != 'unknown':
            if message['destination']['destNumber']['$'] is not None and message['destination']['destNumber']['$'] != 'unknown':
                user1 = message['source']['userProfile']['userID']['$']
                user2 = message['destination']['destNumber']['$']
                if (user1, user2) in seen_user:
                    message_between_user[(user1, user2)].append(message)
                if (user2, user1) in seen_user:
                    message_between_user[(user2, user1)].append(message)
    tmp_del_list = []
    for k, v in message_between_user.items():
        if len(v) == 0:
            tmp_del_list.append(k)
    for k in tmp_del_list:
        del message_between_user[k]
    print(len(message_between_user))
    print(message_between_user)

    a = 1