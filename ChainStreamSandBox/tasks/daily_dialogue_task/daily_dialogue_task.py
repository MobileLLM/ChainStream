import os
import csv
import chainstream as cs
from ..task_config_base import TaskConfigBase
from ChainStreamSandBox.raw_data import DialogData


class DialogueTaskConfig(TaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_dialogue_stream = None
        self.input_dialogue_stream = None
        self.task_description = (
            "Retrieve data from the input stream all_dialogues,process the dialogue data: Classify the following "
            "dialogues contents into one of the categories: positive, negative, neutral, other. Choose one and "
            "explain. Finally output the answer to the stream 'dialogue_classification'."
            "and save the results in the output stream.")
        self.dialogue_data = DialogData().get_dialog_batch(batch_size=10, topic=None)

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

    def record_output(self, runtime):
        if len(self.output_record) == 0:
            return False, "No dialogues found"
        else:
            return True, f"{len(self.output_record)} dialogues found"


if __name__ == '__main__':
    config = DialogueTaskConfig()
