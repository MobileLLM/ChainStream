import os
import json
from sandbox import SandBox
from AgentGenerator.nl2dsl import NL2DSL
from tasks import ALL_TASKS

def evaluate_nl2dsl():
    results_dir = './results'
    os.makedirs(results_dir, exist_ok=True)
    all_results = []
    for task_name, task_class in ALL_TASKS.items():
        task_config = task_class()
        task_description = task_config.task_description
        # agent_code = NL2DSL().generate_dsl(task_description)
        agent_code = '''
import chainstream as cs
from chainstream.llm import get_model

class TestAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_arxiv_agent")
        self.input_stream = cs.get_stream("all_arxiv")
        self.output_stream = cs.get_stream("cs_arxiv")
        self.llm = get_model(["text"])
        self.output_items = []

    def start(self):
        def process_paper(paper):
            if "abstract" in paper:
                paper_title = paper["title"]
                paper_content = paper["abstract"]
                paper_versions = paper["versions"]
                stage_tags = ['Conceptual', 'Development', 'Testing', 'Deployment', 'Maintenance','Other']
                prompt = "Give you an abstract of a paper: {} and the version of this paper: {}. What tag would you like to add to this paper? Choose from the following: {}".format(paper_content, paper_versions, ', '.join(stage_tags))
                prompt_message = [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
                response = self.llm.query(prompt_message)
                print(paper_title + " : " + response)
                self.output_stream.add_item(paper_title + " : " + response)
                self.output_items.append(paper_title + " : " + response)
        self.input_stream.register_listener(self, process_paper)

    def get_output_items(self):
        return self.output_items

    def stop(self):
        self.input_stream.unregister_listener(self)
'''

        oj = SandBox(task_config, agent_code)
        try:
            oj.start_test_agent()
            res = oj.result
        except Exception as e:
            print(f"Error occurred while testing agent for task {task_name}: {e}")
            res = {"error": str(e)}

        agent = oj.get_agent()
        if agent is not None and hasattr(agent, 'get_output_items'):
            output_items = agent.get_output_items()
            if output_items is None:
                output_items = []
            res['output_items'] = output_items
        else:
            res['output_items'] = []

        all_results.append(res)

        with open(f"{results_dir}/{task_name}.json", "w") as f:
            json.dump(res, f)

    return all_results

if __name__ == '__main__':
    all_results = evaluate_nl2dsl()
    print(all_results)
