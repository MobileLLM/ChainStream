# Control Panel Guide

We provide two methods to interact with the ChainStream Runtime: Web and shell. We recommend using the Web method as it is more intuitive and feature-rich.

By default, when you run the `python start.py` command, the ChainStream Runtime will automatically open the Web control panel at the default address `http://localhost:6677`.

The Web control panel is currently in the testing phase, and its functionalities are not yet complete. We have reserved interfaces for planned features, which will be gradually improved.

The currently implemented features mainly include Agent management, Stream monitoring, and Stream Flow Graph monitoring.

## Managing Agents

<img src="../../img/dashboard_agent.png" alt="Agent Management">

The left-hand list automatically scans and loads all Agents from the specified path, allowing you to start, stop, restart, or delete Agents.

The right-hand side displays basic information about running Agents, including Agent ID, Agent name, Agent type, Agent status, Agent creation time, and more.

## Monitoring the Stream Flow Graph

<img src="../../img/dashboard_stream_graph.png" alt="Stream Flow Graph Monitoring">

The dynamic graph shows the current streaming computation graph of the system, providing an intuitive view of the topology and statistical information of the connections between various Agents.