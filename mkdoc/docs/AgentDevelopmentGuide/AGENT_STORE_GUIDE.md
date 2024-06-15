# Agent Store Guide

In the future, we will provide an Agent Store server, which will primarily include features such as the agent package publishing process, review mechanisms, version management, and agent search.

Currently, the Agent Store is still in the planning stage. For now, we have placed the initially implemented agents in the `agents` directory of our GitHub repository. Users can directly search for these agents in the Dashboard and run them immediately.

## Agent Package Structure

In an agent, the following items have to be configured:

- Agent name, description, package (zip)
- ChainStream version
- Devices: desktop, phone, glass, watch, etc. (numbers)
- Deployment doc: how the devices are deployed
- Dependency: other agents/streams/memory that must be available and their versions
- LLM: models that must be available
- Public streams/memory: output streams/memory that can be seen by other agents
