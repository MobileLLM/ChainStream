if __name__ == "__main__":
    from tasks import ALL_TASKS

    DialogueTaskConfig = ALL_TASKS['DialogueTask']

    agent_file = '''
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
            dialogues_id = dialogues["id"]
            dialogues_text = dialogues["text"]
            prompt = "Extract the main topics or themes from the following dialogues. Provide a brief summary of the primary subjects discussed."
            prompt = [
                {
                    "role": "user",
                    "content": prompt+dialogues_text
                }
            ]
            response = self.llm.query(prompt)
            print(dialogues_id+" : "+response)
            self.output_stream.add_item(dialogues_id+" : "+response)
            #print(dialogues)
            self.output_stream.add_item(dialogues)

        self.input_stream.register_listener(self, process_dialogues)

    def stop(self):
        self.input_stream.unregister_listener(self)

'''
    oj = OJ(DialogueTaskConfig(), agent_file)
    oj.start_test_agent()