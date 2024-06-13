# ChainStream System Overview

<img src="../../img/ChainStreamMainComponents.png" alt="ChainStream System Components">

In a narrow sense, ChainStream is mainly an LLM Agent development framework, centered around its provided APIs and runtime. Broadly speaking, ChainStream also includes the various components shown in the image above, which primarily consist of:

- **Sensor Agents**: Perception agents developed using the ChainStream SDK and running within the ChainStream Runtime.
- **ChainStream SDK**: Provides the necessary APIs for developing Sensor Agents, including functions for data collection, data processing, and data transmission.
- **ChainStream Runtime**: Runs Sensor Agents, maintains a global streaming computation graph, controls various edge devices, and manages global resources.
- **Edge Sensor**: Provides apps for systems like Android, Linux, and Windows, capable of integrating the data sources on these devices into the ChainStream Runtime.
- **Dashboard**: The control panel for ChainStream Runtime, mainly used for visualization, configuration, control, and analysis of the runtime.
- **Agent Generator**: A tool that can directly convert natural language descriptions of agents into code, which then runs in the ChainStream Runtime.
- **Sandbox**: A simulation environment for agents, enabling the simulation of the environment in which the agents will run and providing functionalities for agent development, debugging, and testing.
- **Agent Store**: A repository for agents, offering functionalities for sharing, publishing, and searching for agents.