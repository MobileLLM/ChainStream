from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SMSData

random.seed(6666)


class OldMessageTask4(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_sms_stream = None
        self.input_sms_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_sms',"
            "and process the value corresponding to the 'text' key in the SMS dictionary: "
            "Aummarize the content of each SMS message into a concise sentence using an LLM."
            "Output the summarized message to the stream 'cs_sms'."
        )

        self.sms_data = SMSData().get_random_message()
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_message_agent")
        self.input_stream = cs.get_stream(self,"all_sms")
        self.output_stream = cs.get_stream(self,"cs_sms")
        self.llm = get_model("Text")
    def start(self):
        def process_sms(sms):
            sms_text = sms["text"]
            prompt = "Summarize the content of the following each SMS message in a sentence"
            response = self.llm.query(cs.llm.make_prompt(prompt,sms_text))
            print(sms_text+" : "+response)
            self.output_stream.add_item(sms_text+" : "+response)
        self.input_stream.for_each(process_sms)
        '''

    def init_environment(self, runtime):
        self.input_sms_stream = cs.stream.create_stream(self, 'all_sms')
        self.output_sms_stream = cs.stream.create_stream(self, 'cs_sms')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_sms_stream.for_each(record_output)

    def start_task(self, runtime):
        message_list = []
        for message in self.sms_data:
            self.input_sms_stream.add_item(message)
            message_list.append(message)
        return message_list


if __name__ == '__main__':
    config = MessageSummaryConfig()
