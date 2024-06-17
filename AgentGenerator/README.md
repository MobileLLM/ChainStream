## AgentGenerator

generate ChainStream Agent from natural language.

file tree:
* chainstream_doc: chainstream introduction and usage prompt.
* DSL_examples: examples of DSL agents, no need to put agent file here, just write a fetch script to load from .agents folder. And need finish example_selector.py.
* tasks: generate tasks prompt, not for NL2DSL.
* agent_generator.py: the main script to generate agent from natural language.

TODO List:
* update chainstream api prompt, remove memory part.
* test differences between gpt-4 and gpt-4o
* finish example_selector.py, select example based on user task.
* finish nl2dsl.py, as a coding interface, we just need use it like this:
``` python

import chainstream.runtime as runtime
from nl2dsl import NL2DSL

nl2dsl = NL2DSL(model_name='gpt-4o')

new_agent_code = nl2dsl.generate_dsl('filter all message from my friend')

runtime.start_agent(new_agent_code)

```