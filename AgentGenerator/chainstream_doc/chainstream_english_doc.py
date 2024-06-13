chainstream_english_prompt = '''
ChainStream Introduction:

ChainStream is a development framework for processing streaming data, written in Python code. You are required to master the usage of this framework to handle a series of data streams according to the tasks provided by users. These data streams are generated by software or hardware. Data streams from hardware can include image streams from cameras, audio streams from microphones, and location information streams from GPS; data streams from software can include data streams generated by apps, screenshot image streams from computers, etc. You need to select the appropriate data streams and design the processing methods for these data streams to complete the tasks set by users. During this process, you can also create new data streams. Next, I will introduce the various modules of this framework and their usage.

Stream Module:

Description:
The Stream class is the core of the data stream. Each data stream is an instance of Stream, and ChainStream uses stream_id to distinguish different data streams. ChainStream listens to and processes the data in the data stream by attaching listener functions to the data stream. Multiple listener functions can be attached to a data stream, and when data enters the data stream, ChainStream will automatically call the attached listener functions to process the data accordingly. The following will introduce the methods related to the Stream class.

API:

chainstream.get_stream(stream_id): This method retrieves a Stream object based on stream_id.
chainstream.create_stream(stream_id): This method creates a new data stream. It creates and returns a Stream instance, using stream_id as the identifier for the data stream.
chainstream.stream.Stream.register_listener(agent, listener_func): This method attaches a listener function to a Stream instance. listener_func is the listener function to be attached, and agent is the identifier of the Agent that attaches this function.
chainstream.stream.Stream.unregister_listener(agent): This method unregisters the listener functions attached to a data stream, specifying the identifier agent, and all listener functions attached by this Agent will be unregistered.
Agent Module:

Description:
You need to create one or more Agents to complete the tasks specified by users. The Agent instances you create need to inherit from the chainstream.agent.Agent class and implement the __init__, start(), and stop() methods to listen to, process, and output the results of the relevant data streams.

API:

__init__(agent_id): This method creates an Agent for completing tasks by instantiating a new Agent object, with agent_id being the specified Agent identifier. You also need to perform operations such as obtaining or creating data streams, creating data containers, and other initialization resources in this method to prepare data for task execution.
start(): In this method, you need to define the listener functions for processing the data stream and bind these listener functions to the corresponding data streams.
stop(): In this method, you need to unregister all listener functions that this Agent has attached to the data streams.
BufferContext Module:

Description:
If you need to store processed data during the task execution, you can use the BufferContext module to create a data container. This data container is a queue where you can only add data at the end and retrieve stored data from the front. The following will introduce the usage of this module.

API:

chainstream.context.BufferContext(): This method creates a data container by instantiating a new BufferContext object.
chainstream.context.BufferContext.add(data): This method adds data to the end of the data container. You can store any form of data, including images, text, audio, etc.
chainstream.context.BufferContext.get(): This method retrieves the data at the front of the data container. The next stored data in the queue will become the new front data.
LLM Module:

Description:
The LLM module integrates various models that can process multiple types of input data, including text, images, and sound, according to the input processing requirements. You can describe your needs in the processing requirements, and the model will respond accordingly based on your requirements and the data you provide. Please note that ChainStream does not guarantee that the responses from these models are always reliable; you need to describe your processing requirements as detailed as possible.

API:

chainstream.llm.get_model(type): This method instantiates a new LLM object to obtain a model for processing data. type is one of ['text', 'image', 'audio'], describing the type of data the obtained model needs to process.
chainstream.llm.make_prompt(query, data): This method converts the processing requirements and input data into an input that the model can accept. query is the processing requirement, describing how you want to process the input data or what information you want to obtain from the input data, such as: "Describe the specific content of this image", "How many people are speaking in this audio clip". data is the input data, which must be consistent with the data type that the model can process. This method returns the input prompt that the model can accept.
chainstream.llm.query(prompt): This sends the input prompt to the model and returns the model's response.
Example:

Next, I will give you a specific example to show how you should use ChainStream to complete an Agent. Suppose a user wants to filter English messages from a new message queue, you can provide an Agent like this:

from chainstream.agent import Agent
from chainstream.stream import get_stream, create_stream
from chainstream.llm import get_model

class EnglishMessageFilter(Agent):
    def __init__(self):
        super(EnglishMessageFilter, self).__init__("EnglishMessageFilter")
        self.message_from = get_stream("all_messages")
        self.english_message = create_stream("english_message")

        self.llm = get_model("text")

    def start(self):
        def filter_message(message):
            message_content = message["content"]
            prompt = "Is this message in English? Say 'yes' or 'no'."
            response = self.llm.generate(prompt, message_content)
            if response.lower() == "yes":
                self.english_message.add_item(message)

        self.message_from.register_listener(self, filter_message)

    def stop(self):
        self.message_from.deregister_listener(self)
You can create more than one Agent, allowing them to work together to complete user tasks.
If you have mastered the ChainStream framework and can use this framework to write Agents to handle user tasks, please reply with "I understand" and be ready to process user requirements.
'''
