from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import DialogData


class OldDialogueTask2(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_dialogue_stream = None
        self.input_dialogue_stream = None
        self.task_description = (
            "Retrieve data from the input stream all_dialogues,and process the value corresponding to the 'text' key in the paper dictionary:"
            "use LLM to classify the following dialogues contents into one of the categories: positive, negative, neutral, other. Choose one and "
            "explain. Finally output the answer to the stream 'dialogue_classification'."
        )
        self.dialogue_data = DialogData().get_dialog_batch(batch_size=10, topic=None)
        self.agent_example = '''
import chainstream as cs

class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_news_agent")
        self.input_stream = cs.get_stream(self,"all_dialogues")
        self.output_stream = cs.get_stream(self,"cs_dialogues")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def process_dialogues(dialogues):
            dialogues_id = dialogues["id"]
            dialogues_text = dialogues["dialog"]
            prompt = "Classify the following dialogues contents into one of the categories: positive, negative, neutral, other.Choose one and explain"
            response = self.llm.query(cs.llm.make_prompt(prompt,str(dialogues_text)))
            self.output_stream.add_item({"dialogues_id":dialogues_id,"emotion":response})

        self.input_stream.for_each(process_dialogues)
        '''

    def init_environment(self, runtime):
        self.input_dialogue_stream = cs.stream.create_stream(self, 'all_dialogues')
        self.output_dialogue_stream = cs.stream.create_stream(self, 'cs_dialogues')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_dialogue_stream.for_each(record_output)

    def start_task(self, runtime):
        dialogue_list = []
        for dialogue in self.dialogue_data:
            self.input_dialogue_stream.add_item(dialogue)
            dialogue_list.append(dialogue)
        return dialogue_list


