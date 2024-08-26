from ChainStreamSandBox.tasks import ALL_TASKS
from ChainStreamSandBox.sandbox.chainstream_sandbox import ChainStreamSandBox
from AgentGenerator.prompt.feedback_processor import FilterErrorFeedbackProcessor


def test_task(task_id, agent=None):
    task = ALL_TASKS[task_id]()
    sandbox = ChainStreamSandBox(task, task.agent_example if agent is None else agent, save_path=None)

    report = sandbox.start_test_agent(return_report_path=False)

    haha = FilterErrorFeedbackProcessor()
    print("feedback:", haha(report))
    print(report["output_stream_items"])
    print(report['stdout'])



if __name__ == '__main__':
    agent = """
import chainstream
from chainstream.agent import Agent
from chainstream.stream import get_stream
from chainstream.context import Buffer
from PIL import Image
from io import BytesIO
import base64
import time

class ClinicAgent(Agent):
    def __init__(self, agent_id: str = "clinic_agent"):
        super().__init__(agent_id)
        # Get input streams
        self.outdoor_stream = get_stream(self, "all_third_person_outdoor")
        self.indoor_stream = get_stream(self, "all_third_person_indoor")
        
        # Get output streams
        self.output_messages_stream = get_stream(self, "output_messages")
        self.patient_trigger_stream = get_stream(self, "patient_trigger")

        # Initialize a buffer to store frames
        self.buffer = Buffer()
        self.patient_count = 0

    def start(self):
        def process_outdoor_frame(item):
            print("Processing outdoor frame")
            # Add timestamp to the item
            item['timestamp'] = time.time()
            # Decode the image
            img_data = base64.b64decode(item['frame'])
            image = Image.open(BytesIO(img_data))
            # Process the image (This is a placeholder, in a real scenario, we would use some image processing logic)
            self.buffer.append(item)
            self.check_patient_count()

        def process_indoor_batch(items):
            print("Processing indoor batch")
            # Process each frame in the batch
            for item in items['item_list']:
                # Add timestamp to the item
                item['timestamp'] = time.time()
                # Decode the image
                img_data = base64.b64decode(item['frame'])
                image = Image.open(BytesIO(img_data))
                # Process the image (This is a placeholder, in a real scenario, we would use some image processing logic)
                self.buffer.append(item)
            self.check_patient_count()

        def check_patient_count():
            print("Checking patient count")
            # Count the number of patients (This is a placeholder logic)
            buffer_items = self.buffer.get_all()
            self.patient_count = len(buffer_items)
            print(f"Patient count: {self.patient_count}")
            if self.patient_count > 5:
                print("Triggering patient status: True")
                self.patient_trigger_stream.add_item({"Status": "True"})
            else:
                print("Triggering patient status: False")
                self.patient_trigger_stream.add_item({"Status": "False"})

            # Check if patients have been waiting for a period of time
            if self.patient_count > 0:
                current_time = time.time()
                first_patient_time = buffer_items[0].get('timestamp', current_time)
                print(f"First patient waiting time: {current_time - first_patient_time}")
                if current_time - first_patient_time > 300:  # 5 minutes
                    print("Triggering output message")
                    self.output_messages_stream.add_item({"Notion": "There are patients who are waiting for a period of time"})

        # Attach listener functions to the input streams
        self.outdoor_stream.for_each(process_outdoor_frame)
        self.indoor_stream.batch(by_time=5).for_each(process_indoor_batch)

    def stop(self):
        # Unregister all listeners
        self.outdoor_stream.unregister_all(self)
        self.indoor_stream.unregister_all(self)

# Instantiate the agent (This line is for testing purposes and should be removed in the final implementation)
# agent = ClinicAgent()
        """
    test_task("WaitingRoomTask", agent=agent)
