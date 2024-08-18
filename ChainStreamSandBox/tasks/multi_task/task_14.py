from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SpharData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class ShopStockTask(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.input_shop_stream = None
        self.output_message_stream = None
        self.work_trigger_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "clock",
            "description": "the hours of the real-time clock data updated per three frames of the video",
            "fields": {
                "Time": "the hour information,string"
            }
        }, {
            "stream_id": "all_first_person_shop",
            "description": "first_person perspective data in the shop(write a function that use the buffer module to "
                           "store video frame items,every two for packaging as a batch)",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "output_messages",
                "description": "A message that remind merchants to stock up",
                "fields": {
                    "Notion": "Short of goods,please stock up on time!",
                }
            },
            {
                "stream_id": "work_trigger",
                "description": "A trigger when it is in working time",
                "fields": {
                    "Status": "True or False"
                }
            }
        ])
        self.video_data = SpharData().load_for_person_detection()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask14(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task14"):
        super().__init__(agent_id)
        self.clock_input = cs.get_stream(self, "clock")
        self.shop_input = cs.get_stream(self, "all_first_person_shop")
        self.message_output = cs.get_stream(self, "output_messages")
        self.llm = cs.llm.get_model("image")
        self.work_trigger = cs.get_stream(self, "work_trigger")

    def start(self):
        def business_hours(clock_input):
            clock_time_str = clock_input["Time"]  
            hour = int(clock_time_str.split(':')[0])  
            if 8 <= hour <= 22:
                self.work_trigger.add_item({"Status":"True"})
                return clock_input
        self.clock_input.for_each(business_hours)

        def check_empty_stock(shop_inputs):
            shop_input = shop_inputs["item_list"]
            if self.work_trigger == "True":
                prompt = "Are there any shelves out of stock?Simply answer y or n"
                res = self.llm.query(cs.llm.make_prompt(prompt,shop_input["frame"]))
                if res.lower()=="y":
                    self.message_output.add_item({
                    "Notion": "Short of goods,please stock up on time!"
                    })
            return shop_inputs
        def example_func(item, kwargs):
            buffer = kwargs.get('buffer', Buffer())
            kwargs['buffer'] = buffer
            if len(buffer) < 2:
                print("buffer is too short")
                buffer.append(item)
                print(buffer.get_all())
                return None, kwargs
            else:
                buffer.append(item)
                all_items = buffer.pop_all()
                return {"item_list": all_items}, kwargs   
        self.shop_input.batch(by_func=example_func).for_each(check_empty_stock)
        '''

    def init_environment(self, runtime):
        self.input_shop_stream = cs.stream.create_stream(self, 'all_first_person_shop')
        self.clock_stream = cs.stream.create_stream(self, 'clock')
        self.output_message_stream = cs.stream.create_stream(self, 'output_messages')
        self.work_trigger_stream = cs.stream.create_stream(self, 'work_trigger')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['output_messages'].append(data)
            self.output_record['work_trigger'].append(data)

        self.output_message_stream.for_each(record_output)
        self.work_trigger_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_info = {'all_first_person_shop': [], 'clock': []}

        clock_now = 9
        self.clock_stream.add_item({"time": 2024 / 8 / 15 / clock_now})
        cou = 0
        for frame in self.video_data:
            sent_info['all_first_person_shop'].append(frame)
            self.input_shop_stream.add_item({"frame": frame})
            cou += 1
            if cou % 3 == 0:
                clock_now += 1
                sent_info['clock'].append({"time": 2024 / 8 / 15 / clock_now})
                self.clock_stream.add_item({"time": 2024 / 8 / 15 / clock_now})
        return sent_info
