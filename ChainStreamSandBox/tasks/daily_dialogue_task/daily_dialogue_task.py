import os
import csv
import chainstream as cs
from ..task_config_base import TaskConfigBase

class DialogueTaskConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.task_description = (
            "Retrieve data from the input stream all_dialogues,process the dialogue data: Classify the following dialogues contents into one of the categories: positive, negative, neutral, other. Choose one and explain.Finally output the answer to the stream 'cs_news'."
            "and save the results in the output stream.")
        self.dialogue_data = self._get_dialogue_data()

    def init_environment(self, runtime):
        self.input_dialogue_stream = cs.stream.create_stream('all_dialogues')
        self.output_dialogue_stream = cs.stream.create_stream('cs_dialogues')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_dialogue_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for dialogue in self.dialogue_data:
            self.input_dialogue_stream.add_item(dialogue)

    def evaluate_task(self, runtime):
        if len(self.output_record) == 0:
            return False, "No dialogues found"
        else:
            return True, f"{len(self.output_record)} dialogues found"

    def _get_dialogue_data(self):
        data_file = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "test_data", "daily_dialog",
                                 "ijcnlp_dailydialog", "conversations.csv")
        dialogues = []

        with open(data_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                new_message = {}
                new_message['id'] = row[0]  # Conversation Number
                new_message['text'] = row[1]  # Conversation
                dialogues.append(new_message)

        return dialogues

if __name__ == '__main__':
    config = DialogueTaskConfig()
