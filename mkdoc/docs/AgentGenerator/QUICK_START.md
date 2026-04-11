# Quick Start

## What is the Agent Generator?

The ChainStream framework was originally designed to support more powerful agents, where an important concept is that the agents themselves are also users, developers, and administrators of the framework. Agents need to understand the syntax structure of the ChainStream framework and be able to write correct code based on it. This involves converting from natural language (NL) to code.

However, NL is still too far removed from the underlying APIs, as task descriptions are often abstract, and the various APIs are too complex. Therefore, ChainStream's solution is to encapsulate both the upper and lower layers to reduce the gap between them. As shown in the figure:

![generator_motivation.png](..%2Fimg%2Fgenerator_motivation.png)

Specifically, ChainStream designs a streaming data structure and a streaming framework at the lower layer to unify various data APIs into a single interface. At the upper layer, it designs a Query Optimizer to enhance user natural language descriptions, a Sandbox agent simulation environment, and an agent generation process, known as the Agent Generator.

ChainStream's Agent Generator can accept task descriptions in natural language, generate ChainStream framework agent code, and autonomously debug it in the ChainStream Sandbox to optimize the final result. Currently, the Agent Generator is mainly targeted at perception tasks and performs well on the NL-Sense Benchmark we designed.

## How to Use the Agent Generator to Generate Agents?

In the [AgentGenerator/generator](https://github.com/MobileLLM/ChainStream/tree/main/AgentGenerator/generator) directory, as of October 2024, the following Generator scripts are provided:

``` 
AgentGenerator/generator
├── generator_base.py   # Base class
├── batch_mode          # Generator for creating batch mode agents, mainly referring to the mode in which agents operate in the Sandbox and Runtime. See the Sandbox section for details.
│   ├── batch_langchain_zeroshot_generator.py   # Generator for writing LangChain agents in batch mode, without reference examples.
│   ├── batch_native_gpt_zeroshot_generator.py  # Agent using GPT to perform perception tasks directly in batch mode. This is a special baseline that does not generate new agents but returns a perception script calling GPT.
│   ├── batch_native_python_feedback_guided_without_real_task.py    # Generator for writing native Python agents in batch mode, without reference examples but automatically debugs in the Sandbox.
│   └── batch_native_python_zeroshot_generator.py   # Generator for writing native Python agents in batch mode, without reference examples, and does not debug in the Sandbox.
└── stream_mode         # Generator for creating streaming mode agents, including ChainStream agents using listener APIs and Python and LangChain agents using blocking APIs.
    ├── chainstream_cot_generator.py    # Generator for writing ChainStream agents in streaming mode, without reference examples, using Chain-of-Thought generation.
    ├── chainstream_feedback_guided_generator_for_starting.py   # Generator for writing ChainStream agents in streaming mode, without reference examples, automatically debugs in the Sandbox, but without real simulation data, only retrieves hard error information.
    ├── chainstream_feedback_guided_generator_for_debugging.py  # Generator for writing ChainStream agents in streaming mode, without reference examples, automatically debugs in the Sandbox, no real simulation data, retrieves hard error information, and can autonomously send test cases and retrieve output.
    ├── chainstream_feedback_guided_generator_for_real_task.py  # Generator for writing ChainStream agents in streaming mode, without reference examples, automatically debugs in the Sandbox with real simulation data, retrieves error, output, and stdout information. This is the main method used in the paper.
    ├── chainstream_feedback_guided_generator_for_real_task_with_example.py  # Generator for writing ChainStream agents in streaming mode, with reference examples, automatically debugs in the Sandbox with real simulation data, retrieves error, output, and stdout information. This is the main method used in the paper.
    ├── chainstream_few_shot_generator.py    # Generator for writing ChainStream agents in streaming mode, with reference examples, without Sandbox debugging. This is the non-iterative method used in the paper.
    ├── stream_langchain_zeroshot_generator.py    # Generator for writing LangChain agents in streaming mode, without reference examples or Sandbox debugging.
    ├── stream_native_python_feedback_with_real_task.py   # Generator for writing native Python agents in streaming mode, automatically debugs in the Sandbox with real simulation data, retrieves error, output, and stdout information.
    └── stream_native_python_zeroshot_generator.py    # Generator for writing native Python agents in streaming mode, without reference examples, and does not debug in the Sandbox.
```

Each script can be run with code like the following:

``` python
if __name__ == '__main__':
    from ChainStreamSandBox.tasks import ALL_TASKS
    generator = ChainstreamFeedbackGuidedGeneratorForRealTask(framework_example_number=0)  # Select a Generator
    task = ALL_TASKS["HealthTask4"]()  # Select a perception task
    haha = generator.generate_agent(
        StreamListDescription(streams=[     # Describe the task
            {
                "stream_id": "remind_rest",
                "description": "A stream of reminders to take a rest when the heart rate is over 75 in every 2 seconds.",
                "fields": {
                    "Heart Rate": "the heart rate data from the health sensor, float",
                    "reminder": "Heart rate is too high!Remember to rest yourself!"
                }
            }
        ]),
        input_description=task.input_stream_description,    # Specify input stream scope
        task=task,      # Specify task
    )

    agent_code, latency, tokens = haha[0], haha[1], haha[2]  # Get the generated agent code, latency, and the number of generated tokens

    print(agent_code)
    print(latency)
    print(tokens)
```

Simply select the appropriate Generator script and write the task description to generate agent code.

## How to Evaluate the Agent Generator on the NL-Sense Benchmark?

For details, see the [NL-Sense Benchmark](../../NLSenseBenchmark/QUICK_START/) section.