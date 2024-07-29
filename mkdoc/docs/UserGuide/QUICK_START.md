# Quick Start

## System Structure

As mentioned in the [ChainStream Application Scenarios](../../SystemOverview/SYSTEM_SCENARIOS/), the ideal ChainStream product structure includes three tiers: edge devices, local server, and cloud server. Currently, the system has implemented the functionalities of the edge devices and local server, while the cloud server functionality is still under development.

We provide an Edge Sensor App for the Android system. Once the app is installed on a device, it can quickly connect the edge device to the local server.

For the local server, the environment currently needs to be configured and run manually. In the future, we plan to support Docker and release packaged applications.

## Local Server Configuration and Startup

First, clone the project code from GitHub:

```bash
git clone https://github.com/MobileLLM/ChainStream.git
```

Then, install the dependencies in the appropriate interpreter:

```bash
pip install -e .
```

Finally, start the local server:

```bash
python start.py
```

Then, open the web browser and go to `http://localhost:6677/`. You should see the home page of the local server.