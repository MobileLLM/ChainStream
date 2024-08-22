from ChainStreamSandBox.tasks import ALL_TASKS
from ChainStreamSandBox.sandbox.chainstream_sandbox import ChainStreamSandBox


def test_task(task_id, agent=None):
    task = ALL_TASKS[task_id]()
    sandbox = ChainStreamSandBox(task, task.agent_example if agent is None else agent, save_path=None)

    report = sandbox.start_test_agent(return_report_path=False)

    print(report["output_stream_items"])
    print(report['stdout'])



if __name__ == '__main__':
    agent = """
import chainstream
from chainstream.agent import Agent
from chainstream.stream import get_stream
from chainstream.llm import get_model, make_prompt
class ActionDetectionAgent(Agent):
    def __init__(self, agent_id: str = "action_detection_agent"):
        super().__init__(agent_id)
        # Get the input stream
        self.input_stream = get_stream(self, "first_person_perspective_data")
        # Get the existing output stream
        self.output_stream = get_stream(self, "analysis_actions")
        # Get the LLM model for image processing
        self.llm_model = get_model(["image"])
    def start(self) -> None:
        def detect_action(frame_data):
            print("Received frame data:", frame_data)  # Log input data
            # Extract the image from the frame data
            image = frame_data['frame']
            # Prepare the prompt for the LLM
            prompt = make_prompt({
                "image": image,
                "task": "Detect the current action from the first person perspective image. Respond with only the action tag in one or two words."
            })
            print("LLM prompt:", prompt)  # Log the prompt
            # Query the LLM to get the action tag
            action_tag = self.llm_model.query(prompt)
            print("Detected action:", action_tag)  # Log the detected action
            # Send the action tag to the output stream
            return {"analysis_result": action_tag.strip()}  # Ensure the response is clean
        # Register the listener function to the input stream
        self.input_stream.for_each(detect_action, to_stream=self.output_stream)
    def stop(self) -> None:
        # Unregister all listeners
        self.input_stream.unregister_all(self)
        """
    test_task("VideoTask1")
