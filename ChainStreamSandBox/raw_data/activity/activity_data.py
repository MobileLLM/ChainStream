import random


class ActivityData:
    def __init__(self):
        self.activity = ['walking', 'running', 'sitting', 'upstairs', 'downstairs', 'jogging']

    def get_activity_sequence(self):
        activity_sequence = []

        act_num = random.randint(1, 4)

        act_seq = [random.choice(self.activity) for _ in range(act_num)]

        for act in act_seq:
            act_len = random.randint(1, 5)
            activity_sequence.extend([act for i in range(act_len)])

        return activity_sequence


if __name__ == '__main__':
    ad = ActivityData()
    print(ad.get_activity_sequence())
