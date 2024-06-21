# Runtime Optimization - LLM

## Objective

In the future, ChainStream will operate a large-scale Stream flow graph, leading to significant computational load both per unit time and cumulatively over long periods of uptime. This will result in substantial token fee costs. Currently, there are many types of LLMs with varying performance levels. However, for user developers, the chosen LLM only needs to meet their requirements. Often, the strongest and most expensive models are selected to maximize performance, resulting in unnecessary additional costs.

ChainStream aims to optimize token fees from a system perspective. This primarily involves two parts: custom models and model selection:

- Custom Models: For a specific task, attempt to fine-tune a custom LLM after accumulating a certain amount of data.
- Model Selection: Choose among the strongest cloud model, a standard cloud model, a local model, and a custom model to find a trade-off between cost and effectiveness.

Here, we will primarily discuss the design of model selection.

The goals for model selection include:

- LLM API specifies only the model type, such as text-only models, vision models, speech models, etc.
- ChainStream Runtime provides support for various LLM interface classes, including common cloud and local LLMs.
- Monitor the performance of different model types over time and select the optimal model based on their performance.
- Schedule all requests for different model types in real-time.

## Model Selection

ChainStream automatically detects the performance of the LLM used in each task and selects a more suitable specific model accordingly. Users only need to specify the required LLM type.

<img src="../../img/LLMRuntimeOptimize.png" alt="ChainStream System Components">

The detailed design includes the following parts:

- **API**: Determine the number of LLM types to support.
- **LLM SDK**:
  - `get_model` returns the LLM interface class based on the LLM type.
  - The LLM interface class does not execute the actual query.
  - Attach a recorder to each LLM interface class.
- **Runtime**:
  - The LLM manager manages each instance of the LLM interface class.
  - Attach a router to each LLM interface class, selecting the LLM type based on the performance of the node itself and downstream nodes.
- **Abstraction Layer**:
  - Support various LLM models, encapsulating model instance classes for each LLM type.
  - Attach a recorder to each LLM instance class to record runtime performance data.
  - Attach a query queue to each LLM instance class, scheduling based on the source agent's priority and traffic conditions.
- **Evaluation**:
  - Use the ChainStream benchmark to evaluate the accuracy and cost of this method. The strongest model serves as the upper limit for accuracy, while the cheapest model serves as the lower limit for costs.