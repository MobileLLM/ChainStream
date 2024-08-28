import csv
import random
import os
random.seed(42)

"""Here are some explanations about the files:

1) dialogues_text.txt: The DailyDialog dataset which contains 11,318 transcribed dialogues.
2) dialogues_topic.txt: Each line in dialogues_topic.txt corresponds to the topic of that in dialogues_text.txt.
                        The topic number represents: {1: Ordinary Life, 2: School Life, 3: Culture & Education,
                        4: Attitude & Emotion, 5: Relationship, 6: Tourism , 7: Health, 8: Work, 9: Politics, 10: Finance}
3) dialogues_act.txt: Each line in dialogues_act.txt corresponds to the dialog act annotations in dialogues_text.txt.
                      The dialog act number represents: { 1: inform，2: question, 3: directive, 4: commissive }
4) dialogues_emotion.txt: Each line in dialogues_emotion.txt corresponds to the emotion annotations in dialogues_text.txt.
                          The emotion number represents: { 0: no emotion, 1: anger, 2: disgust, 3: fear, 4: happiness, 5: sadness, 6: surprise}
5) train.zip, validation.zip and test.zip are two different segmentations of the whole dataset. """

emo_idx_to_text = {0: "no emotion", 1: "anger", 2: "disgust", 3: "fear", 4: "happiness", 5: "sadness", 6: "surprise"}
act_idx_to_text = {1: "inform", 2: "question", 3: "directive", 4: "commissive"}
topic_idx_to_text = {1: "Ordinary Life", 2: "School Life", 3: "Culture & Education", 4: "Attitude & Emotion",
                     5: "Relationship", 6: "Tourism", 7: "Health", 8: "Work", 9: "Politics", 10: "Finance"}


class DialogData:
    def __init__(self):
        base_dir = os.path.join(os.path.dirname(__file__), "ijcnlp_dailydialog")
        self.text_path = os.path.join(base_dir, "dialogues_text.txt")
        self.act_path = os.path.join(base_dir, "dialogues_act.txt")
        self.emotion_path = os.path.join(base_dir, "dialogues_emotion.txt")
        self.topic_path = os.path.join(base_dir, "dialogues_topic.txt")

        self.dialog_data = []

        self._load_data()

    def _load_data(self):
        dialog_data = []
        act_data = []
        emotion_data = []
        topic_data = []
        with open(self.text_path, "r", encoding="utf-8") as f:
            for line in f:
                dialog_data.append(line.split(" __eou__")[0].split(" __eou__ "))

        with open(self.act_path, "r", encoding="utf-8") as f:
            for line in f:
                act_data.append(line.strip().split())

        with open(self.emotion_path, "r", encoding="utf-8") as f:
            for line in f:
                emotion_data.append(line.strip().split())

        with open(self.topic_path, "r", encoding="utf-8") as f:
            for line in f:
                topic_data.append(line.strip())

        for i in range(len(dialog_data)):
            dialog = []
            for j in range(len(dialog_data[i])):
                dialog.append({
                    "text": dialog_data[i][j],
                    "act": act_idx_to_text[int(act_data[i][j])],
                    "emotion": emo_idx_to_text[int(emotion_data[i][j])],
                })
            self.dialog_data.append({
                "dialog": dialog,
                "topic": topic_idx_to_text[int(topic_data[i])],
                "id": i
            })

    def __len__(self):
        return len(self.dialog_data)

    def __getitem__(self, idx):
        return self.dialog_data[idx]

    def get_dialog_batch(self, batch_size, topic=None):
        if topic is None:
            dialog_batch = random.sample(self.dialog_data, batch_size)
        else:
            if topic not in topic_idx_to_text.values():
                raise ValueError("Invalid topic name")
            dialog_batch = [dialog for dialog in self.dialog_data if dialog["topic"] == topic]
            dialog_batch = random.sample(dialog_batch, batch_size)
        return dialog_batch


if __name__ == "__main__":
    dialog_data = DialogData()
    print(dialog_data.get_dialog_batch(10))
