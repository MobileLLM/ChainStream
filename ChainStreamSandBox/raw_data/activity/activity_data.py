import random




class ActivityData:
    def __init__(self):
        self.activity = ['walking', 'running', 'sitting', 'upstairs', 'downstairs', 'jogging']


    def get_activity_sequence(self):
        activity_sequence = []


        act_num = random.randint(1, 4)
        print("act_num: ", act_num)

        act_seq = [random.choice(self.activity) for i in range(act_num)]
        print("act_seq: ", act_seq)

        for act in act_seq:
            act_len = random.randint(1, 5)
            print("act_len: ", act_len)
            activity_sequence.extend([act for i in range(act_len)])


        return activity_sequence


if __name__ == '__main__':
    ad = ActivityData()
    print(ad.get_activity_sequence())


