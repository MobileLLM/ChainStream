from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import DesktopData
from ChainStreamSandBox.raw_data import SpharData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class StudentInClassTask(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_number_stream = None
        self.warning_board_stream = None
        self.input_three_person_stream = None
        self.input_screenshot_stream = None
        self.input_stream_description1 = StreamListDescription(streams=[{
            "stream_id": "all_screenshot",
            "description": "students screenshot data",
            "fields": {
                "image_file": "image file in the Jpeg format processed using PIL,string"
            }
        }, {
            "stream_id": "all_classroom",
            "description": "classroom surveillance camera data",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "students_number",
                "description": "An electronic blackboard used to record the number of students in the classroom.",
                "fields": {
                    "student_numbers": "the number of the students,string"
                }
            },
            {
                "stream_id": "warning_board",
                "description": "An electronic blackboard used to warn the students who play their cellphones in the "
                               "class.",
                "fields": {
                    "warning_message": "the warning message to the students who break discipline,string"
                }
            }
        ])
        self.screenshot_data = DesktopData().get_random_sample()
        self.video_data = SpharData().load_for_traffic()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask11(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task11"):
        super().__init__(agent_id)
        self.classroom_input = cs.get_stream(self, "all_classroom")
        self.screenshot_input = cs.get_stream(self, "all_screenshot")
        self.numbers_output = cs.get_stream(self, "students_number")
        self.warning_board_output = cs.get_stream(self, "warning_board")
        self.llm = cs.llm.get_model("image")
        self.output_buffer = Buffer()
    def start(self):
        def count_number(three_person_data):
            prompt = "How many students are in the classroom right now?Tell me the number."
            res = self.llm.query(cs.llm.make_prompt(prompt,three_person_data))
            self.numbers_output.add_item({
                "student_numbers": res
            })
            return res
        def analyze_screenshot(screenshot):
            prompt = "Analyze whether I'm looking at something that is not related to study.Simply answer y or n"
            res = self.llm.query(cs.llm.make_prompt(prompt,screenshot['image_file']))
            if res.lower() == "y":
                self.warning_board_output.add_item({
                    "warning_message":"Please pay attention to your study."
                })
            return screenshot
        self.screenshot_input.for_each(analyze_screenshot)
        self.classroom_input.for_each(count_number)
        '''

    def init_environment(self, runtime):
        self.input_three_person_stream = cs.stream.create_stream(self, 'all_classroom')
        self.input_screenshot_stream = cs.stream.create_stream(self, 'all_screenshot')
        self.output_number_stream = cs.stream.create_stream(self, 'students_number')
        self.warning_board_stream = cs.stream.create_stream(self, 'warning_board')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_number_stream.for_each(record_output)
        self.warning_board_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.video_data:
            sent_messages.append(message)
            self.input_three_person_stream.add_item({"frame": message})
        for message in self.screenshot_data:
            sent_messages.append(message)
            self.input_screenshot_stream.add_item(message)
        return sent_messages
