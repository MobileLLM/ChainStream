# ChainStream Application Scenarios

## Continuous Perception

Our ideal agent perception is seamless, continuous in time, data range, and in the perception process and results.

- Continuous in time: The agent's perception is uninterrupted, constantly perceiving everything within its field of view and recording what it deems important.
- Continuous in data range: The agent's perception can span multiple data sources. ChainStream provides Edge Sensors to bridge different devices, sensors, and data sources.
- Continuous in perception process and results: Different agents' perception steps can intersect, and results can be reused, breaking the boundaries between agents.

## ChainStream Product Architecture

The main product architecture of ChainStream consists of a three-tier system: multi-edge sensing devices + local server + cloud server.

- Multi-edge devices: Known as Edge Sensors, these act as the senses and appendages of the entire system, responsible for transmitting sensor data to the local server and executing corresponding actions based on instructions, such as notifications and sound playback.
- Local server: A trusted server deployed locally by each user, responsible for connecting and controlling edge devices, performing main ChainStream computations, hosting local large models, storing high-privacy data, and more.
- Cloud server: A supplementary service provided by ChainStream cloud service providers, including more powerful cloud large models, cloud storage, and an Agent Store.

It is clear that due to privacy and security considerations, a significant portion of ChainStream's computation and storage is done locally. Therefore, users need to configure edge devices, local servers, and trusted local area networks according to their needs.

## Scenario Examples

ChainStream is aimed at a variety of users, including but not limited to:

- Individuals
- Families
- Enterprises
- Shops, offices, schools

Each ChainStream system is shared by all users, terminals, and devices within the user's range.

<img src="../../img/ChainstreamExample.png" alt="ChainStream"/>

In our vision, ChainStream can be applied to the scenarios shown above:

- Personal Assistant: Mainly connects personal phones, wearable devices, smart furniture, and other devices. It perceives the daily life of individual users and provides personalized services.
- Family Assistant: Mainly connects family members' phones, smart furniture, and other devices. It perceives the daily life of family members and provides family services.
- Enterprise Assistant: Mainly connects employees' phones, office equipment, and other devices. It perceives the daily work of employees and provides enterprise services.
- Professional Scenario Assistant: Refers to specialized environments like kitchens, workshops, laboratories, assembly line workshops, and more. It perceives the daily work in professional scenarios, functioning as a log recorder, compliance checker, process guide, and more.