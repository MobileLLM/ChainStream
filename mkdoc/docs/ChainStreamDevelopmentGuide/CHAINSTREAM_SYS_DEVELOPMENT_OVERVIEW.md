# ChainStream Development Overview

## System Architecture

Please see [ChainStream System Architecture Design](../../SystemOverview/SYSTEM_SCENARIOS/) for more details.

## Main Components

- **ChainStream Runtime**: The runtime module is responsible for executing the ChainStream application, including application scheduling, resource management, and data flow.
- **ChainStream SDK**: The SDK module provides developers with interfaces for application development, data flow, and resource management.
- **ChainStream Agent Generator**: The Agent generator module is responsible for generating Agent code based on the application description file.
- **ChainStream Dashboard**: The control panel module provides visualized application management, monitoring, and alarming functions.
- **ChainStream Agent Store**: The Agent repository module provides storage, distribution, and update functions for Agent code.
- **ChainStream SandBox**: The sandbox module provides online debugging and testing capabilities for developers.
- **ChainStream Doc**: The documentation module provides the writing, publishing, and management of ChainStream-related documents.
- **ChainStream Edge Sensor**: The edge sensor module provides access, management, and data collection capabilities for edge computing devices.

## Join the Development

### Project Communication

We maintain a public Zulip chat room for ChainStream development. Please join us and discuss with us. The link is: [mobilellm.zulipchat.com](https://mobilellm.zulipchat.com/#narrow/stream/419866-web-public/topic/ChainStream)

You can contact ChainStream members directly through Zulip. You can also contact us by email [jia.cheng.liu@qq.com](mailto:jia.cheng.liu@qq.com).

### Project Management

Zulip play a role in project management.

Github Project and Issue also play a role in project management. You can follow [ChainStream-Team planning](https://github.com/orgs/MobileLLM/projects/2) and [ChainStream Issues](https://github.com/MobileLLM/ChainStream/issues).

### Branch Management

* Main branch: main
* Dev branch: dev
* Feature branch: feature/xxx
* Fix branch: fix/xxx
* Docs branch: docs/xxx
* Temp branch: temp/xxx
* Docs page: gh-pages



### Code Style

There are no specific development guidelines at the moment, including issue, PR, and commit message. We welcome suggestions from everyone.

The main points to keep in mind are:

1. Communicate with us through various channels, including email, Zulip, and Github Issue, to let us know your ideas and opinions about the project.
2. Code style and naming conventions.
3. It is recommended to use unit tests and integration tests.
4. Try to describe your modifications in the PR.


