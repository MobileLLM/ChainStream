import chainstream as cs
from tasks.task_config_base import SingleAgentTaskConfigBase
from ChainStreamSandBox.raw_data import DialogData


class DialogueDailyConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_dialogue_stream = None
        self.input_dialogue_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_dialogues'. "
            "Add it to the output stream 'cs_dialogues'."
        )

        self.dialogue_data = DialogData().get_dialog_batch(batch_size=10, topic=None)
        self.agent_example = '''
        import chainstream as cs
        from chainstream.llm import get_model
        
        class testAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("test_news_agent")
                self.input_stream = cs.get_stream("all_dialogues")
                self.output_stream = cs.get_stream("cs_dialogues")
                self.llm = get_model(["text"])
        
            def start(self):
                def process_dialogues(dialogues):
                    print(dialogues)
                    self.output_stream.add_item(dialogues)
        
                self.input_stream.for_each(self, process_dialogues)
        
            def stop(self):
                self.input_stream.unregister_all(self)
        '''

    def init_environment(self, runtime):
        self.input_dialogue_stream = cs.stream.create_stream('all_dialogues')
        self.output_dialogue_stream = cs.stream.create_stream('cs_dialogues')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_dialogue_stream.for_each(self, record_output)

    def start_task(self, runtime):
        for dialogue in self.dialogue_data:
            self.input_dialogue_stream.add_item(dialogue)


if __name__ == '__main__':
    config = DialogueDailyConfig()
