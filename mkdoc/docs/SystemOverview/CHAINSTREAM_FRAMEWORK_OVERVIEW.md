# ChainStream Framework Architecture

<img src="../../img/ChainStreamArchNew.png" alt="ChainStream"/>

The diagram above illustrates the architecture of the ChainStream framework in a narrow sense. The ChainStream framework mainly comprises the following layers:

1. **Agent Layer**: Includes user agents and system agents, similar to user apps and system apps in the Android system. User agents are those that users can freely install and uninstall to meet specific user needs, whereas system agents are essential components necessary for system operations, responsible for core system functions.
2. **Libraries Layer**: Provides the core abstractions of ChainStream, mainly including parts such as Stream, Agent, Models, Memory, and Prompt.
3. **Runtime Layer**: Responsible for maintaining the global streaming computation graph, executing optimization and scheduling, and managing and allocating resources.
4. **Abstraction Layer**: Offers unified virtualization of resources, primarily including computational model resources, interface resources, data source resources, and more.
5. **Infrastructure Layer**: Manages underlying hardware resources, including CPU, GPU, network, storage, and others.