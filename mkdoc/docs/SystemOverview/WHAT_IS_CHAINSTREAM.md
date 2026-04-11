# What is ChainStream?

ChainStream is a framework that aims to better support long-term perception capabilities of Agent implementation. The framework uses a multi-layered event-driven stream-based structure, which is designed to realize Agent's long-term perception capability and information sharing capability.

## What is a Stream? What is Event-driven?
Stream is a data pipeline, similar to a water pipe, with an entrance and an exit. Any content can be placed into the stream at any time, and the data will automatically flow downstream to the Agent.

Stream and Agent are related through listening, which is similar to Youtube channel subscription:
- Youtube user subscribes to a channel, and when a new video is published, Youtube will automatically push it to the user.
- Agent listens to a stream, and when new data is pushed to the stream, ChainStream will automatically push it to the Agent.

This pre-listening and automatic pushing mechanism is the core of event-driven architecture. The main advantage of event-driven architecture is that it reduces unnecessary computations in large computation graphs.

## What is an Agent in ChainStream?

The functionalities of an Agent in ChainStream can be subscribed to a stream or written to a stream. An Agent is a logical concept that can include one or more functions.

We can view Agent Function as a transformation function in a stream. For example, for a monitoring camera, it can be considered as the source of a continuous video stream, and the unit of the stream is a video frame. When we construct a Person Detection Agent, it can subscribe to this video stream, perform object detection on it, and push the frames with people to a new stream.
We obtain the Person Stream. Further, we can listen to a Face Recognition Agent to produce a Face Stream. We can construct a complex Agent stream graph in this way.

Based on the above example, we can see that the core idea of ChainStream is to implement perception tasks through multiple atomic transformation steps. And each intermediate step in the stream can be used by other Agents. This makes sharing between Agents more convenient.

For the ChainStream Runtime, its job is to maintain a large Stream Flow Graph that is merged from all Agents, and to implement automatic pushing of streams through event-driven mechanisms. It also performs various system optimizations on the Graph.

## ChainStream VS Agent Frameworks


There are many Agent frameworks out there, some of them are mature and large, such as LangChain, AutoGPT, MetaGPT. What are the differences between ChainStream and these frameworks?

The most obvious difference is that ChainStream is still relatively small:laughing: It has a smaller size compared to other frameworks, and it is still in its early stage of development.

However, the core difference is that:

- Different types of Agents: Most existing Agent frameworks are designed for Problem-solving Agents, while ChainStream is mainly designed for Context-aware Agents, which require long-term perception capabilities.
- Focus on Perception: ChainStream currently concentrates on better solving long-term perception problems. As far as we know, ChainStream is the first framework to develop independent modules specifically for perception.
- Unique Structure: All agents are integrated into a large event-driven flow graph, facilitating information sharing among agents and global system optimization.
- Edge-oriented: While most agent frameworks are cloud-oriented, ChainStream focuses on edge scenarios, attempting to bridge the sensor boundaries between different edge devices.

Overall, ChainStream, as a relatively new conceptual framework, is still in its early stages. **In the short term, we hope it can focus on enhancing the long-term perception capabilities of agents, providing a refined and efficient solution for agent perception. In the long term, we also envision ChainStream becoming a comprehensive framework for large-scale agent development, exploring its potential for edge application development and deployment. We aim to leverage the open-source community to improve its capabilities in all aspects.**